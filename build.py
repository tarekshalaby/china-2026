# -*- coding: utf-8 -*-
import json, html, datetime
from data import (cities, days, items, bookings, flights, trains, hotels, prep,
                  nextup, ribbon, bands, heroes)
P=json.load(open("places.json"))
P["aperture"]["img"]=P["maochengdu"]["img"]; P["aperture"]["imgpage"]=P["maochengdu"]["imgpage"]
CAT={"struggle":("#E53935","✊","People's history"),"music":("#8E24AA","\U0001F3B8","Live music"),
     "food":("#FB8C00","\U0001F35C","Local food"),"landmark":("#1E88E5","\U0001F3DB️","Landmark, reframed"),
     "transit":("#607D8B","\U0001F684","Travel")}
BST={"booked":("#2E7D32","Booked"),"todo":("#C62828","Still to book"),"gate":("#546E7A","Pay at the gate")}
TONE={"k":"#2E7D32","w":"#E65100","n":"#455A64"}
CCOL={c["id"]:c["color"] for c in cities}; CCOL["air"]="#90A4AE"
CNAME={c["id"]:c["name"] for c in cities}; CNAME["air"]="In the air"
E=html.escape
def rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def rgba(h,a):
    r,g,b=rgb(h); return f'rgba({r},{g},{b},{a})'

ICON={
 "plane":'<path d="M2 13l20-8-7 8 7 8z"/>',
 "train":'<rect x="5" y="3" width="14" height="13" rx="3.5"/><path d="M5.5 10.5h13M9 19l-2 2.5M15 19l2 2.5"/><circle cx="9.2" cy="13.3" r=".9" fill="currentColor" stroke="none"/><circle cx="14.8" cy="13.3" r=".9" fill="currentColor" stroke="none"/>',
 "bed":'<path d="M3 19V9h11a5 5 0 0 1 5 5v5M2.5 15.5h17M2.5 19.5h19"/><circle cx="7.5" cy="12" r="1.9"/>',
 "ticket":'<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><path d="M14.5 6.5v11" stroke-dasharray="2.2 2.4"/>',
 "passport":'<rect x="5" y="2.5" width="14" height="19" rx="2.5"/><circle cx="12" cy="10" r="3.2"/><path d="M8.5 17.5h7"/>',
 "phone":'<rect x="6.5" y="2" width="11" height="20" rx="2.5"/><path d="M10.5 19h3"/>',
 "money":'<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M5.5 9.5v5M18.5 9.5v5"/>',
 "sim":'<rect x="5" y="2.5" width="14" height="19" rx="2.5"/><rect x="8" y="11" width="8" height="7" rx="1.5"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7.2V12l3.6 2"/>',
 "alert":'<path d="M12 3.2 2.6 20h18.8z"/><path d="M12 9.4v4.4M12 17h.02"/>',
 "book":'<path d="M4 3.5h8.5A3 3 0 0 1 15.5 6.5v14a3 3 0 0 0-3-3H4z"/><path d="M20 3.5h-4.5v14H20z"/>',
 "pin":'<path d="M12 21.5s7-6.2 7-11.5a7 7 0 1 0-14 0c0 5.3 7 11.5 7 11.5z"/><circle cx="12" cy="10" r="2.6"/>',
}
def ic(name,size=22,cls=""):
    return (f'<svg class="i {cls}" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')

def img(pid,cls=""):
    p=P.get(pid)
    if p and p.get("img"):
        return f'<img class="{cls}" src="{p["img"]}" alt="{E(p["name"])}" loading="lazy">'
    return f'<div class="{cls} noimg"></div>'

import re
_SENT=re.compile(r'(?<=[.!?])\s+(?=[A-Z\u4e00-\u9fff\u00a5\d])')
def lead_sentence(t):
    parts=_SENT.split(t)
    if len(parts)<2: return t
    head=parts[0]
    i=1
    while len(head)<30 and i<len(parts) and len(head)+1+len(parts[i])<=132:
        head=head+' '+parts[i]; i+=1
    return head

def chips(cs):
    if not cs: return ''
    return '<div class="chips">'+''.join(
      f'<span class="chip" style="--t:{TONE[t]};--tbg:{rgba(TONE[t],.07)};--tbd:{rgba(TONE[t],.22)}">{E(v)}</span>' for t,v in cs)+'</div>'

def fine(ps,label="The small print"):
    if not ps: return ''
    return ('<details class="fine"><summary>'+E(label)+'</summary>'
            +''.join(f'<p>{p}</p>' for p in ps)+'</details>')

