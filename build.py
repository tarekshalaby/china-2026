import json, html, datetime
from data import cities, days, items
P=json.load(open("places.json"))
P["aperture"]["img"]=P["maochengdu"]["img"]; P["aperture"]["imgpage"]=P["maochengdu"]["imgpage"]
CAT={"struggle":("#E53935","✊","People's history"),"music":("#8E24AA","🎸","Live music"),"food":("#FB8C00","🍜","Local food"),"landmark":("#1E88E5","🏛️","Landmark, reframed"),"transit":("#607D8B","🚄","Travel")}
E=html.escape

def img(pid,cls=""):
    p=P.get(pid)
    if p and p.get("img"):
        return f'<img class="{cls}" src="{p["img"]}" alt="{E(p["name"])}" loading="lazy">'
    return f'<div class="{cls} noimg"></div>'

out=[]
w=out.append
w("""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>China, the people's version — 20 Sep to 3 Oct 2026</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
:root{--ink:#202124;--muted:#5f6368;--line:#e0e0e0;--bg:#fff}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:17px;line-height:1.5;color:var(--ink);background:var(--bg)}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
header.top{padding:56px 0 24px}
header.top h1{font-size:clamp(40px,6vw,76px);line-height:.98;letter-spacing:-.02em;margin:0 0 14px;font-weight:800}
header.top .dates{font-size:20px;color:var(--muted);margin:0 0 28px}
.citynav{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 28px}
.citynav a{display:block;padding:18px 16px;color:#fff;text-decoration:none;font-weight:700;font-size:20px;border-radius:10px}
.citynav a span{display:block;font-weight:400;font-size:14px;opacity:.9;margin-top:2px}
.legend{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;padding:16px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.legend .chip{display:inline-flex;align-items:center;gap:8px;font-size:15px}
.legend .dot{width:30px;height:30px;border-radius:50%;display:inline-grid;place-items:center;color:#fff;font-size:15px}
.legend .how{margin-left:auto;font-size:15px;color:var(--muted)}
.legend .how a{color:var(--ink)}
.notice{background:#FFF8E1;border-left:6px solid #F9A825;padding:16px 20px;margin:28px 0 0;border-radius:0 10px 10px 0;font-size:16px}
.notice b{display:block;margin-bottom:4px}

section.city{margin-top:64px}
.cityhead{color:#fff;padding:40px 0 34px;position:relative}
.cityhead h2{font-size:clamp(44px,7vw,88px);line-height:.95;letter-spacing:-.025em;margin:0;font-weight:800}
.cityhead .meta{display:flex;flex-wrap:wrap;gap:6px 28px;margin-top:14px;font-size:17px}
.cityhead .meta b{font-weight:700}
.cityhead .sub{font-size:22px;margin-top:10px;opacity:.95}
.cityhead .quick{position:absolute;right:24px;top:44px;display:flex;gap:8px}
.cityhead .quick a{color:#fff;text-decoration:none;border:1.5px solid rgba(255,255,255,.7);padding:6px 12px;border-radius:999px;font-size:14px}

.day{display:grid;grid-template-columns:120px 1fr;gap:0 28px;padding:34px 0 10px;border-top:1px solid var(--line)}
.day:first-of-type{border-top:0}
.datecol{position:sticky;top:16px;align-self:start}
.datecol .wd{font-size:15px;color:var(--muted)}
.datecol .dn{font-size:52px;line-height:1;font-weight:800;letter-spacing:-.03em}
.datecol .mo{font-size:16px;font-weight:700}
.datecol .theme{margin-top:12px;font-size:15px;line-height:1.35;padding-left:10px;border-left:4px solid}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:18px;margin-bottom:20px}
.card{border-radius:12px;overflow:hidden;background:#fff;border:1px solid var(--line);display:flex;flex-direction:column;border-top:7px solid}
.card .ph{position:relative;aspect-ratio:16/10;background:#eceff1;overflow:hidden}
.card .ph img,.card .ph .noimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.card .badge{position:absolute;left:10px;top:10px;width:38px;height:38px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:18px;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.card .num{position:absolute;right:10px;top:10px;min-width:30px;height:30px;padding:0 8px;border-radius:15px;background:#202124;color:#fff;font-weight:700;display:grid;place-items:center;font-size:15px}
.card .bd{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.card .slot{font-size:13px;font-weight:700;letter-spacing:.02em}
.card h4{margin:0;font-size:19px;line-height:1.2;letter-spacing:-.01em}
.card .one{margin:0;font-size:15.5px;line-height:1.4}
.card .tip{margin:2px 0 0;font-size:14px;color:var(--muted);line-height:1.4;padding-left:18px;position:relative}
.card .tip:before{content:"↳";position:absolute;left:0;top:0}
.card .more{margin-top:auto;padding-top:8px;font-size:14px;font-weight:700;text-decoration:none}
.card .more:hover{text-decoration:underline}
.transit{grid-column:1/-1;display:flex;align-items:center;gap:16px;background:#ECEFF1;border-radius:12px;padding:14px 18px;border-left:7px solid #607D8B}
.transit .ic{font-size:28px}
.transit b{font-size:18px}
.transit .one{color:var(--ink);font-size:15.5px}
.transit .tip{color:var(--muted);font-size:14px}

.mapblock{margin:20px 0 0;padding-top:28px;border-top:1px solid var(--line)}
.mapblock h3{font-size:28px;margin:0 0 6px;letter-spacing:-.015em}
.mapblock p{margin:0 0 14px;color:var(--muted);font-size:15px}
.map{height:520px;border-radius:14px;border:1px solid var(--line)}
.mk{width:30px;height:30px;border-radius:50%;color:#fff;font-weight:800;font-size:14px;display:grid;place-items:center;border:2.5px solid #fff;box-shadow:0 1px 5px rgba(0,0,0,.4)}
.mk.star{width:38px;height:38px;font-size:22px;background:#202124}
.leaflet-popup-content{font-family:inherit;font-size:14px;line-height:1.35}
.leaflet-popup-content b{font-size:15px}
.far{margin:12px 0 0;font-size:15px;color:var(--muted)}
.far span{display:inline-block;margin-right:14px}

section.stories{margin-top:96px;padding-bottom:80px}
section.stories>.wrap>h2{font-size:clamp(40px,6vw,72px);letter-spacing:-.025em;line-height:1;margin:0 0 8px;font-weight:800}
section.stories>.wrap>p.lead{font-size:20px;color:var(--muted);margin:0 0 40px;max-width:720px}
.storycity{margin-top:56px}
.storycity h3{font-size:30px;margin:0 0 20px;padding:10px 16px;color:#fff;border-radius:8px;display:inline-block}
.story{display:grid;grid-template-columns:280px 1fr;gap:24px;padding:26px 0;border-top:1px solid var(--line);scroll-margin-top:16px}
.story .ph{border-radius:10px;overflow:hidden;aspect-ratio:4/3;background:#eceff1;position:relative;border-top:7px solid}
.story .ph img,.story .ph .noimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.story .ph .badge{position:absolute;left:10px;top:10px;width:38px;height:38px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:18px}
.story h4{margin:0 0 4px;font-size:24px;letter-spacing:-.015em;line-height:1.15}
.story .when{font-size:14px;color:var(--muted);margin-bottom:12px}
.story .when b{color:var(--ink)}
.story p{margin:0 0 10px;max-width:70ch;font-size:17px}
.story .tip{color:var(--muted);font-size:15px;padding-left:18px;position:relative;max-width:70ch}
.story .tip:before{content:"↳";position:absolute;left:0}
.story .back{font-size:14px;text-decoration:none;font-weight:700;display:inline-block;margin-top:10px}
.story .credit{font-size:12px;color:var(--muted);margin-top:6px}
.story .credit a{color:var(--muted)}
footer{border-top:1px solid var(--line);padding:24px 0 48px;font-size:14px;color:var(--muted)}
@media (max-width:760px){.citynav{grid-template-columns:1fr 1fr}.day{grid-template-columns:1fr}.datecol{position:static;display:flex;gap:12px;align-items:baseline;margin-bottom:14px}.datecol .dn{font-size:36px}.datecol .theme{border-left:0;padding-left:0;margin-top:0}.story{grid-template-columns:1fr}.cityhead .quick{position:static;margin-top:16px}.legend .how{margin-left:0}.map{height:400px}}
@media print{.map,.citynav,.quick{display:none}.card{break-inside:avoid}.story{break-inside:avoid}}
</style></head><body>
""")

