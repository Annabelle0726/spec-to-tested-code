"""Build editable artwork; export the generated SVG/HTML with a browser."""
from pathlib import Path
from html import escape

SOURCE = Path(__file__).resolve().parent
ASSETS = SOURCE.parent
PAPER, INK, BLUE, GOLD = '#f3f0e7', '#172941', '#31588c', '#c9a665'
MUTED = '#637183'

def text(x,y,s,size=24,fill=INK,font='Arial,Microsoft YaHei,sans-serif',weight=400,extra=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="{font}" font-size="{size}" font-weight="{weight}" {extra}>{escape(s)}</text>'

def box(x,y,w,h,fill,stroke='none',radius=2,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" {extra}/>'

def line(x,y,x2,y2,fill=GOLD,extra=''):
    return f'<path d="M{x} {y} L{x2} {y2}" fill="none" stroke="{fill}" {extra}/>'

defs='''<defs>
<filter id="shadow" x="-20%" y="-25%" width="150%" height="175%"><feDropShadow dx="0" dy="12" stdDeviation="11" flood-color="#122139" flood-opacity=".16"/></filter>
<linearGradient id="sheet" x2=".9" y2="1"><stop stop-color="#fffdf8"/><stop offset="1" stop-color="#eee9de"/></linearGradient>
<linearGradient id="dark" x2="1" y2="1"><stop stop-color="#1c3555"/><stop offset="1" stop-color="#101f33"/></linearGradient>
<linearGradient id="gold" x2="1" y2=".4"><stop stop-color="#ecdbb5"/><stop offset=".45" stop-color="#f6e9c8"/><stop offset="1" stop-color="#d5ba7f"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="#b4c8e3" stroke-opacity=".06" fill="none"/></pattern>
<pattern id="grain" width="8" height="9" patternUnits="userSpaceOnUse"><circle cx="1" cy="2" r=".5" fill="#685c41" opacity=".09"/><path d="M5 7h2" stroke="#fff" stroke-opacity=".4" stroke-width=".6"/></pattern>
</defs>'''

def svg(name,s,width,height):
    path=ASSETS/name
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="label"><title id="label">{name.removesuffix(".svg")}</title>{defs}{s}</svg>',encoding='utf8')

# The generated material study is a background only. All exact typography is editable.
overlay=box(70,67,25,30,'none',BLUE,1)+box(75,62,25,30,'none',BLUE,1)
overlay+=line(80,72,92,72,GOLD)+line(80,77,92,77,GOLD)
overlay+=text(122,88,'spec-to-tested-code',23,BLUE,'Consolas,monospace',600)
overlay+=text(870,85,'THE DELIVERY FIELD GUIDE',12,MUTED,'Consolas,monospace',extra='text-anchor="end" letter-spacing="1.8"')
overlay+=line(70,121,873,121,'#b7b3a7',extra='stroke-opacity=".65"')
overlay+=text(68,299,'Spec to Tested Code',87,INK,'Georgia,serif',extra='letter-spacing="-3"')
overlay+=text(72,374,'From intent to verified delivery.',34,BLUE,'Georgia,serif',extra='font-style="italic"')
overlay+=text(74,457,'把业务约定，变成经得起验证的实现。',29,INK,weight=500)
overlay+=text(74,506,'需求澄清  /  行为场景  /  测试实现  /  验证交付',20,MUTED)
overlay+=line(72,653,873,653,'#b7b3a7',extra='stroke-opacity=".65"')
for x,n,label in [(74,'01','SPECIFY'),(350,'02','EXEMPLIFY'),(626,'03','VERIFY')]:
    overlay+=text(x,701,n,14,BLUE,'Consolas,monospace',600)+text(x+35,701,label,14,INK,'Consolas,monospace',extra='letter-spacing="2"')
overlay+=text(74,751,'One shared definition of done.',21,MUTED,'Georgia,serif',extra='font-style="italic"')
for x,y,n,code,label in [(1350,132,'01','SDD','SPECIFICATION'),(1250,303,'02','BDD','SCENARIOS'),(1146,478,'03','TDD','TESTS')]:
    overlay+=f'<g transform="matrix(.96 .17 -.35 .94 {x} {y})">'
    overlay+=text(0,0,n+' / FIELD NOTES',11,BLUE,'Consolas,monospace',600,extra='letter-spacing="1.5"')
    overlay+=text(0,53,code,44,INK,'Georgia,serif')
    overlay+=line(0,68,178,68,'#9d8a61',extra='stroke-width=".7"')
    overlay+=text(0,91,label,10,BLUE,'Consolas,monospace',extra='letter-spacing="2"')+'</g>'

cover=f'''<!doctype html><html><head><meta charset="utf-8"><title>Delivery field guide cover</title><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1800px;height:800px;overflow:hidden}}main{{position:relative;width:1800px;height:800px}}img,svg{{position:absolute;inset:0;width:1800px;height:800px}}img{{object-fit:fill}}</style></head><body><main><img src="folio-art.png" alt="Tactile ivory field guides on navy drafting paper"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 800">{overlay}</svg></main></body></html>'''
(SOURCE/'cover-layout.html').write_text(cover,encoding='utf8')

def backdrop(width,height,dark=False):
    s=box(0,0,width,height,'url(#dark)' if dark else PAPER)
    s+=box(0,0,width,height,'url(#grid)' if dark else 'url(#grain)')
    return s

def folio(x,y,w,h,fill,rotation=0):
    return f'<g transform="rotate({rotation} {x+w/2} {y+h/2})">'+box(x+4,y+8,w,h,'#d1c8b5')+box(x+2,y+4,w,h,'#f3eee0',stroke='#bdb5a5')+box(x,y,w,h,fill,stroke='#d1c9b8',extra='filter="url(#shadow)"')

def chapter_top(n,caption,x,y,w):
    return text(x,y,n,20,BLUE,'Consolas,monospace',600)+text(x+w,y,caption,12,MUTED,'Consolas,monospace',extra='text-anchor="end" letter-spacing="1.5"')+line(x,y+20,x+w,y+20,'#d4ccbb')

entries=[('01','DISCOVERY','需求还模糊',['已确认规则','验收场景','待决问题'],-1.5),('02','IMPLEMENTATION','规则已确认',['有效的失败测试','最小实现','受保护的重构'],0),('03','DIAGNOSIS','出现了缺陷',['最小复现','有证据的根因','回归验证'],1.5)]
s=backdrop(1440,660)
s+=text(58,55,'THE FIELD GUIDE / CHOOSE YOUR ENTRY',13,BLUE,'Consolas,monospace',extra='letter-spacing="2"')
s+=text(57,124,'从你现在的位置开始。',48,INK,weight=600)
s+=text(1380,113,'01 — 03',18,BLUE,'Consolas,monospace',extra='text-anchor="end"')
for i,(n,caption,title,rows,angle) in enumerate(entries):
    x=64+i*455
    s+=folio(x,195,404,348,'url(#sheet)',angle)
    s+=box(x+280,185,90,27,GOLD if i==2 else INK,1)
    s+=text(x+325,204,caption[:4],10,PAPER,'Consolas,monospace',extra='text-anchor="middle" letter-spacing="2"')
    s+=chapter_top(n,caption,x+28,235,348)
    s+=text(x+28,299,title,32,INK,weight=600)
    for j,row in enumerate(rows):
        yy=355+j*52
        s+=text(x+28,yy,chr(97+j)+'.',15,BLUE,'Georgia,serif',extra='font-style="italic"')+text(x+62,yy,row,25,INK)
        s+=line(x+62,yy+15,x+374,yy+15,'#dad3c4')
    s+='</g>'
s+=line(60,588,1380,588,'#bcb6a9')
s+=text(61,623,'只做规格，就停在规格；已授权实现，就继续到验证。',21,MUTED)
s+=text(1380,624,'START WHERE THE WORK IS.',12,BLUE,'Consolas,monospace',extra='text-anchor="end" letter-spacing="1.5"')
svg('entry-points.svg',s,1440,660)

s=backdrop(1440,660,True)
for radius in [180,260,340]:s+=f'<circle cx="1440" cy="0" r="{radius}" fill="none" stroke="#b2c0d7" stroke-opacity=".08"/>'
s+=text(58,55,'THE EVIDENCE / ONE SHARED AGREEMENT',13,'#dec58e','Consolas,monospace',extra='letter-spacing="2"')
s+=text(57,124,'同一条约定，贯穿场景与验证。',48,PAPER,weight=600)
cards=[(64,'R1','CONFIRMED RULE','已确认规则',['本人可取消未发货订单。','成功后状态变为已取消。'],'url(#sheet)',-1.2),(519,'S1 / R1','BEHAVIOR SCENARIO','具体场景',['甲取消自己的未发货订单。','重新读取时，状态为已取消。'],'url(#sheet)',0),(974,'T1 / S1','VERIFICATION','验证要点',['核对返回结果与最终状态。','未执行的检查如实标明。'],'url(#gold)',1.2)]
for x,n,caption,title,rows,fill,angle in cards:
    s+=folio(x,195,404,348,fill,angle)
    s+=chapter_top(n,caption,x+28,235,348)
    s+=text(x+28,308,title,33,INK,weight=600)
    for j,row in enumerate(rows):s+=text(x+28,370+j*43,row,23,INK)
    s+=line(x+28,464,x+376,464,'#b7aa8c')
    s+=text(x+28,502,{'R1':'AGREEMENT','S1 / R1':'OBSERVABLE BEHAVIOR','T1 / S1':'EXECUTION EVIDENCE'}[n],12,BLUE,'Consolas,monospace',extra='letter-spacing="1.4"')+'</g>'
s+=line(60,588,1380,588,'#4b5b71')+text(61,624,'场景示意 · 说明工作方法，非已执行测试记录。',18,'#b6c2d4')+text(1380,624,'TRACE THE SAME RULE.',12,'#dec58e','Consolas,monospace',extra='text-anchor="end" letter-spacing="1.5"')
svg('rule-to-evidence.svg',s,1440,660)

# Narrow-screen editions preserve the visual system and increase label size.
for kind in ['entry-points','rule-to-evidence']:
    dark=kind=='rule-to-evidence'
    s=backdrop(720,1040,dark)
    s+=text(36,47,'THE EVIDENCE' if dark else 'THE FIELD GUIDE',14,'#dec58e' if dark else BLUE,'Consolas,monospace',extra='letter-spacing="2"')
    s+=text(34,109,'同一条约定，贯穿验证。' if dark else '从你现在的位置开始。',35,PAPER if dark else INK,weight=600)
    for i in range(3):
        yy=165+i*266
        if dark:
            _,n,caption,title,rows,fill,_=cards[i]
        else:
            n,caption,title,rows,_=entries[i];fill='url(#sheet)'
        s+=folio(37,yy,646,232,fill,0)
        s+=text(63,yy+42,n,18,BLUE,'Consolas,monospace',600)+text(657,yy+42,caption,12,MUTED,'Consolas,monospace',extra='text-anchor="end"')
        s+=line(63,yy+60,657,yy+60,'#d0c6b3')
        s+=text(63,yy+114,title,32,INK,weight=600)
        if dark:
            for j,row in enumerate(rows):s+=text(63,yy+158+j*37,row,25,INK)
        else:
            s+=text(63,yy+164,' / '.join(rows[:2]),24,INK)+text(63,yy+202,rows[2],24,INK)
        s+='</g>'
    s+=text(36,1011,'方法示意，非执行记录。' if dark else '只做规格时停在规格，已授权实现时继续推进。',17,'#bdc8d6' if dark else MUTED)
    svg(kind+'-mobile.svg',s,720,1040)

print('Built cover layout, 2 desktop diagrams, and 2 mobile diagrams.')