out=[]; w=out.append
w("""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>China, the people's version — 20 Sep to 3 Oct 2026</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
:root{--ink:#1a1c1e;--muted:#5f6368;--line:#e3e5e8;--soft:#f6f7f8;--bg:#fff}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:17px;line-height:1.5;color:var(--ink);background:var(--bg)}
a{color:inherit}
svg.i{flex:none;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
h2.big{font-size:clamp(36px,5.6vw,68px);letter-spacing:-.025em;line-height:1;margin:0 0 6px;font-weight:800}
p.lead{font-size:19px;color:var(--muted);margin:0 0 26px;max-width:640px}

/* ---------- header ---------- */
header.top{padding:52px 0 8px}
header.top h1{font-size:clamp(38px,6vw,74px);line-height:.97;letter-spacing:-.025em;margin:0 0 12px;font-weight:800}
header.top .dates{font-size:19px;color:var(--muted);margin:0 0 30px}

/* ribbon */
.ribbon{margin:0 0 34px}
.rbands{display:grid;grid-template-columns:repeat(15,1fr);gap:3px;margin-bottom:6px;height:24px}
.rband{border-radius:6px;color:#fff;font-size:11.5px;font-weight:700;display:flex;align-items:center;
 justify-content:center;letter-spacing:.02em;white-space:nowrap;overflow:hidden;padding:0 4px}
.rdays{display:grid;grid-template-columns:repeat(15,1fr);gap:3px}
.rday{background:var(--c);color:#fff;border-radius:7px;padding:8px 2px 7px;text-align:center;line-height:1.05}
.rday b{display:block;font-size:clamp(13px,1.35vw,19px);font-weight:800;letter-spacing:-.02em}
.rday span{display:block;font-size:clamp(8.5px,.85vw,11px);opacity:.85;text-transform:uppercase;letter-spacing:.06em}
.rkey{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:10px;font-size:13.5px;color:var(--muted)}
.rkey b{color:var(--ink)}

/* next up */
.nextup{display:grid;grid-template-columns:repeat(auto-fit,minmax(272px,1fr));gap:12px;margin:0 0 34px}
.nu{border:1px solid var(--line);border-left:5px solid var(--t);border-radius:12px;padding:14px 16px;background:#fff;
 display:grid;grid-template-columns:auto 1fr;gap:3px 12px;align-items:start}
.nu .nic{grid-row:span 3;color:var(--t);margin-top:3px}
.nu .nw{font-size:12px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--t)}
.nu .nw em{font-style:normal;opacity:.65;font-weight:700;letter-spacing:.03em}
.nu .nh{font-size:17px;font-weight:700;line-height:1.25;letter-spacing:-.01em}
.nu .nl{font-size:14.5px;color:var(--muted);line-height:1.4}

/* nav */
.citynav{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 16px}
.citynav a{display:block;padding:16px;color:#fff;text-decoration:none;font-weight:700;font-size:19px;border-radius:11px}
.citynav a span{display:block;font-weight:400;font-size:13.5px;opacity:.92;margin-top:2px}
.bar{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding:16px 0 0;border-top:1px solid var(--line)}
.refnav{display:flex;flex-wrap:wrap;gap:7px}
.refnav a{font-size:14.5px;font-weight:700;text-decoration:none;border:1.5px solid var(--line);
 padding:8px 15px;border-radius:999px;display:inline-flex;align-items:center;gap:7px}
.refnav a:hover{background:var(--soft)}
.legend{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin-left:auto}
.legend .lg{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;color:var(--muted)}
.legend .dot{width:24px;height:24px;border-radius:50%;display:inline-grid;place-items:center;color:#fff;font-size:12px}

/* ---------- chips, small print ---------- */
.chips{display:flex;flex-wrap:wrap;gap:7px}
.chip{font-size:13.5px;font-weight:700;color:var(--t);background:var(--tbg);border:1px solid var(--tbd);
 border-radius:8px;padding:5px 10px;white-space:nowrap}
details.fine{margin-top:13px}
details.fine summary{font-size:13.5px;font-weight:700;color:var(--muted);cursor:pointer;list-style:none;
 display:inline-flex;align-items:center;gap:7px;padding:5px 11px;border:1px solid var(--line);border-radius:999px}
details.fine summary::-webkit-details-marker{display:none}
details.fine summary:hover{background:var(--soft)}
details.fine summary:before{content:"+";font-size:15px;line-height:1}
details.fine[open] summary:before{content:"\\2013"}
details.fine p{font-size:15.5px;margin:12px 0 0;max-width:68ch;line-height:1.55;color:#33363a}
.ref{font-size:13px;color:var(--muted);margin-top:11px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
 letter-spacing:-.01em;word-break:break-word}

/* ---------- city ---------- */
section.city{margin-top:60px}
.cityhead{color:#fff;position:relative;overflow:hidden;background:var(--c)}
.cityhead .hero{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cityhead .tint{position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.26) 0%,rgba(0,0,0,0) 46%),var(--g)}
.cityhead .inner{position:relative;padding:46px 0 38px}
.cityhead h2{font-size:clamp(42px,6.6vw,84px);line-height:.95;letter-spacing:-.03em;margin:0;font-weight:800;
 text-shadow:0 2px 18px rgba(0,0,0,.28)}
.cityhead .sub{font-size:20px;margin-top:8px;max-width:30ch;text-shadow:0 1px 10px rgba(0,0,0,.3)}
.cityhead .meta{display:flex;flex-wrap:wrap;gap:6px 10px;margin-top:16px;font-size:14px}
.cityhead .meta span{background:rgba(0,0,0,.24);padding:5px 11px;border-radius:999px;display:inline-flex;align-items:center;gap:6px}
.cityhead .quick{position:absolute;right:24px;top:40px;display:flex;gap:7px}
.cityhead .quick a{color:#fff;text-decoration:none;background:rgba(0,0,0,.26);padding:7px 13px;border-radius:999px;font-size:13.5px}

.day{display:grid;grid-template-columns:118px 1fr;gap:0 30px;padding:32px 0 6px;border-top:1px solid var(--line)}
.day:first-of-type{border-top:0}
.datecol{position:sticky;top:14px;align-self:start}
.datecol .wd{font-size:14px;color:var(--muted)}
.datecol .dn{font-size:50px;line-height:1;font-weight:800;letter-spacing:-.035em}
.datecol .mo{font-size:15px;font-weight:700;color:var(--muted)}
.datecol .theme{margin-top:11px;font-size:14.5px;line-height:1.35;padding-left:10px;border-left:4px solid}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(252px,1fr));gap:18px;margin-bottom:18px}
.card{border-radius:13px;overflow:hidden;background:#fff;border:1px solid var(--line);display:flex;flex-direction:column;border-top:6px solid}
.card .ph{position:relative;aspect-ratio:16/10;background:#eceff1;overflow:hidden}
.card .ph img,.card .ph .noimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.card .badge{position:absolute;left:10px;top:10px;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:17px;box-shadow:0 2px 7px rgba(0,0,0,.3)}
.card .num{position:absolute;right:10px;top:10px;min-width:29px;height:29px;padding:0 8px;border-radius:15px;background:rgba(26,28,30,.92);color:#fff;font-weight:700;display:grid;place-items:center;font-size:14px}
.card .pill{position:absolute;left:10px;bottom:10px;font-size:12px;font-weight:800;color:#fff;padding:5px 11px;border-radius:999px;text-decoration:none;box-shadow:0 2px 7px rgba(0,0,0,.32);letter-spacing:.01em}
.card .bd{padding:13px 15px 15px;display:flex;flex-direction:column;gap:5px;flex:1}
.card .slot{font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
.card h4{margin:1px 0 0;font-size:18.5px;line-height:1.2;letter-spacing:-.015em}
.card .one{margin:0;font-size:15px;line-height:1.4}
.card .tip{margin:4px 0 0;font-size:13.5px;color:var(--muted);line-height:1.45;padding-left:17px;position:relative}
.card .tip:before{content:"\\21B3";position:absolute;left:0;top:0}
.card .more{margin-top:auto;padding-top:9px;font-size:13.5px;font-weight:700;text-decoration:none}
.card .more:hover{text-decoration:underline}
.transit{grid-column:1/-1;display:flex;align-items:center;gap:15px;background:var(--soft);border-radius:13px;padding:14px 18px;border-left:6px solid #607D8B}
.transit .ic{color:#607D8B}
.transit b{font-size:17.5px}
.transit .one{font-size:15px}
.transit .tip{color:var(--muted);font-size:13.5px}

.mapblock{margin:18px 0 0;padding-top:26px;border-top:1px solid var(--line)}
.mapblock h3{font-size:25px;margin:0 0 4px;letter-spacing:-.02em}
.mapblock p{margin:0 0 13px;color:var(--muted);font-size:14.5px}
.map{height:500px;border-radius:14px;border:1px solid var(--line)}
.mk{width:29px;height:29px;border-radius:50%;color:#fff;font-weight:800;font-size:13.5px;display:grid;place-items:center;border:2.5px solid #fff;box-shadow:0 1px 5px rgba(0,0,0,.4)}
.mk.star{width:37px;height:37px;font-size:21px;background:#1a1c1e}
.leaflet-popup-content{font-family:inherit;font-size:14px;line-height:1.35}
.far{margin:11px 0 0;font-size:14px;color:var(--muted)}
.far span{display:inline-block;margin-right:14px}

/* ---------- reference sections ---------- */
section.refsec{margin-top:88px}
.grouphead{display:flex;align-items:center;gap:11px;margin:46px 0 4px}
.grouphead .gi{width:42px;height:42px;border-radius:11px;display:grid;place-items:center;color:#fff;background:#607D8B}
.grouphead h3{font-size:25px;margin:0;letter-spacing:-.02em}

/* flight / train legs */
.legs{display:grid;grid-template-columns:repeat(auto-fit,minmax(266px,1fr));gap:13px;margin:16px 0 0}
.leg{border:1px solid var(--line);border-radius:13px;padding:14px 16px 15px;border-top:5px solid #607D8B}
.leg .lno{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:12px}
.leg .lno b{font-size:17px;letter-spacing:-.01em}
.leg .lno span{font-size:13px;color:var(--muted)}
.route{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:10px}
.route .t{font-size:24px;font-weight:800;letter-spacing:-.03em;line-height:1}
.route .c{font-size:13px;font-weight:700;color:var(--muted);margin-top:3px}
.route .n{font-size:11.5px;color:var(--muted);margin-top:1px}
.route .mid{display:flex;align-items:center;gap:4px;color:#90A4AE}
.route .mid i{flex:1;height:2px;background:currentColor;border-radius:2px;display:block}
.route .r{text-align:right}
.leg .ld{font-size:12.5px;color:var(--muted);margin-top:11px;border-top:1px solid var(--line);padding-top:9px}

/* reference row */
.row{display:grid;grid-template-columns:186px 1fr;gap:12px 28px;padding:24px 0;border-top:1px solid var(--line);scroll-margin-top:14px}
.row .side .pill2{display:inline-block;font-size:12.5px;font-weight:800;color:#fff;padding:5px 12px;border-radius:999px;letter-spacing:.01em}
.row .side .when{font-size:16px;margin-top:9px;font-weight:700;line-height:1.3}
.row .side .clock{font-size:14px;color:var(--muted);margin-top:2px;display:flex;align-items:center;gap:6px}
.row h4{margin:0 0 4px;font-size:22px;letter-spacing:-.02em;line-height:1.2}
.row h4 a{font-size:13.5px;font-weight:400;color:var(--muted);text-decoration:none;margin-left:9px;white-space:nowrap}
.row .cn{font-size:14.5px;color:var(--muted);margin:0 0 11px}
.row .line{font-size:17px;line-height:1.5;max-width:66ch;margin:12px 0 0}
.addr{display:grid;grid-template-columns:auto 1fr;gap:9px 11px;margin:14px 0 0;font-size:15px;align-items:start}
.addr .ai{color:#607D8B;margin-top:2px}
.addr .cnaddr{font-size:17px;font-weight:700;background:var(--soft);border:1px solid var(--line);
 border-radius:9px;padding:9px 12px;display:block;width:fit-content;max-width:100%;margin-top:7px}
.addr .cnaddr em{display:block;font-style:normal;font-size:12px;font-weight:400;color:var(--muted);margin-top:3px;letter-spacing:.02em;text-transform:uppercase}
.rlist{margin:13px 0 0;display:grid;gap:7px}
.rlist div{font-size:14.5px;display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:baseline}
.rlist b{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13.5px;background:var(--soft);
 border:1px solid var(--line);border-radius:6px;padding:3px 7px;white-space:nowrap}

/* prep tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:14px;margin-top:20px}
.tile{border:1px solid var(--line);border-radius:14px;padding:18px 19px 19px}
.tile .th{display:flex;align-items:center;gap:11px;margin-bottom:12px}
.tile .th .ti{width:40px;height:40px;border-radius:11px;display:grid;place-items:center;background:var(--soft);color:#37474F}
.tile .th b{font-size:19px;letter-spacing:-.015em}
.tile .line{font-size:15.5px;line-height:1.5;margin:11px 0 0}

/* ---------- stories ---------- */
section.stories{margin-top:92px;padding-bottom:70px}
.storycity{margin-top:50px}
.storycity h3{font-size:27px;margin:0 0 14px;padding:9px 15px;color:#fff;border-radius:9px;display:inline-block}
.story{display:grid;grid-template-columns:300px 1fr;gap:26px;padding:28px 0;border-top:1px solid var(--line);scroll-margin-top:14px}
.story .ph{border-radius:11px;overflow:hidden;aspect-ratio:4/3;background:#eceff1;position:relative;border-top:6px solid}
.story .ph img,.story .ph .noimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.story .ph .badge{position:absolute;left:10px;top:10px;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:17px}
.story h4{margin:0 0 4px;font-size:24px;letter-spacing:-.02em;line-height:1.15}
.story .when{font-size:13.5px;color:var(--muted);margin-bottom:14px;display:flex;flex-wrap:wrap;gap:4px 10px}
.story .when b{color:var(--ink)}
.story p{margin:0 0 12px;max-width:66ch;font-size:17px;line-height:1.62}
.story p:first-of-type{font-size:19px;line-height:1.55}
.story .tip{color:var(--muted);font-size:14.5px;padding-left:17px;position:relative;max-width:66ch;line-height:1.5}
.story .tip:before{content:"\\21B3";position:absolute;left:0}
.story .back{font-size:13.5px;text-decoration:none;font-weight:700;display:inline-block;margin-top:12px}
.story .credit{font-size:11.5px;color:var(--muted);margin-top:6px}
footer{border-top:1px solid var(--line);padding:22px 0 44px;font-size:13.5px;color:var(--muted)}

@media (max-width:860px){
 .row{grid-template-columns:1fr;gap:8px}
 .story{grid-template-columns:1fr}
 .cityhead .quick{position:static;margin-top:16px}
}
@media (max-width:760px){
 .citynav{grid-template-columns:1fr 1fr}
 .day{grid-template-columns:1fr}
 .datecol{position:static;display:flex;gap:11px;align-items:baseline;flex-wrap:wrap;margin-bottom:13px}
 .datecol .dn{font-size:34px}
 .datecol .theme{border-left:0;padding-left:0;margin-top:0;flex-basis:100%}
 .legend{margin-left:0}
 .map{height:380px}
 .rday{padding:6px 1px 5px;border-radius:5px}
 .rbands{height:20px}
 .addr{grid-template-columns:1fr}
 .addr .ai{display:none}
}
@media print{.map,.citynav,.quick,.refnav,.nextup{display:none}.card,.story,.row{break-inside:avoid}details.fine{display:none}}
</style></head><body>
""")

