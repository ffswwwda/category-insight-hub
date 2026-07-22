/** 会议引擎：多智能体发言 / 任务规划 / 任务产出
 *  统一策略：LLM 优先（BYOK），任何失败/无密钥都回退到规则引擎。
 *  保证「当下无密钥也能跑通完整产品」，接入密钥后自动升级为真实生成。
 */
import { chatOnce } from '@/lib/llm'
import { kbOf } from '@/lib/employeeKB'
import { isLLMEnabled } from '@/store/workspaceStore'

export interface ChatMsg {
  role: 'user' | string // 'user' 或员工 id
  text: string
}

export interface MeetingContext {
  topic: string
  purpose: string
  thread: ChatMsg[]
}

/** 把会话线程压缩成给 LLM 的上下文文本 */
function threadToText(thread: ChatMsg[], nameOf: (id: string) => string): string {
  const tail = thread.slice(-8)
  return tail.map((m) => (m.role === 'user' ? '发起人：' + m.text : nameOf(m.role) + '：' + m.text)).join('\n')
}

/* ───────── 1. 多智能体发言（圆桌讨论） ───────── */
export async function buildReply(id: string, ctx: MeetingContext, nameOf: (id: string) => string): Promise<string> {
  const kb = kbOf(id)
  const userMsgs = ctx.thread.filter((m) => m.role === 'user')
  const latest = userMsgs[userMsgs.length - 1]?.text ?? ctx.purpose

  if (isLLMEnabled()) {
    try {
      const sys = `${kb.systemPrompt}\n你现在参加一个多智能体圆桌会议，其他同事和发起人都在场。请基于你的领域知识，对发起人的最新发言给出你的专业看法：指出关键风险、补充被忽略的角度、给出可落地的建议。用第一人称、口语化、2-4 句，不要寒暄标题，直接说观点。`
      const user = `会议主题：${ctx.topic}\n会议目的：${ctx.purpose}\n\n近期讨论：\n${threadToText(ctx.thread, nameOf)}\n\n发起人最新说：${latest}\n\n请给出你的看法：`
      const out = await chatOnce(sys, user, { temperature: 0.8 })
      if (out && out.trim().length > 0) return out.trim()
    } catch { /* 回退规则 */ }
  }
  return ruleReply(id, ctx, latest)
}

function ruleReply(id: string, ctx: MeetingContext, latest: string): string {
  const kb = kbOf(id)
  const text = (latest + ' ' + ctx.topic + ' ' + ctx.purpose).toLowerCase()
  const hit = kb.dataSources.some((d) => text.includes(d.toLowerCase().split(' ')[0].slice(0, 2)))
  const riskWord = /风险|不确定|担心|可能|存疑|隐患|翻车/.test(ctx.purpose + latest)
  const lead = riskWord ? `我比较谨慎——「${ctx.topic}」里我看到的隐患是：` : `关于「${ctx.topic}」，我的角度是这样的：`
  const body = `我手上的${kb.dataSources[0] ?? '领域数据'}能支撑这块。建议你先落到「${kb.deliverable}」上，证据足了再扩大。`
  const tail = hit ? '这一块我有现成的方法，可以直接接。' : '不过这块如果缺数据，结论要先打问号。'
  return lead + body + tail
}

/* ───────── 2. 规划：每位员工提议自己要认领的任务 ───────── */
export function buildPlanItems(invited: string[], ctx: MeetingContext): Array<{ ownerId: string; title: string }> {
  return invited.map((id) => {
    const kb = kbOf(id)
    const topic = ctx.topic || '本次会议主题'
    const titleMap: Record<string, string> = {
      voc: `产出「${topic}」相关 VOC 标签分布与用户痛点摘要`,
      score: `对「${topic}」概念做四维评分并附证据`,
      lab: `对「${topic}」做数字世界多场景策略推演`,
      dev: `围绕「${topic}」生成产品开发方向与 FABE 文案`,
      idea: `为「${topic}」产出创意图与视觉概念`,
      stress: `对「${topic}」方案做虚拟用户压力测试`,
      pr: `将「${topic}」相关表达做多市场地道本地化`,
    }
    return { ownerId: id, title: titleMap[id] ?? `负责「${topic}」的${kb.role}` }
  })
}

/* ───────── 3. 任务产出（执行阶段的交付物） ───────── */
export async function buildTaskOutput(id: string, title: string, ctx: MeetingContext, nameOf: (id: string) => string): Promise<string> {
  const kb = kbOf(id)
  if (isLLMEnabled()) {
    try {
      const sys = `${kb.systemPrompt}\n你是会议中被分派执行任务的一员。请直接产出你这个任务的交付物内容（用 Markdown，中文，具体可落地，含关键要点与可执行的下一步），不要寒暄、不要加标题之外的客套。`
      const user = `会议主题：${ctx.topic}\n会议目的：${ctx.purpose}\n\n你的任务：${title}\n\n可接入的数据源：${kb.dataSources.join('、')}\n期望交付物：${kb.deliverable}\n\n请产出交付物正文：`
      const out = await chatOnce(sys, user, { temperature: 0.6 })
      if (out && out.trim().length > 0) return out.trim()
    } catch { /* 回退规则 */ }
  }
  return ruleTaskOutput(id, title, ctx)
}

function ruleTaskOutput(id: string, title: string, ctx: MeetingContext): string {
  const kb = kbOf(id)
  const topic = ctx.topic || '本次会议主题'
  const lines: string[] = []
  lines.push(`# ${title}`)
  lines.push('')
  lines.push(`> 负责人：${kb.name}（${kb.role}）`)
  lines.push(`> 会议主题：${topic}`)
  lines.push('')
  lines.push('## 一、依据的数据源')
  kb.dataSources.forEach((d) => lines.push(`- ${d}`))
  lines.push('')
  lines.push('## 二、关键要点')
  lines.push(`- 围绕「${topic}」，从${kb.role}视角，优先确认最核心的 2-3 个判断依据。`)
  lines.push(`- 用${kb.dataSources[0] ?? '领域数据'}做证据底座，避免平均意见稀释。`)
  lines.push(`- 输出形态对齐预期交付物：${kb.deliverable}。`)
  lines.push('')
  lines.push('## 三、下一步')
  lines.push(`- 将以上要点沉淀为可交付的「${kb.deliverable}」，并标注数据缺口。`)
  lines.push('')
  lines.push('> 说明：当前为规则引擎生成的占位交付物（未接入大模型）。在会议室设置中填入 API Key 后，这里会自动替换为该员工基于真实知识库生成的实质内容。')
  return lines.join('\n')
}
