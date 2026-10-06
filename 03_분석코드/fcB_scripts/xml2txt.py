import re,html,sys
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=re.sub(r'<xref[^>]*>(.*?)</xref>',r'[\1]',s,flags=re.S)
t=re.sub(r'</(p|title|sec|caption|td|tr)>','\n',t)
t=re.sub(r'<[^>]+>','',t)
t=html.unescape(t)
t=re.sub(r'\n\s*\n+','\n',t)
open(sys.argv[2],'w').write(t)