# ================= header =================
w('<header class="top"><div class="wrap">')
w('<h1>China, the people\'s version</h1>')
w('<p class="dates">Beijing · Xi\'an · Chengdu · Chongqing &nbsp;—&nbsp; 19 September to 3 October 2026 &nbsp;—&nbsp; four of us</p>')

# ribbon
w('<div class="ribbon"><div class="rbands">')
used=1
for label,col,a,b in bands:
    if a>used: w(f'<span style="grid-column:{used}/{a}"></span>')
    w(f'<span class="rband" style="grid-column:{a}/{b};background:{col}">{E(label)}</span>')
    used=b
w('</div><div class="rdays">')
for cid,dn,mo in ribbon:
    w(f'<div class="rday" style="--c:{CCOL[cid]}"><b>{dn}</b><span>{mo}</span></div>')
w('</div><div class="rkey">')
for c in cities:
    w(f'<span><b style="color:{c["color"]}">■</b> {E(c["name"])} · {c["nights"]} nights</span>')
w('<span><b style="color:#90A4AE">■</b> Flying</span>')
w('</div></div>')

# next up
w('<div class="nextup">')
for n in nextup:
    t=TONE[n["tone"]]
    sub=f' <em>{E(n["sub"])}</em>' if n["sub"] else ''
    w(f'<div class="nu" style="--t:{t}"><span class="nic">{ic(n["icon"],21)}</span>'
      f'<span class="nw">{E(n["when"])}{sub}</span>'
      f'<span class="nh">{E(n["head"])}</span><span class="nl">{E(n["line"])}</span></div>')
