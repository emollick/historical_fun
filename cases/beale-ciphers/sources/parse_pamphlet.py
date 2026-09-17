import re, html, json, os
S=os.environ.get('S','.')
OUT=os.path.join(S,'data')
pages=[]
for i in range(1,24):
    t=open(f'ws_page_{i}.txt',encoding='utf-8').read()
    t=re.sub(r'<noinclude>.*?</noinclude>','',t,flags=re.S)
    # hyphenated words across pages: keep full word at hws, drop hwe
    t=re.sub(r'\{\{hws\|[^|}]*\|([^|}]*)\}\}',r'\1',t)
    t=re.sub(r'\{\{hwe\|[^|}]*\|([^|}]*)\}\}','',t)
    # dual numbering of first ten DOI words: {{dual|n|word|...}} -> word (n)
    t=re.sub(r'\{\{dual\|(\d+)\|([^|}]*)(?:\|[^}]*)?\}\}',r'\2 (\1)',t)
    t=re.sub(r'\{\{anchor\|[^}]*\}\}','',t)
    t=re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]',r'\1',t)
    t=re.sub(r'\[\[([^\]]*)\]\]',r'\1',t)
    for _ in range(8):
        t=re.sub(r'\{\{(?:sc|di|bl|c|center|right|left|larger|x-larger|xx-larger|xxx-larger|xxxx-larger|smaller|x-smaller|smaller block|x-smaller block|center block|border|uc|em|italic)\|((?:[^{}]|\{\{[^{}]*\}\})*)\}\}',r'\1',t,flags=re.S)
    t=re.sub(r'\{\{[^{}]*\}\}','',t)
    t=re.sub(r'<[^>]+>','',t)
    t=t.replace("''","")
    t=html.unescape(t)
    pages.append(t)
full='\n'.join(pages)
full=re.sub(r'[ \t]+\n','\n',full)
full=re.sub(r'\n{3,}','\n\n',full)
open(os.path.join(OUT,'beale_papers_1885.txt'),'w',encoding='utf-8').write(full)

def between(a,b,text=full):
    i=text.index(a); j=text.index(b,i+len(a))
    return text[i:j]

# --- ciphers
def nums(s):
    return [int(x) for x in re.findall(r'\d+',s)]
c2_block=between('marked “2,” which is fully explained by the foregoing document, is as follows.','By comparing the foregoing numbers')
# FIX: between() returns the text INCLUDING the start string, whose
# “2,” was being swept up by nums() as a spurious first cipher number; drop the delimiter text.
c2_block=c2_block[len('marked “2,” which is fully explained by the foregoing document, is as follows.'):]
c1_block=between('THE LOCALITY OF THE VAULT','The following paper is marked “3”')
c3_block=between('NAMES AND RESIDENCES.','The papers given above were all')
C1,C2,C3=nums(c1_block),nums(c2_block),nums(c3_block)
for name,c in [('cipher1',C1),('cipher2',C2),('cipher3',C3)]:
    open(os.path.join(OUT,name+'.txt'),'w').write(' '.join(map(str,c))+'\n')
    print(name,len(c),'numbers; max',max(c),'min',min(c),'distinct',len(set(c)))

# --- DOI as printed in the pamphlet (with its parenthetical numbering)
doi=between('When, (1)','The letter, or paper, so often alluded to')
doi=doi.strip()
open(os.path.join(OUT,'doi_pamphlet_as_printed.txt'),'w',encoding='utf-8').write(doi+'\n')
# --- B2 plaintext as printed
p2=between('the translation will be found to be as follows:','The following is the paper which, according to Beale')
p2=p2.strip()
open(os.path.join(OUT,'b2_plaintext_as_printed.txt'),'w',encoding='utf-8').write(p2+'\n')
print('B2 plaintext letters:',len(re.sub(r'[^A-Za-z]','',p2)))
# --- letters
L1=between('Lynchburg, January 4th, 1822.','Lynchburg, Va, January 5th, 1822.')
L2=between('Lynchburg, Va, January 5th, 1822.','The two letters given above')
L3=between('St. Louis, Mo., May 9th, 1822.','After the reception of this letter')
for name,txt in [('letter_1822-01-04',L1),('letter_1822-01-05',L2),('letter_1822-05-09',L3)]:
    open(os.path.join(OUT,name+'.txt'),'w',encoding='utf-8').write(txt.strip()+'\n')
    print(name,len(txt.split()),'words')
# --- Morriss's quoted statement (between the opening quote of his account and its end)
mor=between('“It was in the month of January, 1820','After the reception of this letter')
# the Morriss quotation ends before "The following is the letter addressed to Mr. Morriss by Beale"
mor=mor[:mor.index('The following is the letter addressed to Mr. Morriss by Beale')]
open(os.path.join(OUT,'morriss_statement.txt'),'w',encoding='utf-8').write(mor.strip()+'\n')
print('morriss statement',len(mor.split()),'words')
# --- Ward/anonymous narrative: everything else in prose
narr=full
for chunk in [c1_block,c2_block,c3_block,doi,p2,L1,L2,L3,mor]:
    narr=narr.replace(chunk,'\n')
narr=narr[narr.index('THE following details'):]
narr=narr[:narr.index('It is needless to say that I shall await with much anxiety the development of the mystery.')+len('It is needless to say that I shall await with much anxiety the development of the mystery.')]
narr=re.sub(r'\n{3,}','\n\n',narr)
open(os.path.join(OUT,'narrative_anonymous_author.txt'),'w',encoding='utf-8').write(narr.strip()+'\n')
print('narrative',len(narr.split()),'words')
