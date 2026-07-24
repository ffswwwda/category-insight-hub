import json, io

HEAD = open('/Users/fsw/WorkBuddy/2026-07-15-08-51-27/tpl_head.html', encoding='utf-8').read()
TAIL = open('/Users/fsw/WorkBuddy/2026-07-15-08-51-27/tpl_tail.html', encoding='utf-8').read()
DATA = open('/Users/fsw/WorkBuddy/2026-07-15-08-51-27/sales_data_new.json', encoding='utf-8').read()

OUT = '/Users/fsw/WorkBuddy/2026-07-15-08-51-27/vendor/product-sales.html'

# Inject SALES_DATA between head and tail
data_js = "var SALES_DATA = " + DATA + ";\n"

html = HEAD + "\n<script>\n" + data_js + "</script>\n" + TAIL

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

print("WROTE", OUT, "bytes=", len(html.encode('utf-8')))