w('</div>')

w('<nav class="citynav">')
for c in cities:
    w(f'<a href="#{c["id"]}" style="background:{c["color"]}">{c["name"]}<span>{c["dates"]}</span></a>')
w('</nav>')
w('<div class="bar"><nav class="refnav">')
for href,i,lab in [("#travel","plane","Flights, trains, hotels"),("#tickets","ticket","Tickets"),
                   ("#prep","passport","Before you fly"),("#stories","book","The stories")]:
    w(f'<a href="{href}">{ic(i,17)}{E(lab)}</a>')
w('</nav><div class="legend">')
for k,(col,i2,lab) in CAT.items():
    w(f'<span class="lg"><span class="dot" style="background:{col}">{i2}</span>{lab}</span>')
w('</div></div>')
w('</div></header>')

# ================= cities =================
for c in cities:
    cid=c["id"]; col=c["color"]
    citems=[it for it in items if it[1]==cid]
    nums={}; n=0
    for it in citems:
        if it[4]!="transit": n+=1; nums[it[0]]=n
    g=(f'linear-gradient(98deg,{col} 0%,{col} 38%,{rgba(col,.74)} 52%,{rgba(col,.18)} 74%,{rgba(col,0)} 88%)')
    w(f'<section class="city" id="{cid}"><div class="cityhead" style="--c:{col};--g:{g}">')
    w(img(heroes[cid],"hero")); w('<div class="tint"></div>')
    w('<div class="inner"><div class="wrap">')
    w(f'<h2>{E(c["name"])}</h2><div class="sub">{E(c["sub"])}</div>')
    w(f'<div class="meta"><span>{ic("clock",15)}{c["dates"]}</span><span>{ic("bed",15)}{E(c["hotel"].split(",")[0])}</span>'
      f'<span>{ic("pin",15)}{c["nights"]} nights</span></div>')
    w(f'<div class="quick"><a href="#map-{cid}">Map</a><a href="#hotel-{cid}">Hotel</a><a href="#stories-{cid}">Stories</a></div>')
    w('</div></div></div><div class="wrap">')
    for di,(dlabel,theme) in enumerate(days[cid]):
        wd,dn,mo=dlabel.split()
        w(f'<div class="day" id="day-{cid}-{di}"><div class="datecol"><div class="wd">{wd}</div><div class="dn">{dn}</div>'
          f'<div class="mo">{mo}</div><div class="theme" style="border-color:{col}">{E(theme)}</div></div><div class="cards">')
        for it in citems:
            pid,_,d,slot,cat,title,one,tip,story,far=it
            if d!=di: continue
            ccol,i2,lab=CAT[cat]
            if cat=="transit":
                w(f'<div class="transit"><span class="ic">{ic("train",26)}</span><div><b>{E(title)}</b> '
                  f'<span class="slot" style="color:#607D8B"> {E(slot)}</span><div class="one">{E(one)}</div>'
                  f'<div class="tip">{E(tip)}</div></div></div>')
                continue
            farlab=' <span style="font-weight:400;text-transform:none;letter-spacing:0;color:#5f6368">(out of town)</span>' if far else ''
            bk=bookings.get(pid)
            pill=(f'<a class="pill" style="background:{BST[bk["state"]][0]}" href="#ticket-{pid}">{E(bk["pill"])}</a>') if bk else ''
            w(f'<article class="card" style="border-top-color:{ccol}"><div class="ph">{img(pid)}'
              f'<span class="badge" style="background:{ccol}" title="{lab}">{i2}</span>'
              f'<span class="num">{nums[pid]}</span>{pill}</div>')
            w(f'<div class="bd"><div class="slot" style="color:{ccol}">{E(slot)}{farlab}</div><h4>{E(title)}</h4><p class="one">{E(one)}</p>')
            if tip: w(f'<p class="tip">{E(lead_sentence(tip))}</p>')
            if story: w(f'<a class="more" style="color:{ccol}" href="#story-{pid}">Read the story</a>')
            w('</div></article>')
        w('</div></div>')
    w(f'<div class="mapblock" id="map-{cid}"><h3>{E(c["name"])} on the map</h3>'
      f'<p>Pins match the card numbers and the category colours. The black pin is your hotel.</p><div class="map" id="lmap-{cid}"></div>')
    fars=[it for it in citems if it[9]]
    if fars:
        w('<p class="far">Off the edge of the map: '+" ".join(f'<span><b>{nums[it[0]]}</b> {E(it[5])}</span>' for it in fars)+'</p>')
    w('</div></div></section>')

