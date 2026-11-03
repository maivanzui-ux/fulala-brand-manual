"""Build the download files in files/. Run: python3 src/assets.py (build.py runs it too)

files/logo/
- fulala-logo-<variant>-cmyk.pdf/.eps   vector logo in CMYK, drawn from the SVG paths
- fulala-logo-digital.zip               SVG + PNG (RGB) of all variants
- fulala-logo-print.zip                 CMYK PDF + EPS of all variants
  The logo SVGs and PNGs are source files and are not generated here.
files/ilustrace/
- fulala-<art>-<variant>.svg/.png       RGB artwork from src/*.svg.part (PNG via headless Chrome)
- fulala-<art>-<variant>-cmyk.pdf/.eps  the same in CMYK
- fulala-ilustrace-digital.zip / -print.zip
files/barvy/
- fulala-palette-rgb.ase / -cmyk.ase    Adobe swatches, values from COL in template.html
Every file is written only when its content changes, and ZIPs use a fixed timestamp,
so rebuilding without changes leaves the files byte-identical.
"""
import math,os,re,shutil,struct,subprocess,zipfile
SRC=os.path.dirname(os.path.abspath(__file__))
FILES=os.path.join(SRC,"..","files")

CMYK={"cinnabar":(0,.83,.83,0),"black":(0,0,0,1),"white":(0,0,0,0)}
HEX={"cinnabar":"#ff2c2c","black":"#000000","white":"#ffffff"}

def write(path,data):
    data=data.encode() if isinstance(data,str) else data
    if os.path.exists(path) and open(path,"rb").read()==data:return False
    open(path,"wb").write(data);return True

def path_ops(d):
    """SVG path data (M L H V C S Z, absolute and relative) to PDF path operators."""
    toks=re.findall(r"[MmLlHhVvCcSsZz]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?",d)
    out=[];i=0;cmd=None;x=y=sx=sy=0;c2=None
    f=lambda v:("%.3f"%v).rstrip("0").rstrip(".")
    while i<len(toks):
        if toks[i].isalpha():cmd=toks[i];i+=1
        rel=cmd.islower();C=cmd.upper()
        if C=="Z":out.append("h");x,y=sx,sy;c2=None;continue
        if C in "ML":
            nx,ny=float(toks[i]),float(toks[i+1]);i+=2
            if rel:nx+=x;ny+=y
            x,y=nx,ny
            if C=="M":sx,sy=x,y;out.append(f"{f(x)} {f(y)} m");cmd="l" if rel else "L"
            else:out.append(f"{f(x)} {f(y)} l")
            c2=None
        elif C in "HV":
            v=float(toks[i]);i+=1
            if C=="H":x=v+x if rel else v
            else:y=v+y if rel else v
            out.append(f"{f(x)} {f(y)} l");c2=None
        else:
            n=6 if C=="C" else 4
            p=[float(t) for t in toks[i:i+n]];i+=n
            if rel:p=[v+(x if j%2==0 else y) for j,v in enumerate(p)]
            if C=="S":p=([2*x-c2[0],2*y-c2[1]] if c2 else [x,y])+p
            out.append(" ".join(f(v) for v in p)+" c");c2=(p[2],p[3]);x,y=p[4],p[5]
    return "\n".join(out)

def body_for(vb,shapes,bg,pad):
    """PDF content stream. shapes: [(cmyk, path data)] in paint order."""
    x0,y0,w,h=vb;W,H=w+2*pad,h+2*pad
    body=f"1 0 0 -1 {pad-x0:.3f} {H-pad+y0:.3f} cm\n"
    if bg:body+="%g %g %g %g k\n%.3f %.3f %.3f %.3f re f\n"%(*bg,x0-pad,y0-pad,W,H)
    last=None
    for c,d in shapes:
        if c!=last:body+="%g %g %g %g k\n"%c;last=c
        body+=path_ops(d)+"\nf\n"
    return body.rstrip("\n"),W,H