# header
w('<header class="top"><div class="wrap">')
w('<h1>China, the people\'s version</h1>')
w('<p class="dates">Beijing · Xi\'an · Chengdu · Chongqing &nbsp;—&nbsp; 20 September to 3 October 2026 &nbsp;—&nbsp; Tarek\'s must-do list</p>')
w('<nav class="citynav">')
for c in cities:
    w(f'<a href="#{c["id"]}" style="background:{c["color"]}">{c["name"]}<span>{c["dates"]} · {c["nights"]} nights</span></a>')
w('</nav>')
w('<div class="legend">')
for k,(col,ic,lab) in CAT.items():
    w(f'<span class="chip"><span class="dot" style="background:{col}">{ic}</span>{lab}</span>')
w('<span class="how">Numbers on the cards match the pins on each city map. <a href="#stories">Full backstories</a> are at the bottom.</span>')
w('</div>')
w('<div class="notice"><b>Timing warning: Chongqing falls on National Day.</b>30 September is Martyrs\' Day and 1 October starts Golden Week. Hongyadong, Ciqikou and Liziba will be jammed; security around monuments is heavy. Do the crowd-magnets before 09:00 or after 21:00. Tiananmen Square needs an advance reservation with passport details (WeChat mini-program), and Forbidden City and Panda Base tickets sell out days ahead. Install Showstart 秀动 and Damai 大麦 for gig tickets, and Amap 高德 for navigation.</div>')
w('</div></header>')