# ================= travel =================
w('<section class="refsec" id="travel"><div class="wrap"><h2 class="big">Flights, trains, hotels</h2>')
w('<p class="lead">Every reference, seat and address from the confirmations. Passport numbers are not here — the gates read the passport itself.</p>')

w(f'<div class="grouphead"><span class="gi">{ic("plane",22)}</span><h3>Flights</h3></div>')
w(chips(flights["chips"]))
w(f'<p class="line" style="margin-top:12px">{E(flights["line"])}</p>')
w('<div class="legs">')
for g in flights["segs"]:
    w(f'<div class="leg"><div class="lno"><b>{E(g["no"])}</b><span>{E(g["date"])}</span></div><div class="route">')
    w(f'<div><div class="t">{E(g["at"])}</div><div class="c">{E(g["a"])}</div><div class="n">{E(g["an"])}</div></div>')
    w(f'<div class="mid"><i></i>{ic("plane",15)}<i></i></div>')
    w(f'<div class="r"><div class="t">{E(g["bt"])}</div><div class="c">{E(g["b"])}</div><div class="n">{E(g["bn"])}</div></div>')
    w(f'</div><div class="ld">{E(g["dur"])} · {E(g["note"])}</div></div>')
w('</div>')
w('<div class="rlist">'+''.join(f'<div><b>{E(p)}</b><span>{E(nm)} · e-ticket {E(t)}</span></div>' for p,nm,t in flights["refs"])+'</div>')
w(fine(flights["fine"]))

