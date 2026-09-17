#!/usr/bin/env python3
import sys,re,html,urllib.parse,urllib.request
q=sys.argv[1]; maxr=sys.argv[2] if len(sys.argv)>2 else '50'
url="https://jsru.kb.nl/sru/sru?operation=searchRetrieve&x-collection=DDD_artikel&maximumRecords=%s&recordSchema=ddd&query=%s"%(maxr,urllib.parse.quote(q))
s=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=90).read().decode('utf-8','ignore')
n=re.search(r'<srw:numberOfRecords>(\d+)',s); print('QUERY',q,'->',n.group(1) if n else '?')
for r in re.findall(r'<srw:record>(.*?)</srw:record>',s,flags=re.S):
    def g(tag):
        m=re.search(r'<(?:dc:|ddd:)?%s[^>]*>(.*?)</'%tag,r,flags=re.S); return html.unescape(m.group(1)).strip() if m else ''
    print('---',g('date')[:10],'|',g('papertitle'),'|',g('title')[:150],'|',g('identifier'))
