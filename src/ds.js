/* design system: tokens come from tokens/fulala.tokens.json (injected by build.py) */
const TOK={{TOKENS}};
const TOK_CSS={{TOKENS_CSS}};
const DS_USE={
 "bg-page":"Výchozí pozadí stránky, zhruba polovina každé plochy",
 "bg-brand":"Výrazné bloky, hero, patička. Ilustrace jen ve verzi bílá na cinnabar",
 "bg-inverse":"Tmavé bloky, panely ke stažení",
 "bg-subtle":"Klidné sekce a informační boxy. Bez ilustrací",
 "bg-warm":"Promo bloky. Bez ilustrací",
 "text-primary":"Veškerý běžný text, i na cinnabar",
 "text-on-brand":"Na cinnabar jen nadpisy, logo a tučný text od 19 px",
 "text-on-inverse":"Text na černé",
 "text-warm":"Text na Cornsilk a Soft Apricot",
 "text-brand":"Cinnabar text na bílé jen u nadpisů od 24 px",
 "border-default":"Okraje tlačítek, polí a karet",
 "border-focus":"Pole, do kterého se právě píše",
 "border-inverse":"Okraje na cinnabar a černé",
 "action-primary":"Primární tlačítko, jedno na obrazovce",
 "action-primary-text":"Popisek primárního tlačítka, vždy 20 px Bold",
 "action-disabled":"Nedostupné tlačítko a pole",
 "action-disabled-text":"Popisek nedostupného tlačítka",
 "feedback-error":"Okraj a ikona chyby. Text chyby zůstává černý",
 "feedback-success":"Potvrzení, vegetariánské",
 "feedback-highlight":"Bestseller, hodnocení"};
const tokRef=v=>v.slice(1,-1).split(".").reduce((o,k)=>o[k],TOK);
const SEM=[];for(const g of ["bg","text","border","action","feedback"])for(const[k,o]of Object.entries(TOK.color[g])){const p=tokRef(o.$value),name=o.$value.slice(7,-1);SEM.push([`color-${g}-${k}`,p.$value,name,DS_USE[`${g}-${k}`]])}
document.getElementById("ds-color-rows").innerHTML=SEM.map(([n,h,p,u])=>`<tr><td><code>--fulala-${n}</code></td><td><span class="chip"><i style="background:${h}"></i>${copyBtn(h)}</span> <span class="small muted">${p}</span></td><td class="muted">${t(u)}</td></tr>`).join("");
const px=v=>parseInt(v,10);
document.getElementById("ds-space").innerHTML=Object.entries(TOK.space).map(([k,o])=>`<div class="s"><span>space-${k}</span><i style="width:${px(o.$value)*1.5}px"></i>${px(o.$value)} px</div>`).join("");
document.getElementById("ds-radius").innerHTML=Object.entries(TOK.radius).map(([k,o])=>`<div><i style="border-radius:${Math.min(px(o.$value),28)}px"></i>radius-${k} · ${k==="pill"?"pill":px(o.$value)+" px"}</div>`).join("");
DLP.ds=[["Pro vývoj","CSS · JSON","Tokeny pro web a aplikaci",[["Všechny tokeny jako CSS proměnné","Barvy, mezery, zaoblení, stín, písma","CSS",[()=>TOK_CSS,"fulala-design-tokens.css"]],["Tokeny ve formátu W3C Design Tokens","Pro Figmu a nástroje na tokeny","JSON",[()=>JSON.stringify(TOK,null,2),"fulala-design-tokens.json"]],["Textové styly","Pro web a aplikaci","CSS",[TYPE_CSS,"fulala-typography.css"]]]]];