w(f'<div class="grouphead"><span class="gi">{ic("train",22)}</span><h3>Trains</h3></div>')
for t in trains:
    bcol,_=BST[t["state"]]
    w(f'<div class="row" id="train-{E(t["date"]).replace(" ","")}"><div class="side">')
    w(f'<span class="pill2" style="background:{bcol}">{E(t["pill"])}</span>')
    w(f'<div class="when">{E(t["date"])}</div><div class="clock">{ic("clock",14)}{E(t["dur"])} · {E(t["no"])}</div></div><div>')
    w('<div class="route" style="max-width:520px">')
    w(f'<div><div class="t">{E(t["at"])}</div><div class="c">{E(t["a"])}</div><div class="n">{E(t["acn"])}</div></div>')
    w(f'<div class="mid"><i></i>{ic("train",16)}<i></i></div>')
    w(f'<div class="r"><div class="t">{E(t["bt"])}</div><div class="c">{E(t["b"])}</div><div class="n">{E(t["bcn"])}</div></div>')
    w('</div>')
    w('<div style="margin-top:14px">'+chips(t["chips"])+'</div>')
    w(f'<p class="line">{E(t["line"])}</p>')
    w(f'<div class="rlist"><div><b>Seats</b><span>{E(t["seats"])}</span></div></div>')
    w(f'<div class="ref">{E(t["ref"])}</div>')
    w(fine(t["fine"]))
    w('</div></div>')

