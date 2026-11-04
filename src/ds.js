/* design system tokens */
const DS={
 color:[
  ["color-brand","#ff2c2c","Hlavní barva značky, primární tlačítka, logo"],
  ["color-brand-pressed","#e01b1b","Stisknuté tlačítko, cinnabar text na bílé"],
  ["color-bg","#ffffff","Pozadí stránky"],
  ["color-surface","#f9edcc","Zvýrazněné sekce, pozadí karet (Cornsilk)"],
  ["color-surface-warm","#ffdab9","Teplé plochy, promo bloky (Soft Apricot)"],
  ["color-text","#000000","Text a ikony"],
  ["color-text-on-brand","#ffffff","Velký tučný text na cinnabar"],
  ["color-text-warm","#61210f","Text na světlých teplých plochách (Dark Walnut)"],
  ["color-success","#00bb77","Potvrzení, vegetariánské (Jungle green)"],
  ["color-highlight","#edae49","Bestseller, hodnocení (Honey Bronze)"],
  ["color-error","#ff2c2c","Chyby ve formulářích, vždy s textem"]],
 space:[["space-1",4],["space-2",8],["space-3",12],["space-4",16],["space-6",24],["space-8",32],["space-12",48],["space-16",64]],
 radius:[["radius-sm",8],["radius-md",14],["radius-lg",20],["radius-pill",999]],
 shadow:[["shadow-sm","0 1px 2px rgba(23,17,15,.08), 0 2px 6px rgba(23,17,15,.06)"],["shadow-md","0 6px 20px rgba(23,17,15,.12)"],["shadow-pop","4px 4px 0 #000000"]]
};
document.getElementById("ds-color-rows").innerHTML=DS.color.map(([n,h,u])=>`<tr><td><code>--fulala-${n}</code></td><td><span class="chip"><i style="background:${h}"></i>${copyBtn(h)}</span></td><td class="muted">${u}</td></tr>`).join("");
document.getElementById("ds-space").innerHTML=DS.space.map(([n,v])=>`<div class="s"><span>${n}</span><i style="width:${v*2}px"></i>${v} px</div>`).join("");
document.getElementById("ds-radius").innerHTML=DS.radius.map(([n,v])=>`<div><i style="border-radius:${Math.min(v,28)}px"></i>${n} · ${v===999?"pill":v+" px"}</div>`).join("");
const DS_CSS=()=>{let o="/* Fulala design tokens v1.0 (návrh) */\n:root {\n";
  [...COL.core,...COL.extra].forEach(([n,h])=>o+=`  --fulala-${n.toLowerCase().replace(/ /g,"-")}: ${h};\n`);
  o+="\n";DS.color.forEach(([n,h])=>o+=`  --fulala-${n}: ${h};\n`);
  o+="\n";DS.space.forEach(([n,v])=>o+=`  --fulala-${n}: ${v}px;\n`);
  o+="\n";DS.radius.forEach(([n,v])=>o+=`  --fulala-${n}: ${v}px;\n`);
  o+="\n";DS.shadow.forEach(([n,v])=>o+=`  --fulala-${n}: ${v};\n`);
  o+="\n  --fulala-font-display: \"Grandstander\", system-ui, sans-serif;\n  --fulala-font-body: \"DM Sans\", system-ui, sans-serif;\n}\n";return o};
const DS_JSON=()=>JSON.stringify({
  color:{brand:Object.fromEntries([...COL.core,...COL.extra].map(([n,h])=>[n.toLowerCase().replace(/ /g,"-"),{$type:"color",$value:h}])),
         semantic:Object.fromEntries(DS.color.map(([n,h,u])=>[n.replace("color-",""),{$type:"color",$value:h,$description:t(u)}]))},
  space:Object.fromEntries(DS.space.map(([n,v])=>[n.replace("space-",""),{$type:"dimension",$value:v+"px"}])),
  radius:Object.fromEntries(DS.radius.map(([n,v])=>[n.replace("radius-",""),{$type:"dimension",$value:v+"px"}])),
  shadow:Object.fromEntries(DS.shadow.map(([n,v])=>[n.replace("shadow-",""),{$type:"shadow",$value:v}])),
  font:{display:{$type:"fontFamily",$value:"Grandstander"},body:{$type:"fontFamily",$value:"DM Sans"}}},null,2);
DLP.ds=[["Pro vývoj","CSS · JSON","Tokeny pro web a aplikaci",[["Všechny tokeny jako CSS proměnné","Barvy, mezery, zaoblení, stíny","CSS",[DS_CSS,"fulala-design-tokens.css"]],["Tokeny ve formátu W3C Design Tokens","Pro Figmu a nástroje na tokeny","JSON",[DS_JSON,"fulala-design-tokens.json"]],["Textové styly","Pro web a aplikaci","CSS",[TYPE_CSS,"fulala-typography.css"]]]]];