# cities
for c in cities:
    cid=c["id"]; col=c["color"]
    citems=[it for it in items if it[1]==cid]
    nums={}; n=0
    for it in citems:
        if it[4]!="transit": n+=1; nums[it[0]]=n
    w(f'<section class="city" id="{cid}"><div class="cityhead" style="background:{col}"><div class="wrap">')
    w(f'<h2>{E(c["name"])}</h2><div class="sub">{E(c["sub"])}</div>')
    w(f'<div class="meta"><span><b>{c["dates"]}</b> · {c["nights"]} nights</span><span>Hotel: {E(c["hotel"])}</span></div>')
    w(f'<div class="quick"><a href="#map-{cid}">Map</a><a href="#stories-{cid}">Stories</a></div>')
    w('</div></div><div class="wrap">')
    for di,(dlabel,theme) in enumerate(days[cid]):
        wd,dn,mo=dlabel.split()
        w(f'<div class="day" id="day-{cid}-{di}"><div class="datecol"><div class="wd">{wd}</div><div class="dn">{dn}</div><div class="mo">{mo}</div><div class="theme" style="border-color:{col}">{E(theme)}</div></div><div class="cards">')
        for it in citems:
            pid,_,d,slot,cat,title,one,tip,story,far=it
            if d!=di: continue
            ccol,ic,lab=CAT[cat]
            if cat=="transit":
                w(f'<div class="transit"><span class="ic">{ic}</span><div><b>{E(title)}</b> <span class="slot" style="color:#607D8B;font-weight:700"> {E(slot)}</span><div class="one">{E(one)}</div><div class="tip">{E(tip)}</div></div></div>')
                continue
            farlab=' <span style="font-weight:400;color:#5f6368">(out of town)</span>' if far else ''
            w(f'<article class="card" style="border-top-color:{ccol}"><div class="ph">{img(pid)}<span class="badge" style="background:{ccol}" title="{lab}">{ic}</span><span class="num">{nums[pid]}</span></div>')
            w(f'<div class="bd"><div class="slot" style="color:{ccol}">{E(slot)}{farlab}</div><h4>{E(title)}</h4><p class="one">{E(one)}</p>')
            if tip: w(f'<p class="tip">{E(tip)}</p>')
            if story: w(f'<a class="more" style="color:{ccol}" href="#story-{pid}">Read the story</a>')
            w('</div></article>')
        w('</div></div>')
    # map
    w(f'<div class="mapblock" id="map-{cid}"><h3>{E(c["name"])} on the map</h3><p>Pins are numbered like the cards and coloured by category. Tap a pin for the name and the day. The black pin is your hotel.</p><div class="map" id="lmap-{cid}"></div>')
    fars=[it for it in citems if it[9]]
    if fars:
        w('<p class="far">Out of town, off the edge of the map: '+" ".join(f'<span><b>{nums[it[0]]}</b> {E(it[5])}</span>' for it in fars)+'</p>')
    w('</div></div></section>')

