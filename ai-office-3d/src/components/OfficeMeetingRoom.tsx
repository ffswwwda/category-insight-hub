import { useState, useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'
import { AGENT_ROSTER, MEETING_EXPERTS } from '@/scene/layout/officeLayout'
import { getOfficeScene } from '@/scene/officeSceneBridge'
import {
  addLiveProject, updateTask,
  type LiveProject, type ProjectTask,
  getLLMConfig, setLLMConfig, isLLMEnabled,
} from '@/store/workspaceStore'
import {
  buildReply, buildPlanItems, buildTaskOutput,
  type ChatMsg, type MeetingContext,
} from '@/lib/meetingEngine'
import { kbOf } from '@/lib/employeeKB'

function SvgIcon({ id, size = 14 }: { id: string; size?: number }) {
  return <svg viewBox="0 0 24 24" width={size} height={size}><use href={'#' + id}/></svg>
}

const ROSTER: Record<string, { id: string; name: string; color: number; task: string }> =
  Object.fromEntries(AGENT_ROSTER.map((r) => [r.id, r]))
const EXPERT: Record<string, { id: string; competency: string; keywords: string[] }> =
  Object.fromEntries(MEETING_EXPERTS.map((e) => [e.id, e]))
const nameOf = (id: string) => ROSTER[id]?.name ?? id
const colorHex = (id: string) => '#' + (ROSTER[id]?.color ?? 0x888888).toString(16).padStart(6, '0')

type Step = 'setup' | 'discuss' | 'plan' | 'done'

/** 「建议拉取员工」：按主题/目的关键词命中打分排序 */
function suggestExperts(topic: string, purpose: string) {
  const text = (topic + ' ' + purpose).toLowerCase()
  return MEETING_EXPERTS
    .map((e) => {
      const hits = e.keywords.filter((k) => text.includes(k.toLowerCase()))
      return { id: e.id, score: hits.length, hits }
    })
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
}

function buildPlanDoc(topic: string, purpose: string, items: Array<{ ownerId: string; title: string }>): string {
  const lines: string[] = []
  lines.push('# 会议规划与执行方案')
  lines.push(`> 主题：${topic || '（未填写）'}`)
  lines.push(`> 目的：${purpose || '（未填写）'}`)
  lines.push('')
  lines.push('## 一、会议目标')
  lines.push(`- 围绕「${topic}」展开，目的为：${purpose}`)
  lines.push('')
  lines.push('## 二、执行分工')
  items.forEach((it, i) => {
    const r = ROSTER[it.ownerId]
    lines.push(`${i + 1}. **${r.name}（${EXPERT[it.ownerId].competency}）**：任务——${it.title}`)
  })
  lines.push('')
  lines.push('## 三、分工说明')
  items.forEach((it) => {
    const kb = kbOf(it.ownerId)
    lines.push(`- ${nameOf(it.ownerId)} 将基于以下数据源产出「${kb.deliverable}」：${kb.dataSources.join('、')}`)
  })
  return lines.join('\n')
}

function MeetingRoom({ onClose }: { onClose: () => void }) {
  const [step, setStep] = useState<Step>('setup')
  const [topic, setTopic] = useState('')
  const [purpose, setPurpose] = useState('')
  const [suggested, setSuggested] = useState<Array<{ id: string; score: number; hits: string[] }>>([])
  const [invited, setInvited] = useState<string[]>([])
  const [messages, setMessages] = useState<ChatMsg[]>([])
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const [respondingId, setRespondingId] = useState<string | null>(null)
  const [planItems, setPlanItems] = useState<Array<{ ownerId: string; title: string }>>([])
  const [planDoc, setPlanDoc] = useState('')
  const [project, setProject] = useState<LiveProject | null>(null)
  const [executing, setExecuting] = useState(false)
  const [openTask, setOpenTask] = useState<string | null>(null)
  const [cfgOpen, setCfgOpen] = useState(false)
  const [copied, setCopied] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight
  }, [messages, respondingId])

  const ctx = (): MeetingContext => ({ topic, purpose, thread: messages })

  const runSuggest = () => {
    const s = suggestExperts(topic, purpose)
    setSuggested(s)
    setInvited((prev) => Array.from(new Set([...s.map((x) => x.id), ...prev])))
  }

  const toggleInvite = (id: string) =>
    setInvited((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]))

  const startDiscuss = () => {
    if (invited.length === 0) return
    setMessages([{ role: 'user', text: `主题：${topic}\n目的：${purpose}` }])
    setStep('discuss')
  }

  /** 用户发言 → 每位受邀员工依次回应 */
  const sendMessage = async () => {
    const text = draft.trim()
    if (!text || busy) return
    const next = [...messages, { role: 'user' as const, text }]
    setMessages(next)
    setDraft('')
    setBusy(true)
    for (const id of invited) {
      setRespondingId(id)
      const reply = await buildReply(id, { topic, purpose, thread: next }, nameOf)
      setMessages((m) => [...m, { role: id, text: reply }])
      await new Promise((r) => setTimeout(r, 350))
    }
    setRespondingId(null)
    setBusy(false)
  }

  const makePlan = () => {
    const items = buildPlanItems(invited, ctx())
    setPlanItems(items)
    setPlanDoc(buildPlanDoc(topic, purpose, items))
    setStep('plan')
  }

  /** 确认方案 → 生成真实项目并写入工作区存储 */
  const confirmPlan = () => {
    const pid = 'mtg-' + Date.now().toString(36)
    const tasks: ProjectTask[] = planItems.map((it, i) => ({
      id: pid + '-t' + i,
      title: it.title,
      ownerId: it.ownerId,
      status: 'todo',
    }))
    const ownerId = planItems[0]?.ownerId ?? invited[0]
    const proj: LiveProject = {
      id: pid,
      name: topic || '未命名会议项目',
      topic,
      purpose,
      status: '进行中',
      progress: 0,
      ownerId,
      memberIds: Array.from(new Set(planItems.map((p) => p.ownerId))),
      tasks,
      createdAt: Date.now(),
      source: 'meeting',
    }
    addLiveProject(proj)
    setProject(proj)
    setStep('done')
  }

  /** 分派执行：每个任务交由对应员工真做（调 LLM 或规则），实时回写进度与产出 */
  const doExecute = async () => {
    if (!project) return
    setExecuting(true)
    const scene = getOfficeScene()
    for (const t of project.tasks) {
      updateTask(project.id, t.id, { status: 'doing', startedAt: Date.now() })
      scene?.setAgentState(t.ownerId, 'thinking', t.title)
      scene?.pushActivity(`${nameOf(t.ownerId)} 开始执行：${t.title}`, ROSTER[t.ownerId]?.color ?? 0x00d4ff)
      const out = await buildTaskOutput(t.ownerId, t.title, { topic, purpose, thread: messages }, nameOf)
      updateTask(project.id, t.id, { status: 'done', output: out, doneAt: Date.now() })
      scene?.setAgentState(t.ownerId, 'working', '已完成：' + t.title)
      scene?.pushActivity(`${nameOf(t.ownerId)} 交付：${t.title}`, ROSTER[t.ownerId]?.color ?? 0x34c759)
      await new Promise((r) => setTimeout(r, 250))
    }
    setProject({ ...project, status: '已完成' })
    setExecuting(false)
  }

  const copyPlan = async () => {
    try { await navigator.clipboard.writeText(planDoc); setCopied(true); setTimeout(() => setCopied(false), 1600) } catch { /* ignore */ }
  }

  const openProjects = () => {
    window.dispatchEvent(new CustomEvent('office:open-projects'))
    onClose()
  }

  const steps: Array<{ key: Step; label: string; icon: string }> = [
    { key: 'setup', label: '设置', icon: 'i-compass' },
    { key: 'discuss', label: '讨论', icon: 'i-msg' },
    { key: 'plan', label: '规划', icon: 'i-doc' },
    { key: 'done', label: '执行', icon: 'i-zap' },
  ]
  const stepIdx = steps.findIndex((s) => s.key === step)
  const allMembers = AGENT_ROSTER
  const llmOn = isLLMEnabled()

  return (
    <div className="mr-overlay" onClick={onClose}>
      <div className="mr-card" onClick={(e) => e.stopPropagation()}>
        <div className="mr-head">
          <div className="mr-title-row">
            <SvgIcon id="i-meeting" size={18} />
            <h3>会议室</h3>
            <span className="mr-badge">多智能体圆桌 · 开会到交付</span>
            <button className={'mr-gear' + (llmOn ? ' on' : '')} title="大模型设置（BYOK）" onClick={() => setCfgOpen((v) => !v)}>
              <SvgIcon id="i-gear" size={14} />
              <span className="mr-gear-dot" />
            </button>
          </div>
          <button className="dr-close" onClick={onClose} aria-label="关闭会议室">×</button>
        </div>

        {/* LLM 设置面板 */}
        {cfgOpen && <LLMPanel onClose={() => setCfgOpen(false)} />}

        {/* 步骤指示 */}
        <div className="mr-steps">
          {steps.map((s, i) => (
            <div key={s.key} className={'mr-step' + (i === stepIdx ? ' on' : '') + (i < stepIdx ? ' past' : '')}>
              <span className="mr-step-ic"><SvgIcon id={s.icon} size={13} /></span>
              <span>{s.label}</span>
              {i < steps.length - 1 && <span className="mr-step-line" />}
            </div>
          ))}
        </div>

        <div className="mr-body">
          {/* ── 步骤一：设置 ── */}
          {step === 'setup' && (
            <div className="mr-setup">
              <div className="mr-field">
                <label><SvgIcon id="i-target" size={12} /> 本次会议主题</label>
                <input className="mr-input" value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="例如：新品类德国站上市打法" />
              </div>
              <div className="mr-field">
                <label><SvgIcon id="i-compass" size={12} /> 目的 / 想解决什么</label>
                <textarea className="mr-textarea" value={purpose} onChange={(e) => setPurpose(e.target.value)} placeholder="例如：验证概念可行性，并产出可执行的上市方案" rows={3} />
              </div>
              <button className="mr-btn primary" onClick={runSuggest}>
                <SvgIcon id="i-users" size={13} /> 建议拉取员工
              </button>
              {suggested.length > 0 && (
                <div className="mr-suggest">
                  <div className="mr-section-title"><SvgIcon id="i-zap" size={12} /> 智能建议（按主题相关性匹配）</div>
                  <div className="mr-suggest-list">
                    {suggested.map((s) => (
                      <div key={s.id} className={'mr-suggest-item' + (invited.includes(s.id) ? ' on' : '')} onClick={() => toggleInvite(s.id)}>
                        <span className="mr-suggest-dot" style={{ background: colorHex(s.id) }} />
                        <span className="mr-suggest-name">{nameOf(s.id)}</span>
                        <span className="mr-suggest-hit">{s.hits.slice(0, 3).join(' / ')}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              <div className="mr-field" style={{ marginTop: 14 }}>
                <div className="mr-section-title"><SvgIcon id="i-users" size={12} /> 参会成员（点击可增减）</div>
                <div className="mr-members">
                  {allMembers.map((r) => (
                    <button key={r.id} className={'mr-member' + (invited.includes(r.id) ? ' on' : '')}
                      style={invited.includes(r.id) ? { borderColor: colorHex(r.id) } : undefined}
                      onClick={() => toggleInvite(r.id)}>
                      <span className="mr-member-dot" style={{ background: colorHex(r.id) }} />
                      {r.name}
                    </button>
                  ))}
                </div>
              </div>
              <div className="mr-foot">
                <button className="mr-btn primary" disabled={invited.length === 0} onClick={startDiscuss}>
                  进入讨论（已选 {invited.length} 人）
                </button>
              </div>
            </div>
          )}

          {/* ── 步骤二：讨论（多智能体圆桌） ── */}
          {step === 'discuss' && (
            <div className="mr-discuss">
              <div className="mr-chips">
                {invited.map((id) => (
                  <span key={id} className="mr-chip" style={{ borderColor: colorHex(id) }}>
                    <span className="mr-chip-dot" style={{ background: colorHex(id) }} />
                    {nameOf(id)}
                  </span>
                ))}
              </div>
              <div className="mr-thread" ref={scrollRef}>
                {messages.map((m, i) => {
                  if (m.role === 'user') {
                    return (
                      <div key={i} className="mr-msg user">
                        <div className="mr-bubble user"><p>{m.text}</p></div>
                        <span className="mr-msg-name">发起人</span>
                      </div>
                    )
                  }
                  const r = ROSTER[m.role]
                  return (
                    <div key={i} className="mr-msg">
                      <span className="mr-avatar" style={{ background: colorHex(m.role) }}>{r?.name?.[0] ?? '?'}</span>
                      <div className="mr-bubble">
                        <span className="mr-msg-name">{r?.name}</span>
                        <p>{m.text}</p>
                      </div>
                    </div>
                  )
                })}
                {respondingId && (
                  <div className="mr-msg">
                    <span className="mr-avatar" style={{ background: colorHex(respondingId) }}>{ROSTER[respondingId]?.name?.[0]}</span>
                    <div className="mr-bubble">
                      <span className="mr-msg-name">{ROSTER[respondingId]?.name} 正在发言…</span>
                      <div className="mr-typing"><span /><span /><span /></div>
                    </div>
                  </div>
                )}
              </div>
              <div className="mr-compose">
                <textarea className="mr-input" value={draft} rows={2}
                  placeholder={busy ? '员工们正在回应…' : '说点什么，全体员工会基于各自领域回应你'}
                  disabled={busy}
                  onChange={(e) => setDraft(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) sendMessage() }} />
                <button className="mr-btn primary" disabled={busy || !draft.trim()} onClick={sendMessage}>
                  {busy ? '生成中…' : '发送'}
                </button>
              </div>
              <div className="mr-foot">
                <button className="mr-btn primary" disabled={busy} onClick={makePlan}>
                  <SvgIcon id="i-doc" size={13} /> 汇总成执行方案
                </button>
              </div>
            </div>
          )}

          {/* ── 步骤三：规划（任务可改负责人） ── */}
          {step === 'plan' && (
            <div className="mr-plan">
              <div className="mr-section-title"><SvgIcon id="i-sliders" size={12} /> 执行分工（可改负责人 / 任务名）</div>
              <div className="mr-plan-items">
                {planItems.map((it, i) => (
                  <div key={i} className="mr-plan-row">
                    <span className="mr-plan-no">{i + 1}</span>
                    <input className="mr-input sm" value={it.title} onChange={(e) => {
                      const v = [...planItems]; v[i] = { ...v[i], title: e.target.value }; setPlanItems(v)
                    }} />
                    <select className="mr-select" value={it.ownerId} style={{ borderColor: colorHex(it.ownerId) }} onChange={(e) => {
                      const v = [...planItems]; v[i] = { ...v[i], ownerId: e.target.value }; setPlanItems(v)
                    }}>
                      {AGENT_ROSTER.map((r) => <option key={r.id} value={r.id}>{r.name}</option>)}
                    </select>
                  </div>
                ))}
              </div>
              <details className="mr-doc-detail">
                <summary><SvgIcon id="i-doc" size={12} /> 查看方案文档（Markdown）</summary>
                <pre className="mr-plan-doc">{planDoc}</pre>
              </details>
              <div className="mr-foot">
                <button className="mr-btn" onClick={copyPlan}>{copied ? '已复制' : '复制方案'}</button>
                <button className="mr-btn primary" onClick={confirmPlan}>
                  <SvgIcon id="i-zap" size={13} /> 确认并生成项目
                </button>
              </div>
            </div>
          )}

          {/* ── 步骤四：执行（实时产出） ── */}
          {step === 'done' && project && (
            <div className="mr-done">
              <div className="mr-done-badge">
                <SvgIcon id="i-zap" size={20} />
                <span>{executing ? '项目执行中…' : '项目已生成，员工正在交付'}</span>
              </div>
              <div className="mr-progress">
                <div className="mr-progress-track"><div className="mr-progress-fill" style={{ width: project.progress + '%' }} /></div>
                <span className="mr-progress-val">{project.progress}%</span>
              </div>
              <ul className="mr-task-list">
                {project.tasks.map((t) => (
                  <li key={t.id} className={'mr-task' + (t.status === 'done' ? ' done' : t.status === 'doing' ? ' doing' : '')}>
                    <span className="mr-task-dot" style={{ background: colorHex(t.ownerId) }} />
                    <button className="mr-task-main" onClick={() => t.output && setOpenTask(openTask === t.id ? null : t.id)}>
                      <span className="mr-task-name">{t.title}</span>
                      <span className="mr-task-owner">{nameOf(t.ownerId)} · {t.status === 'done' ? '已交付' : t.status === 'doing' ? '执行中' : '待执行'}</span>
                    </button>
                    {t.output && openTask === t.id && (
                      <pre className="mr-task-output">{t.output}</pre>
                    )}
                  </li>
                ))}
              </ul>
              <div className="mr-foot">
                {!executing && project.progress < 100 && (
                  <button className="mr-btn primary" onClick={doExecute}>
                    <SvgIcon id="i-zap" size={13} /> 分派执行
                  </button>
                )}
                <button className="mr-btn" onClick={openProjects}>查看项目看板</button>
                <button className="mr-btn primary" onClick={onClose}>完成</button>
              </div>
              <p className="mr-done-tip">产出会实时回写到「项目」看板，可在左侧栏「项目」随时查看每人进度与交付物。</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

/* ═════════ LLM 设置面板（BYOK） ═════════ */
function LLMPanel({ onClose }: { onClose: () => void }) {
  const [key, setKey] = useState(getLLMConfig().key)
  const [base, setBase] = useState(getLLMConfig().baseURL)
  const [model, setModel] = useState(getLLMConfig().model)
  const [saved, setSaved] = useState(false)
  const enabled = key.trim().length > 0

  const save = () => {
    setLLMConfig({ key: key.trim(), baseURL: base.trim() || 'https://api.openai.com/v1', model: model.trim() || 'gpt-4o-mini' })
    setSaved(true)
    setTimeout(() => setSaved(false), 1600)
  }

  return (
    <div className="mr-cfg">
      <div className="mr-cfg-head">
        <SvgIcon id="i-gear" size={14} />
        <span>大模型设置（BYOK · 仅存本地）</span>
        <button className="dr-close sm" onClick={onClose}>×</button>
      </div>
      <div className="mr-cfg-status" data-on={enabled}>{enabled ? '● 已接入大模型：员工将真实生成内容' : '○ 未接入：使用规则引擎（占位产出）'}</div>
      <div className="mr-field">
        <label>API Key</label>
        <input className="mr-input" type="password" value={key} onChange={(e) => setKey(e.target.value)} placeholder="sk-..." />
      </div>
      <div className="mr-field">
        <label>Base URL（OpenAI 兼容）</label>
        <input className="mr-input" value={base} onChange={(e) => setBase(e.target.value)} placeholder="https://api.openai.com/v1" />
      </div>
      <div className="mr-field">
        <label>模型名</label>
        <input className="mr-input" value={model} onChange={(e) => setModel(e.target.value)} placeholder="gpt-4o-mini" />
      </div>
      <p className="mr-cfg-tip">密钥只保存在你浏览器 localStorage，绝不上传仓库。填好保存后，会议室发言与任务产出会自动切换为真实大模型生成。</p>
      <button className="mr-btn primary" onClick={save}>{saved ? '已保存' : '保存'}</button>
    </div>
  )
}

export function OfficeMeetingRoom({ onClose }: { onClose: () => void }) {
  return createPortal(<MeetingRoom onClose={onClose} />, document.body)
}