w(f'<div class="grouphead"><span class="gi">{ic("bed",22)}</span><h3>Hotels</h3></div>')
CBY={c["id"]:c for c in cities}
for h in hotels:
    c=CBY[h["city"]]
    w(f'<div class="row" id="hotel-{h["city"]}"><div class="side">')
    w(f'<span class="pill2" style="background:{c["color"]}">{E(c["name"])}</span>')
    w(f'<div class="when">{E(h["inn"])}</div><div class="clock">{ic("clock",14)}out {E(h["out"])}</div>'
      f'<div class="clock">{ic("bed",14)}{E(h["nights"])}</div></div><div>')
    w(f'<h4>{E(h["name"])}</h4><p class="cn">{E(h["cn"])}</p>')
    w(chips(h["chips"]))
    w(f'<p class="line">{E(h["line"])}</p>')
    w(f'<div class="addr"><span class="ai">{ic("pin",19)}</span><div>{E(h["addr"])}'
      f'<span class="cnaddr">{E(h["addrcn"])}<em>show this to the driver</em></span></div>'
      f'<span class="ai">{ic("phone",19)}</span><div>{E(h["phone"])}</div></div>')
    w('<div class="rlist">'+''.join(f'<div><b>{E(no)} · {E(pin)}</b><span>{E(what)}</span></div>' for no,pin,what in h["refs"])+'</div>')
    w(fine(h["fine"]))
    w('</div></div>')
w('</div></section>')

# ================= tickets =================
counts={k:sum(1 for b in bookings.values() if b["state"]==k) for k in BST}
w('<section class="refsec" id="tickets"><div class="wrap"><h2 class="big">Tickets</h2>')
w('<p class="lead">What is bought, what is not, and what to do at each gate. Numbers and PINs are on every row.</p>')
w('<div class="chips">')
for k,(kcol,klab) in BST.items():
    if counts[k]: w(f'<span class="chip" style="--t:{kcol};--tbg:{rgba(kcol,.07)};--tbd:{rgba(kcol,.22)};font-size:14.5px;padding:7px 13px">{counts[k]} {E(klab.lower())}</span>')
w('</div>')
for c in cities:
    cid=c["id"]
    rows=[it for it in items if it[1]==cid and it[0] in bookings]
    if not rows: continue
    w(f'<div class="grouphead"><span class="gi" style="background:{c["color"]}">{ic("ticket",22)}</span><h3>{E(c["name"])}</h3></div>')
    for it in rows:
        pid,_,d,slot,cat,title,one,tip,story,far=it
        b=bookings[pid]; bcol,_=BST[b["state"]]
        w(f'<div class="row" id="ticket-{pid}"><div class="side">')
        w(f'<span class="pill2" style="background:{bcol}">{E(b["pill"])}</span>')
        w(f'<div class="when">{E(b["when"])}</div><div class="clock">{ic("clock",14)}{E(b["clock"])}</div></div><div>')
        w(f'<h4>{E(title)}<a href="#day-{cid}-{d}">↑ in the plan</a></h4>')
        w(chips(b["chips"]))
        w(f'<p class="line">{E(b["line"])}</p>')
        if b.get("ref"): w(f'<div class="ref">{E(b["ref"])}</div>')
        w(fine(b["fine"]))
        w('</div></div>')
