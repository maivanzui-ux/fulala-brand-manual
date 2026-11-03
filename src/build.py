"""Build index.html from src/. Run: python3 src/build.py"""
import re,os,shutil,sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
t=open("template.html").read()
t=t.replace("  </div></main>",open("ds.html").read()+"\n  </div></main>",1)
t=t.replace("@media (prefers-reduced-motion:reduce)",open("ds.css").read()+"\n@media (prefers-reduced-motion:reduce)",1)
t=t.replace('renderDlp();\n</script>',open("ds.js").read()+'\nrenderDlp();\n</script>',1)
t=t.replace(' {id:"ilustrace",t:"Ilustrace",s:[["il-tygr","Tygr s knedlíčkem"],["il-hlava","Hlava tygra"],["il-knedlik","Knedlíček"],["il-hulky","Hůlky"],["il-knedhul","Knedlíček a hůlky"],["il-nudle","Nudle"],["il-nudhul","Nudle s hůlkami"],["il-pouziti","Použití"],["il-stazeni","Ke stažení"]]}',
 ' {id:"ilustrace",t:"Ilustrace",s:[["il-tygr","Tygr s knedlíčkem"],["il-hlava","Hlava tygra"],["il-knedlik","Knedlíček"],["il-hulky","Hůlky"],["il-knedhul","Knedlíček a hůlky"],["il-nudle","Nudle"],["il-nudhul","Nudle s hůlkami"],["il-pouziti","Použití"],["il-stazeni","Ke stažení"]]},\n {id:"system",t:"Design systém",s:[["ds-barvy","Barevné tokeny"],["ds-rozmery","Mezery a zaoblení"],["ds-tlacitka","Tlačítka"],["ds-formulare","Formulářová pole"],["ds-stitky","Štítky"],["ds-karta","Karta jídla"],["ds-stazeni","Ke stažení"]]}')
t=t.replace('<div class="next"><a href="#uvod"><span>Zpět na začátek</span><b>Úvod →</b></a></div>\n  </article>\n\n  <!-- ============ DESIGN','<div class="next"><a href="#system"><span>Další kapitola</span><b>Design systém →</b></a></div>\n  </article>\n\n  <!-- ============ DESIGN',1)
syms="";vbs={}
for name,sid in [("logo","logo"),("tiger","tiger"),("chopsticks","chop"),("tigercin","tigercin"),("chopcin","chopcin"),("knedlik","kned"),("knedlikcin","knedcin"),("knedlikblack","knedblack"),("knedhul","knedhul"),("knedhulcin","knedhulcin"),("knedhulblack","knedhulblack"),("noodles","nood"),("noodlescin","noodcin"),("noodlesblack","noodblack"),("noodhul","noodhul"),("noodhulcin","noodhulcin"),("noodhulblack","noodhulblack")]:
    s=open(name+".svg.part").read()
    vb=re.search(r'viewBox="([^"]+)"',s).group(1); vbs[sid]=vb
    syms+=f'<symbol id="{sid}" viewBox="{vb}">{re.sub(r"^<svg[^>]*>","",s)[:-6]}</symbol>\n'
# symbol (tiger head): src/symbol.svg.part + src/symbolcin.svg.part once the artwork exists, a placeholder until then
for name,sid in [("symbol","sym"),("symbolcin","symcin")]:
    if os.path.exists(name+".svg.part"):
        s=open(name+".svg.part").read();vb=re.search(r'viewBox="([^"]+)"',s).group(1)
        syms+=f'<symbol id="{sid}" viewBox="{vb}">{re.sub(r"^<svg[^>]*>","",s)[:-6]}</symbol>\n'
    else:
        vb="0 0 100 100"
        syms+=f'<symbol id="{sid}" viewBox="{vb}"><circle cx="50" cy="50" r="46" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="8 6"/><text x="50" y="62" text-anchor="middle" font-size="36" font-family="sans-serif" fill="currentColor">?</text></symbol>\n'
    vbs[sid]=vb
# don't-example: the logo letters pulled apart (paths in the order F, A, L, A, L, U)
s=open("logo.svg.part").read();x0,y0,w,h=map(float,re.search(r'viewBox="([^"]+)"',s).group(1).split())
GAP=55;order=[0,3,2,5,4,1]
paths=re.findall(r'<path[^>]*/>',s)
syms+=f'<symbol id="logosplit" viewBox="{x0:g} {y0:g} {w+5*GAP:g} {h:g}">'+"".join(f'<g transform="translate({order[i]*GAP} 0)">{p}</g>' for i,p in enumerate(paths))+"</symbol>\n"
vbs["logosplit"]=f"{x0:g} {y0:g} {w+5*GAP:g} {h:g}"
z=lambda v:"0 0 "+" ".join(v.split()[2:])
import json as _j,subprocess
subprocess.run([sys.executable,"assets.py"],check=True,stdout=subprocess.DEVNULL)
sizes={os.path.relpath(os.path.join(r,f),".."):os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk("../files") for f in fs}
t=t.replace("{{SIZES}}",_j.dumps(sizes))
t=t.replace("{{SYMBOLS}}",syms).replace("{{LOGO_VB}}",z(vbs["logo"])).replace("{{TIGER_VB}}",z(vbs["tiger"])).replace("{{CHOP_VB}}",z(vbs["chop"])).replace("{{TIGERCIN_VB}}",z(vbs["tigercin"])).replace("{{CHOPCIN_VB}}",z(vbs["chopcin"])).replace("{{SYM_VB}}",z(vbs["sym"])).replace("{{LOGOSPLIT_VB}}",z(vbs["logosplit"])).replace("{{KNED_VB}}",z(vbs["kned"])).replace("{{KNEDCIN_VB}}",z(vbs["knedcin"])).replace("{{KNEDBLACK_VB}}",z(vbs["knedblack"])).replace("{{KNEDHUL_VB}}",z(vbs["knedhul"])).replace("{{KNEDHULCIN_VB}}",z(vbs["knedhulcin"])).replace("{{KNEDHULBLACK_VB}}",z(vbs["knedhulblack"])).replace("{{NOOD_VB}}",z(vbs["nood"])).replace("{{NOODCIN_VB}}",z(vbs["noodcin"])).replace("{{NOODBLACK_VB}}",z(vbs["noodblack"])).replace("{{NOODHUL_VB}}",z(vbs["noodhul"])).replace("{{NOODHULCIN_VB}}",z(vbs["noodhulcin"])).replace("{{NOODHULBLACK_VB}}",z(vbs["noodhulblack"])).replace("{{SYMCIN_VB}}",z(vbs["symcin"]))
t=t.replace(',"V podkladu chybně uveden kód #ffdab9. Hodnota je odečtená ze vzorku, potvrdit."','')

t=t.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
i=t.index("</style>")+len("</style>")
html='<!doctype html>\n<html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+t[:i].replace("<style>","<style>\nbody{margin:0}img{max-width:100%}[hidden]{display:none!important}\n",1)+"\n</head><body>"+t[i:]+"\n</body></html>\n"
import json,importlib.util
sp=importlib.util.spec_from_file_location('en','en.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
html=html.replace('{{EN}}',json.dumps(m.EN,ensure_ascii=False)).replace('\n</script>','\napplyLang();\n</script>')
open("../index.html","w").write(html)