# stories
w('<section class="stories" id="stories"><div class="wrap"><h2>The stories behind each stop</h2><p class="lead">The long version, in the same order as the days. Read on the train, not on the street; most of what follows is not for conversation with strangers.</p>')
for c in cities:
    cid=c["id"]
    w(f'<div class="storycity" id="stories-{cid}"><h3 style="background:{c["color"]}">{E(c["name"])}</h3>')
    for it in [i for i in items if i[1]==cid and i[8]]:
        pid,_,d,slot,cat,title,one,tip,story,far=it
        ccol,ic,lab=CAT[cat]
        p=P.get(pid,{})
        credit=f'<div class="credit">Photo: <a href="{p["imgpage"]}" target="_blank" rel="noopener">Wikimedia Commons</a></div>' if p.get("imgpage") else ''
        w(f'<article class="story" id="story-{pid}"><div><div class="ph" style="border-top-color:{ccol}">{img(pid)}<span class="badge" style="background:{ccol}">{ic}</span></div>{credit}</div>')
        w(f'<div><h4>{E(title)}</h4><div class="when"><b>{days[cid][d][0]}</b> · {E(slot)} · {lab}</div>')
        for para in story.split("\n\n"): w(f'<p>{E(para)}</p>')
        if tip: w(f'<p class="tip">{E(tip)}</p>')
        w(f'<a class="back" style="color:{c["color"]}" href="#day-{cid}-{d}">Back to {days[cid][d][0]}</a></div></article>')
    w('</div>')
w('</div></section>')
w('<footer><div class="wrap">Last updated '+datetime.date.today().strftime('%-d %B %Y')+' · Built from the visa itinerary (flights, hotels and trains as booked). Photos are from Wikimedia Commons and show the place or the dish, not always the exact venue. Gig listings change weekly: check Showstart about ten days before each city.</div></footer>')

# map data
mapdata={}
hotels={"beijing":(39.9405,116.3935),"xian":(34.2610,108.9455),"chengdu":(30.6640,104.0435),"chongqing":(29.5610,106.5690)}
for c in cities:
    cid=c["id"]; n=0; pts=[]
    for it in items:
        if it[1]!=cid or it[4]=="transit": continue
        n+=1; p=P[it[0]]
        pts.append(dict(n=n,lat=p["lat"],lng=p["lng"],title=it[5],day=days[cid][it[2]][0],slot=it[3],col=CAT[it[4]][0],far=it[9],id=it[0]))
    mapdata[cid]=dict(pts=pts,hotel=hotels[cid],hname=c["hotel"])
w('<script>const DATA='+json.dumps(mapdata,ensure_ascii=False)+';')
w("""
for(const [cid,d] of Object.entries(DATA)){
  const m=L.map('lmap-'+cid,{scrollWheelZoom:false});
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}).addTo(m);
  const b=[];
  L.marker(d.hotel,{icon:L.divIcon({className:'',html:'<div class="mk star">🏨</div>',iconSize:[38,38],iconAnchor:[19,19]}),zIndexOffset:1000}).addTo(m).bindPopup('<b>Hotel</b><br>'+d.hname);
  b.push(d.hotel);
  for(const p of d.pts){
    L.marker([p.lat,p.lng],{icon:L.divIcon({className:'',html:'<div class="mk" style="background:'+p.col+'">'+p.n+'</div>',iconSize:[30,30],iconAnchor:[15,15]})}).addTo(m)
     .bindPopup('<b>'+p.n+'. '+p.title+'</b><br>'+p.day+' · '+p.slot+'<br><a href="#story-'+p.id+'">Read the story</a>');
    if(!p.far) b.push([p.lat,p.lng]);
  }
  m.fitBounds(b,{padding:[30,30]});
}
</script></body></html>""")
open("China-Must-Do-List-Tarek.html","w").write("\n".join(out))
print("ok", sum(1 for i in items), "items")