w('</div></section>')

# ================= prep =================
w('<section class="refsec" id="prep"><div class="wrap"><h2 class="big">Before you fly</h2>')
w('<p class="lead">Six things to have sorted. Nothing else needs doing.</p><div class="tiles">')
for p in prep:
    w(f'<div class="tile"><div class="th"><span class="ti">{ic(p["icon"],22)}</span><b>{E(p["t"])}</b></div>')
    w(chips(p["chips"]))
    w(f'<p class="line">{E(p["line"])}</p>')
    w(fine(p["fine"],"More"))
    w('</div>')
w('</div></div></section>')

# ================= stories =================
w('<section class="stories" id="stories"><div class="wrap"><h2 class="big">The stories</h2>')
w('<p class="lead">The long version, in day order. Read these on the train, not on the street.</p>')
for c in cities:
    cid=c["id"]
    w(f'<div class="storycity" id="stories-{cid}"><h3 style="background:{c["color"]}">{E(c["name"])}</h3>')
    for it in [i for i in items if i[1]==cid and i[8]]:
        pid,_,d,slot,cat,title,one,tip,story,far=it
        ccol,i2,lab=CAT[cat]
        p=P.get(pid,{})
        credit=(f'<div class="credit"><a href="{p["imgpage"]}" target="_blank" rel="noopener">Photo: Wikimedia Commons</a></div>'
                if p.get("imgpage") else '')
        w(f'<article class="story" id="story-{pid}"><div><div class="ph" style="border-top-color:{ccol}">{img(pid)}'
          f'<span class="badge" style="background:{ccol}">{i2}</span></div>{credit}</div>')
        w(f'<div><h4>{E(title)}</h4><div class="when"><b>{days[cid][d][0]}</b><span>{E(slot)}</span><span>{lab}</span></div>')
        for para in story.split("\n\n"): w(f'<p>{E(para)}</p>')
        if tip: w(f'<p class="tip">{E(tip)}</p>')
        w(f'<a class="back" style="color:{c["color"]}" href="#day-{cid}-{d}">↑ Back to {days[cid][d][0]}</a></div></article>')
    w('</div>')
w('</div></section>')
w('<footer><div class="wrap">Last updated '+datetime.date.today().strftime('%-d %B %Y')
  +' · Photos from Wikimedia Commons, showing the place or the dish, not always the exact venue.</div></footer>')

# ================= map =================
mapdata={}
hotelpins={"beijing":(39.9405,116.3935),"xian":(34.2610,108.9455),"chengdu":(30.6640,104.0435),"chongqing":(29.5610,106.5690)}
for c in cities:
    cid=c["id"]; n=0; pts=[]
    for it in items:
        if it[1]!=cid or it[4]=="transit": continue
        n+=1; p=P[it[0]]
        pts.append(dict(n=n,lat=p["lat"],lng=p["lng"],title=it[5],day=days[cid][it[2]][0],slot=it[3],col=CAT[it[4]][0],far=it[9],id=it[0]))
    mapdata[cid]=dict(pts=pts,hotel=hotelpins[cid],hname=c["hotel"])
w('<script>const DATA='+json.dumps(mapdata,ensure_ascii=False)+';')
w(r"""
for(const [cid,d] of Object.entries(DATA)){
  const m=L.map('lmap-'+cid,{scrollWheelZoom:false});
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}).addTo(m);
  const b=[];
  L.marker(d.hotel,{icon:L.divIcon({className:'',html:'<div class="mk star">\u{1F3E8}</div>',iconSize:[37,37],iconAnchor:[18,18]}),zIndexOffset:1000}).addTo(m).bindPopup('<b>Hotel</b><br>'+d.hname);
  b.push(d.hotel);
  for(const p of d.pts){
    L.marker([p.lat,p.lng],{icon:L.divIcon({className:'',html:'<div class="mk" style="background:'+p.col+'">'+p.n+'</div>',iconSize:[29,29],iconAnchor:[15,15]})}).addTo(m)
     .bindPopup('<b>'+p.n+'. '+p.title+'</b><br>'+p.day+' · '+p.slot+'<br><a href="#story-'+p.id+'">Read the story</a>');
    if(!p.far) b.push([p.lat,p.lng]);
  }
  m.fitBounds(b,{padding:[30,30]});
}
</script></body></html>""")
open("China-Must-Do-List-Tarek.html","w").write("\n".join(out))
print("ok", len(items), "items")