def pdf(path,title,body,W,H):
    objs=["<< /Type /Catalog /Pages 2 0 R >>","<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
          f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W:.2f} {H:.2f}] /Contents 4 0 R /Resources << >> >>",
          f"<< /Length {len(body)} >>\nstream\n{body}\nendstream",
          f"<< /Title ({title}) /Producer (src/assets.py) >>"]
    out=b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n";offs=[]
    for i,o in enumerate(objs,1):offs.append(len(out));out+=f"{i} 0 obj\n{o}\nendobj\n".encode()
    xref=len(out)
    out+=f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()+"".join(f"{o:010d} 00000 n \n" for o in offs).encode()
    out+=f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R /Info 5 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    write(path,out)

PS_OPS={"m":"moveto","l":"lineto","c":"curveto","h":"closepath","f":"fill","k":"setcmykcolor"}
def eps(path,title,body,W,H):
    """Same drawing as the PDF content stream, rewritten as PostScript."""
    lines=[]
    for ln in body.split("\n"):
        a=ln.split()
        if a[-1]=="cm":lines.append("["+" ".join(a[:-1])+"] concat")
        elif a[-2:]==["re","f"]:lines.append(" ".join(a[:-2])+" rectfill")
        else:lines.append(" ".join(a[:-1]+[PS_OPS[a[-1]]]))
    head=("%!PS-Adobe-3.0 EPSF-3.0\n"
          f"%%BoundingBox: 0 0 {math.ceil(W)} {math.ceil(H)}\n%%HiResBoundingBox: 0 0 {W:.2f} {H:.2f}\n"
          f"%%Title: {title}\n%%Creator: src/assets.py\n%%LanguageLevel: 2\n"
          "%%DocumentProcessColors: Cyan Magenta Yellow Black\n%%Pages: 1\n%%EndComments\n%%Page: 1 1\n")
    write(path,head+"gsave\n"+"\n".join(lines)+"\ngrestore\nshowpage\n%%EOF\n")

def print_files(base,title,vb,shapes,bg=None,pad=0):
    body,W,H=body_for(vb,shapes,bg,pad)
    pdf(base+"-cmyk.pdf",title+", CMYK",body,W,H)
    eps(base+"-cmyk.eps",title+", CMYK",body,W,H)

