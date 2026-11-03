"""Build index.html from src/. Run: python3 src/build.py"""
import re,os,shutil,sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
t=open("template.html").read()
t=t.replace("  </div></main>",open("ds.html").read()+"\n  </div></main>",1)
t=t.replace("@media (prefers-reduced-motion:reduce)",open("ds.css").read()+"\n@media (prefers-reduced-motion:reduce)",1)
t=t.replace('document.querySelectorAll("[data-dl]")',open("ds.js").read()+'\ndocument.querySelectorAll("[data-dl]")',1)
t=t.replace(' {id:"ilustrace",t:"Ilustrace",s:[["il-tygr","Tygr s knedlíčkem"],["il-hulky","Hůlky"],["il-pouziti","Použití"],["il-stazeni","Ke stažení"]]}',
 ' {id:"ilustrace",t:"Ilustrace",s:[["il-tygr","Tygr s knedlíčkem"],["il-hulky","Hůlky"],["il-pouziti","Použití"],["il-stazeni","Ke stažení"]]},\n {id:"system",t:"Design systém",s:[["ds-barvy","Barevné tokeny"],["ds-rozmery","Mezery a zaoblení"],["ds-tlacitka","Tlačítka"],["ds-formulare","Formulářová pole"],["ds-stitky","Štítky"],["ds-karta","Karta jídla"],["ds-stazeni","Ke stažení"]]}')
t=t.replace('<div class="next"><a href="#uvod"><span>Zpět na začátek</span><b>Úvod →</b></a></div>\n  </article>\n\n  <!-- ============ DESIGN','<div class="next"><a href="#system"><span>Další kapitola</span><b>Design systém →</b></a></div>\n  </article>\n\n  <!-- ============ DESIGN',1)
syms="";vbs={}
for name,sid in [("logo","logo"),("tiger","tiger"),("chopsticks","chop"),("tigercin","tigercin"),("chopcin","chopcin")]:
    s=open(name+".svg.part").read()
    vb=re.search(r'viewBox="([^"]+)"',s).group(1); vbs[sid]=vb
    syms+=f'<symbol id="{sid}" viewBox="{vb}">{re.sub(r"^<svg[^>]*>","",s)[:-6]}</symbol>\n'
z=lambda v:"0 0 "+" ".join(v.split()[2:])
t=t.replace("{{SYMBOLS}}",syms).replace("{{LOGO_VB}}",z(vbs["logo"])).replace("{{TIGER_VB}}",z(vbs["tiger"])).replace("{{CHOP_VB}}",z(vbs["chop"])).replace("{{TIGERCIN_VB}}",z(vbs["tigercin"])).replace("{{CHOPCIN_VB}}",z(vbs["chopcin"]))
t=t.replace(',"V podkladu chybně uveden kód #ffdab9. Hodnota je odečtená ze vzorku, potvrdit."','')
start=t.index("let downloads;"); end=t.index("</script>")
t=t[:start]+'''document.addEventListener("click",e=>{
  const b=e.target.closest("button.dlb");if(!b)return;
  const st=b.closest("section").querySelector(".status");
  const [,,name,src]=DL[b.dataset.g][+b.dataset.i];
  const a=document.createElement("a");a.download=name;
  if(typeof src==="function"){const type=name.endsWith(".svg")?"image/svg+xml":name.endsWith(".json")?"application/json":"text/css";a.href=URL.createObjectURL(new Blob([src()],{type}));}
  else a.href=src;
  document.body.appendChild(a);a.click();a.remove();
  st.textContent=t("Staženo: ")+name;
});
'''+t[end:]
t=t.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
i=t.index("</style>")+len("</style>")
html='<!doctype html>\n<html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+t[:i].replace("<style>","<style>\nbody{margin:0}img{max-width:100%}[hidden]{display:none!important}\n",1)+"\n</head><body>"+t[i:]+"\n</body></html>\n"
import json,importlib.util
sp=importlib.util.spec_from_file_location('en','en.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
html=html.replace('{{EN}}',json.dumps(m.EN,ensure_ascii=False)).replace('\n</script>','\napplyLang();\n</script>')
open("../index.html","w").write(html)