def pack(zpath,files,folder):
    buf=os.path.join(os.path.dirname(zpath),".tmp.zip")
    with zipfile.ZipFile(buf,"w") as z:
        for f in files:
            z.writestr(zipfile.ZipInfo(f"{folder}/{os.path.basename(f)}",(2026,11,1,0,0,0)),open(f,"rb").read(),zipfile.ZIP_DEFLATED)
    write(zpath,open(buf,"rb").read());os.remove(buf)

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def png(svg,out,width):
    """Render an SVG to a transparent PNG with headless Chrome, only when the SVG is newer."""
    if os.path.exists(out) and os.path.getmtime(out)>=os.path.getmtime(svg):return
    chrome=CHROME if os.path.exists(CHROME) else shutil.which("chromium") or shutil.which("google-chrome")
    if not chrome:print("skipped (no Chrome):",out);return
    vb=list(map(float,re.search(r'viewBox="([^"]+)"',open(svg).read()).group(1).split()))
    h=round(width*vb[3]/vb[2]);page=out+".html"
    write(page,f'<!doctype html><style>html,body{{margin:0;background:transparent}}img{{display:block;width:{width}px;height:{h}px}}</style><img src="file://{os.path.abspath(svg)}">')
    subprocess.run([chrome,"--headless=new","--disable-gpu","--hide-scrollbars","--force-device-scale-factor=1","--default-background-color=00000000",
                    "--allow-file-access-from-files",f"--window-size={width},{h}",f"--screenshot={os.path.abspath(out)}","file://"+os.path.abspath(page)],
                   check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    os.remove(page)

# ---------- logo ----------
D=os.path.join(FILES,"logo")
LOGO={"cinnabar":("cinnabar",None),"black":("black",None),"white":("white",None),"white-on-cinnabar":("white","cinnabar")}
for name,(fg,bg) in LOGO.items():
    svg=open(os.path.join(D,f"fulala-logo-{fg}.svg")).read()
    vb=tuple(map(float,re.search(r'viewBox="([^"]+)"',svg).group(1).split()))
    print_files(os.path.join(D,f"fulala-logo-{name}"),f"Fulala logo, {name}",vb,
                [(CMYK[fg],d) for d in re.findall(r' d="([^"]+)"',svg)],CMYK[bg] if bg else None,vb[2]*.1 if bg else 0)
pack(os.path.join(D,"fulala-logo-digital.zip"),[os.path.join(D,f"fulala-logo-{n}.{x}") for n in LOGO for x in ("svg","png")],"fulala-logo")
pack(os.path.join(D,"fulala-logo-print.zip"),[os.path.join(D,f"fulala-logo-{n}-cmyk.{x}") for n in LOGO for x in ("pdf","eps")],"fulala-logo")

# ---------- illustrations ----------
# class m = artwork colour, class k = paper (holes); the cinnabar-bg artwork is its own drawing, never a recolour
D=os.path.join(FILES,"ilustrace");os.makedirs(D,exist_ok=True)
ART={"tiger-cinnabar":("tiger","cinnabar","white",None),"tiger-white-on-cinnabar":("tigercin","white","cinnabar","cinnabar"),
     "chopsticks-cinnabar":("chopsticks","cinnabar","white",None),"chopsticks-white-on-cinnabar":("chopcin","white","cinnabar","cinnabar")}
for name,(part,m,k,bg) in ART.items():
    s=open(os.path.join(SRC,part+".svg.part")).read()
    vb=tuple(map(float,re.search(r'viewBox="([^"]+)"',s).group(1).split()))
    paths=re.findall(r'<path[^>]*class="([mk])"[^>]*\sd="([^"]+)"',s)
    col={"m":m,"k":k}
    rect=f'<rect x="{vb[0]:g}" y="{vb[1]:g}" width="{vb[2]:g}" height="{vb[3]:g}" fill="{HEX[bg]}"/>' if bg else ""
    svg=('<?xml version="1.0" encoding="UTF-8"?>\n'
         f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join("%g"%v for v in vb)}" width="{vb[2]:g}" height="{vb[3]:g}">{rect}'
         +"".join(f'<path fill="{HEX[col[c]]}" d="{d}"/>' for c,d in paths)+"</svg>\n")
    base=os.path.join(D,f"fulala-{name}")
    write(base+".svg",svg)
    png(base+".svg",base+".png",2000)
    print_files(base,f"Fulala {name}",vb,[(CMYK[col[c]],d) for c,d in paths],CMYK[bg] if bg else None)
pack(os.path.join(D,"fulala-ilustrace-digital.zip"),[os.path.join(D,f"fulala-{n}.{x}") for n in ART for x in ("svg","png")],"fulala-ilustrace")
pack(os.path.join(D,"fulala-ilustrace-print.zip"),[os.path.join(D,f"fulala-{n}-cmyk.{x}") for n in ART for x in ("pdf","eps")],"fulala-ilustrace")

# ---------- colour swatches (Adobe ASE) ----------
D=os.path.join(FILES,"barvy");os.makedirs(D,exist_ok=True)
tpl=open(os.path.join(SRC,"template.html")).read()
COL=re.findall(r'\["([^"]+)","(#[0-9a-f]{6})",\d,"([\d ]+)"',tpl[tpl.index("const COL={"):])[:8]
def ase(model):
    def name(s):return struct.pack(">H",len(s)+1)+s.encode("utf-16-be")+b"\0\0"
    blocks=[(0xC001,name("Fulala"))]
    for n,h,cmyk in COL:
        vals=[int(h[i:i+2],16)/255 for i in (1,3,5)] if model=="RGB " else [int(v)/100 for v in cmyk.split()]
        blocks.append((1,name(n)+model.encode()+struct.pack(">"+"f"*len(vals),*vals)+struct.pack(">H",2)))
    blocks.append((0xC002,b""))
    return b"ASEF"+struct.pack(">HHI",1,0,len(blocks))+b"".join(struct.pack(">HI",t,len(b))+b for t,b in blocks)
write(os.path.join(D,"fulala-palette-rgb.ase"),ase("RGB "))
write(os.path.join(D,"fulala-palette-cmyk.ase"),ase("CMYK"))

# ---------- symbol (tiger head) ----------
# symbol.svg.part is the artwork for light backgrounds, symbolcin.svg.part the dedicated one for cinnabar/dark
D=os.path.join(FILES,"symbol");os.makedirs(D,exist_ok=True)
SYM={"cinnabar":("symbol","cinnabar","white"),"black":("symbol","black","white"),
     "on-cinnabar":("symbolcin","white","cinnabar"),"on-black":("symbolcin","white","black")}
def art(part):
    s=open(os.path.join(SRC,part+".svg.part")).read()
    return tuple(map(float,re.search(r'viewBox="([^"]+)"',s).group(1).split())),re.findall(r'<path class="([mk])" d="([^"]+)"',s)
def svg_doc(vb,paths,col,bg=None,square=None):
    """square: (side, padding) puts the artwork centred on a filled square, as for app icons."""
    x0,y0,w,h=vb
    if square:
        pad=square;side=max(w,h)*(1+2*pad);ox=x0-(side-w)/2;oy=y0-(side-h)/2
        view=f"{ox:g} {oy:g} {side:g} {side:g}";rect=f'<rect x="{ox:g}" y="{oy:g}" width="{side:g}" height="{side:g}" fill="{HEX[bg]}"/>'
        size=f'width="{side:g}" height="{side:g}"'
    else:
        view=" ".join("%g"%v for v in vb);rect="";size=f'width="{w:g}" height="{h:g}"'
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" {size}>{rect}'
            +"".join(f'<path fill="{HEX[col[c]]}" d="{d}"/>' for c,d in paths)+"</svg>\n")
for name,(part,m,k) in SYM.items():
    vb,paths=art(part);col={"m":m,"k":k};base=os.path.join(D,f"fulala-symbol-{name}")
    write(base+".svg",svg_doc(vb,paths,col))
    png(base+".svg",base+".png",1000)
    print_files(base,f"Fulala symbol, {name}",vb,[(CMYK[col[c]],d) for c,d in paths])
pack(os.path.join(D,"fulala-symbol-digital.zip"),[os.path.join(D,f"fulala-symbol-{n}.{x}") for n in SYM for x in ("svg","png")],"fulala-symbol")
pack(os.path.join(D,"fulala-symbol-print.zip"),[os.path.join(D,f"fulala-symbol-{n}-cmyk.{x}") for n in SYM for x in ("pdf","eps")],"fulala-symbol")

# favicon and app icons: the cinnabar-bg artwork on a cinnabar square
vb,paths=art("symbolcin");col={"m":"white","k":"cinnabar"}
write(os.path.join(D,"icon.svg"),svg_doc(vb,paths,col,bg="cinnabar",square=.12))
ICONS={"favicon-16.png":16,"favicon-32.png":32,"favicon-48.png":48,"apple-touch-icon.png":180,"icon-192.png":192,"icon-512.png":512}
# Chrome renders the 512 px master; smaller sizes are downscaled with sips (headless Chrome stalls on tiny windows)
master=os.path.join(D,"icon-512.png");png(os.path.join(D,"icon.svg"),master,512)
for f,px in ICONS.items():
    out=os.path.join(D,f)
    if out!=master and (not os.path.exists(out) or os.path.getmtime(out)<os.path.getmtime(master)):
        subprocess.run(["sips","-z",str(px),str(px),master,"--out",out],check=True,stdout=subprocess.DEVNULL)
def ico(out,sizes):
    data=[open(os.path.join(D,f"favicon-{s}.png"),"rb").read() for s in sizes]
    head=struct.pack("<HHH",0,1,len(sizes));off=6+16*len(sizes);entries=b""
    for s,b in zip(sizes,data):entries+=struct.pack("<BBBBHHII",s,s,0,0,1,32,len(b),off);off+=len(b)
    write(out,head+entries+b"".join(data))
ico(os.path.join(D,"favicon.ico"),(16,32,48))
pack(os.path.join(D,"fulala-favicon.zip"),[os.path.join(D,f) for f in ("favicon.ico","icon.svg",*ICONS)],"fulala-favicon")
