# -*- coding: utf-8 -*-
# Generator for the China 2026 site. Mobile first: five views, a fixed tab bar,
# stops as rows that open a full-screen story sheet. One file, nothing reloads.
import json, html, datetime, re
from urllib.parse import urlencode
from data import (cities, days, items, bookings, flights, trains, hotels, prep,
                  nextup, ribbon, bands, heroes)

P = json.load(open("places.json"))
P["aperture"]["img"] = P["maochengdu"]["img"]; P["aperture"]["imgpage"] = P["maochengdu"]["imgpage"]

CAT = {"struggle": ("#E53935", "✊", "People's history"),
       "music":    ("#8E24AA", "\U0001F3B8", "Live music"),
       "food":     ("#FB8C00", "\U0001F35C", "Local food"),
       "landmark": ("#1E88E5", "\U0001F3DB️", "Landmark, reframed"),
       "transit":  ("#607D8B", "\U0001F684", "Travel")}
BST  = {"booked": ("#2E7D32", "Booked"), "todo": ("#C62828", "Still to book"),
        "gate": ("#546E7A", "Pay at the gate")}
TONE = {"k": "#2E7D32", "w": "#E65100", "n": "#455A64"}
CCOL = {c["id"]: c["color"] for c in cities}; CCOL["air"] = "#90A4AE"
CBY  = {c["id"]: c for c in cities}
MONTH = {"Sep": "09", "Oct": "10"}
E = html.escape

def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def rgba(h, a):
    r, g, b = rgb(h); return f'rgba({r},{g},{b},{a})'

ICON = {
 "plane":'<path d="M21 15.6v-2.1l-7.6-4.4V4.4a1.4 1.4 0 0 0-2.8 0v4.7L3 13.5v2.1l7.6-2.4v3.7l-2.2 1.6v1.4L12 18.8l3.6 1.1v-1.4l-2.2-1.6v-3.7z"/>',
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
 "cal":'<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "map":'<path d="M9 3 3 5.6v15.2L9 18l6 3 6-2.6V3.2L15 6z"/><path d="M9 3v15M15 6v15"/>',
 "taxi":'<path d="M4 16.5h16M5.5 16.5v2.2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-6l2.2-5A2 2 0 0 1 7 6.2h10a2 2 0 0 1 1.8 1.3l2.2 5v6a1 1 0 0 1-1 1h-.5a1 1 0 0 1-1-1v-2.2"/><path d="M3.2 12.2h17.6M9 6.2V4.2h6v2"/><circle cx="7.4" cy="14.4" r=".9" fill="currentColor" stroke="none"/><circle cx="16.6" cy="14.4" r=".9" fill="currentColor" stroke="none"/>',
 "close":'<path d="M6 6l12 12M18 6L6 18"/>',
 "chev":'<path d="M9 5l7 7-7 7"/>',
 "left":'<path d="M15 5l-7 7 7 7"/>',
 "copy":'<rect x="8.5" y="8.5" width="12" height="12" rx="2.5"/><path d="M15.5 5.5h-9a2 2 0 0 0-2 2v9"/>',
 "up":'<path d="M12 19V5M5 12l7-7 7 7"/>',
 "nav":'<path d="M3.4 11.2 20.6 4.1a.7.7 0 0 1 .9.9l-7.1 17.2a.7.7 0 0 1-1.3-.1l-2-6.6-6.6-2a.7.7 0 0 1-.1-1.3z"/>',
}
# Icons are defined once as a <symbol> sprite and referenced with <use>: 605 uses across
# the page, so inlining each one costs ~110KB of markup and several thousand DOM nodes.
def sprite():
    parts = ['<svg class="sprite" aria-hidden="true" focusable="false"><defs>']
    for name, body in ICON.items():
        parts.append(f'<symbol id="i-{name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                     f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{body}</symbol>')
    parts.append('</defs></svg>')
    return ''.join(parts)

def ic(name, size=22, cls=""):
    c = f'i {cls}'.strip()
    return (f'<svg class="{c}" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#i-{name}"/></svg>')

# Getting directions in China is a coordinate-system trap. Amap draws on GCJ-02, the
# mandated offset grid; our coordinates are WGS-84 from OpenStreetMap, so handing them to
# Amap puts every pin 300-500m out. Converting is easy enough, but it does not help: an
# audit of these 86 places found 26 stored coarsely enough to be 60-740m wrong at source,
# and OpenStreetMap has no record at all for 13 of them (交通茶馆, 重庆工业博物馆,
# 红卫兵墓园, MAO Livehouse). Fuzzy geocoding made it worse, not better — "足疗 西安市"
# matched a foot massage shop in Toronto.
#
# So we are not the source of truth. The links search Amap's own POI database by Chinese
# name, scoped to the city. Amap knows exactly where 交通茶馆 is; we do not. That also
# handles chains properly: 南城香 has 160 branches, and a search sorts them by distance
# from wherever you are standing, which a single pin never could.
#
# Everything on the site's own Leaflet map stays WGS-84, which is correct for OSM tiles.
# The two systems never meet, which is the point.
CITYCN = {"beijing": "北京市", "xian": "西安市", "chengdu": "成都市", "chongqing": "重庆市"}
# Chinese characters and digits only: names like 大华1935 need the digits, but letting
# Latin in drags trailing English into the query ("王府井 and St Joseph"). A title naming
# two places splits into two runs here, and the longest one is what the stop is about.
_CJK = re.compile(r'[\u4e00-\u9fff][\u4e00-\u9fff0-9]*')

def amap_keyword(title):
    """The Chinese name out of a title like 'Jiaotong Teahouse 交通茶馆 · 黄桷坪'.
    Amap matches one POI at a time, so a title naming two places yields the longer name."""
    hits = _CJK.findall(title or "")
    return max(hits, key=len) if hits else (title or "").strip()

def amap_url(keyword, city):
    if not keyword: return ""
    return "https://uri.amap.com/search?" + urlencode(
        {"keyword": keyword, "city": CITYCN[city], "src": "china2026",
         "coordinate": "gaode", "callnative": "1"})

def amap_for(title, city, pid=None):
    """places.json may carry an explicit "amap" term where the derived one is wrong."""
    p = P.get(pid) if pid else None
    return amap_url((p or {}).get("amap") or amap_keyword(title), city)

def img(pid, cls=""):
    p = P.get(pid)
    if p and p.get("img"):
        return f'<img class="{cls}" src="{p["img"]}" alt="{E(p["name"])}" loading="lazy" decoding="async">'
    return f'<div class="{cls} noimg"></div>'

def chips(cs, big=False):
    if not cs: return ''
    k = ' big' if big else ''
    return f'<div class="chips{k}">' + ''.join(
      f'<span class="chip" style="--t:{TONE[t]};--tbg:{rgba(TONE[t],.07)};--tbd:{rgba(TONE[t],.22)}">{E(v)}</span>'
      for t, v in cs) + '</div>'

def fine(ps, label="The small print"):
    if not ps: return ''
    return ('<details class="fine"><summary>' + E(label) + '</summary>'
            + ''.join(f'<p>{p}</p>' for p in ps) + '</details>')

def copyable(text, label):
    """A monospace value you can tap to copy. The panic-item pattern."""
    return (f'<button class="cp" type="button" data-copy="{E(text)}" aria-label="Copy {E(label)}">'
            f'<span>{E(text)}</span>{ic("copy",15)}</button>')

# ---- day index: (city, day-number, month) -> day slot, plus ISO dates for "today" ----
DAYKEY = {}
for _cid in days:
    for _di, (_lbl, _th) in enumerate(days[_cid]):
        _wd, _dn, _mo = _lbl.split()
        DAYKEY[(_cid, _dn, _mo)] = _di

def isoof(dn, mo):
    return f'2026-{MONTH[mo]}-{int(dn):02d}'

# The two flying days are real days with real content, so they get real blocks in the Plan.
# Without them the rail had 15 chips for 13 days and the odd two had to jump you to another
# tab, which is disorienting. Every chip now scrolls within the Plan.
AIR_ISO = [isoof(dn, mo) for cid, dn, mo in ribbon if cid == "air"]

def seg_iso(datestr):
    _wd, _dn, _mo = datestr.split()
    return isoof(_dn, _mo)

# A segment belongs to the last flying day that has already begun, so the overnight
# Cairo-Doha-Beijing pair sits together under 19 Sep rather than splitting across two days.
AIRSEGS = {a: [] for a in AIR_ISO}
for _g in flights["segs"]:
    _gi = seg_iso(_g["date"])
    _owner = AIR_ISO[0]
    for _a in AIR_ISO:
        if _a <= _gi: _owner = _a
    AIRSEGS[_owner].append(_g)

# day blocks in the order the Plan renders them
BLOCKS = [(AIR_ISO[0], "day-air-0")]
for _c in cities:
    for _di, (_lbl, _th) in enumerate(days[_c["id"]]):
        _wd, _dn, _mo = _lbl.split()
        BLOCKS.append((isoof(_dn, _mo), f'day-{_c["id"]}-{_di}'))
BLOCKS.append((AIR_ISO[-1], "day-air-1"))

# 24, 27 and 30 Sep each appear twice — you start the day in one city and end it in the
# next. A chip must land on the first block for the date, or you skip that last morning.
FIRSTBLOCK = {}
for _iso, _bid in BLOCKS:
    FIRSTBLOCK.setdefault(_iso, _bid)

# A band is written as grid columns a..b, and column n is ribbon day n-1. The bands used to
# be their own row above the day chips; they are now a cap on the chips themselves, which
# is where the row the city buttons needed came from.
HOL = {}
for _lbl, _col, _a, _b in bands:
    for _i in range(_a - 1, _b - 1):
        HOL[_i] = (_lbl, _col)

# ...and the name the rail no longer carries goes on the city header, narrowed to the days
# you are actually in that city: "Mid-Autumn 25-26 Sep" on Xi'an, "27 Sep" on Chengdu.
CITYHOL = {}
for _i, (_cid, _dn, _mo) in enumerate(ribbon):
    if _i in HOL and _cid != "air":
        CITYHOL.setdefault(_cid, {}).setdefault(HOL[_i][0], []).append((_dn, _mo))
def holchips(cid):
    out = []
    for _lbl, _ds in CITYHOL.get(cid, {}).items():
        (_d0, _m0), (_d1, _m1) = _ds[0], _ds[-1]
        span = f'{_d0} {_m0}' if _ds[0] == _ds[-1] else (
               f'{_d0}\u2013{_d1} {_m1}' if _m0 == _m1 else f'{_d0} {_m0} \u2013 {_d1} {_m1}')
        out.append(f'{_lbl} {span}')
    return out

# stop order across the whole trip, for the sheet's prev/next
ORDER = [it[0] for it in items if it[8]]
NUMS = {}
for _c in cities:
    _n = 0
    for _it in items:
        if _it[1] != _c["id"] or _it[4] == "transit": continue
        _n += 1; NUMS[_it[0]] = _n

HOTELCN = {h["city"]: h["addrcn"] for h in hotels}

out = []; w = out.append

w("""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#ffffff">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="China 2026">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>China, the people's version — 20 Sep to 3 Oct 2026</title>
<style>
:root{
 --ink:#1a1c1e;--muted:#5f6368;--line:#e3e5e8;--soft:#f6f7f8;--bg:#fff;
 --app:54px;--tab:58px;--tabh:0px;--gut:16px;
 --sat:env(safe-area-inset-top,0px);--sab:env(safe-area-inset-bottom,0px);
 --stick:calc(var(--app) + var(--sat) + var(--tabh));
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:400 16px/1.5 "Helvetica Neue",Helvetica,Arial,sans-serif;color:var(--ink);
 background:var(--bg);-webkit-font-smoothing:antialiased;overscroll-behavior-y:none}
body.locked{overflow:hidden}
a{color:inherit}
button{font:inherit;color:inherit;background:none;border:0;padding:0;margin:0;text-align:left;
 cursor:pointer;-webkit-tap-highlight-color:transparent}
img{max-width:100%}
svg.i{flex:none;display:block}
.sprite{position:absolute;width:0;height:0;overflow:hidden}
.noimg{background:#eceff1}
.wrap{padding:0 var(--gut)}
h2.big{font-size:30px;letter-spacing:-.03em;line-height:1.04;margin:0 0 5px;font-weight:800}
p.lead{font-size:16px;color:var(--muted);margin:0 0 18px;max-width:62ch}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* ---------------- top bar ---------------- */
.appbar{position:fixed;top:0;left:0;right:0;z-index:60;background:rgba(255,255,255,.93);
 -webkit-backdrop-filter:saturate(1.7) blur(14px);backdrop-filter:saturate(1.7) blur(14px);
 border-bottom:1px solid var(--line);padding-top:var(--sat)}
.abrow{height:var(--app);display:flex;align-items:center;gap:10px;padding:0 var(--gut)}
.brand{font-weight:800;letter-spacing:-.025em;font-size:16.5px;line-height:1.05;text-decoration:none;flex:none}
.brand span{display:block;font-weight:400;font-size:11px;color:var(--muted);letter-spacing:.02em;margin-top:1px}
.taxi{margin-left:auto;display:inline-flex;align-items:center;gap:7px;border:1.5px solid var(--line);
 border-radius:999px;padding:0 13px;height:40px;font-size:13.5px;font-weight:700;flex:none}
.taxi:active{background:var(--soft)}

/* ---------------- tab bar ---------------- */
.tabs{position:fixed;left:0;right:0;bottom:0;z-index:60;
 background:rgba(255,255,255,.95);-webkit-backdrop-filter:saturate(1.7) blur(14px);
 backdrop-filter:saturate(1.7) blur(14px);border-top:1px solid var(--line);padding-bottom:var(--sab)}
.tabin{display:grid;grid-template-columns:repeat(5,1fr)}
.tabs button{position:relative;height:var(--tab);display:flex;flex-direction:column;align-items:center;
 justify-content:center;gap:3px;color:var(--muted);font-size:10.5px;font-weight:700;letter-spacing:.01em}
.tabs button b{font-weight:700}
.tabs button[aria-selected=true]{color:var(--ink)}
.tabs button[aria-selected=true]:before{content:"";position:absolute;top:0;left:50%;width:32px;height:3px;
 margin-left:-16px;border-radius:0 0 3px 3px;background:var(--ink)}
.tabs .bub{position:absolute;top:7px;left:calc(50% + 8px);min-width:16px;height:16px;padding:0 4px;
 border-radius:8px;background:#C62828;color:#fff;font-size:10px;font-weight:800;display:grid;place-items:center}

main{padding-top:var(--stick);padding-bottom:calc(var(--tab) + var(--sab) + 26px)}
body.mapview main{padding-bottom:0}
body.mapview footer{display:none}
.view{display:none}
.view.on{display:block}

/* ---------------- sticky sub-navs ---------------- */
.sub{position:sticky;top:var(--stick);z-index:50;background:rgba(255,255,255,.96);
 -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.scroller{display:flex;gap:7px;overflow-x:auto;padding:9px var(--gut);scrollbar-width:none;
 -webkit-overflow-scrolling:touch}
.scroller::-webkit-scrollbar{display:none}
.seg{flex:none;border:1.5px solid var(--line);border-radius:999px;padding:0 14px;height:40px;
 display:inline-flex;align-items:center;gap:6px;font-size:13.5px;font-weight:700;white-space:nowrap;
 text-decoration:none}
.seg[aria-pressed=true],.seg.on{background:var(--ink);border-color:var(--ink);color:#fff}
.seg .sd{width:9px;height:9px;border-radius:50%;background:var(--c);flex:none}
.seg[aria-pressed=true] .sd,.seg.on .sd{box-shadow:0 0 0 2px rgba(255,255,255,.55)}

/* city jump. Four buttons, no sideways scroll: every city is one tap from anywhere in
   the Plan. It sits where the holiday bands used to, so the rail is no taller than before. */
.crow{display:flex;gap:5px;padding:6px var(--gut) 0}
.crow button{flex:1 1 auto;min-width:0;height:30px;border-radius:9px;display:flex;align-items:center;
 justify-content:center;gap:6px;font-size:12px;font-weight:800;letter-spacing:-.02em;color:var(--muted);
 background:var(--soft);white-space:nowrap;overflow:hidden}
.crow button i{width:8px;height:8px;border-radius:50%;background:var(--c);flex:none}
.crow button.here{background:var(--c);color:#fff}
.crow button.here i{background:rgba(255,255,255,.9)}
.crow button:active{transform:scale(.97)}

/* day rail */
.rail{overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:4px var(--gut) 7px}
.rail::-webkit-scrollbar{display:none}
.railin{display:grid;grid-template-columns:repeat(15,46px);gap:4px}
.rd{background:var(--c);color:#fff;border-radius:10px;padding:5px 2px 4px;text-align:center;
 line-height:1.05;display:block;width:46px;position:relative}
.rd b{display:block;font-size:16px;font-weight:800;letter-spacing:-.03em}
.rd span{display:block;font-size:8.5px;text-transform:uppercase;letter-spacing:.05em;opacity:.92}
/* a holiday is a cap across the top of the days it covers, named on the city header */
.rd.hol:before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--h);
 border-radius:10px 10px 0 0}
.rd.here{box-shadow:0 0 0 2px #fff,0 0 0 4px var(--ink)}
.rd.past{opacity:.4}
.rd .tdot{position:absolute;left:50%;bottom:-6px;width:5px;height:5px;margin-left:-2.5px;border-radius:50%;
 background:var(--ink)}

/* ---------------- the "needs you" strip ---------------- */
.nowstrip{display:flex;gap:11px;overflow-x:auto;scroll-snap-type:x mandatory;padding:16px var(--gut) 4px;
 scrollbar-width:none;-webkit-overflow-scrolling:touch}
.nowstrip::-webkit-scrollbar{display:none}
.nu{flex:none;width:84%;max-width:330px;scroll-snap-align:start;border:1px solid var(--line);
 border-left:4px solid var(--t);border-radius:13px;padding:13px 15px;background:#fff}
.nu .nw{font-size:11px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--t);
 display:flex;align-items:center;gap:6px}
.nu .nw em{font-style:normal;opacity:.6;letter-spacing:.03em}
.nu .nh{display:block;font-size:16px;font-weight:700;line-height:1.25;letter-spacing:-.015em;margin:5px 0 3px}
.nu .nl{display:block;font-size:13.5px;color:var(--muted);line-height:1.4}
.striphd{display:flex;align-items:baseline;gap:9px;padding:20px var(--gut) 0}
.striphd h3{font-size:14px;margin:0;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}
.striphd .cnt{font-size:12px;font-weight:800;color:#C62828}

/* countdown / today banner */
.tod{margin:16px var(--gut) 0;border-radius:13px;padding:13px 15px;background:var(--soft);
 border:1px solid var(--line);display:flex;align-items:center;gap:11px}
.tod .tdi{color:var(--muted);flex:none}
.tod b{display:block;font-size:16px;letter-spacing:-.01em}
.tod span{display:block;font-size:13.5px;color:var(--muted);line-height:1.35}

/* ---------------- city header ---------------- */
.chead{position:relative;overflow:hidden;background:var(--c);color:#fff;margin-top:30px;
 scroll-margin-top:calc(var(--stick) + 69px)}
.chead .hero{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.chead .tint{position:absolute;inset:0;
 background:linear-gradient(180deg,rgba(0,0,0,.18) 0%,rgba(0,0,0,.34) 100%),var(--g)}
.chead .in{position:relative;padding:20px var(--gut) 18px}
.chead h2{font-size:33px;line-height:.98;letter-spacing:-.03em;margin:0;font-weight:800;
 text-shadow:0 2px 16px rgba(0,0,0,.3)}
.chead .csub{font-size:15px;margin-top:6px;max-width:30ch;text-shadow:0 1px 9px rgba(0,0,0,.35);opacity:.97}
.chead .meta{display:flex;flex-wrap:wrap;gap:6px;margin-top:13px;font-size:12.5px}
.chead .meta span.hol{background:rgba(0,0,0,.45);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.5)}
.chead .meta span{background:rgba(0,0,0,.28);padding:5px 10px;border-radius:999px;display:inline-flex;
 align-items:center;gap:5px}
.chead .quick{display:flex;gap:7px;margin-top:13px}
.chead .quick button{color:#fff;background:rgba(0,0,0,.3);padding:0 13px;height:36px;border-radius:999px;
 font-size:13px;font-weight:700;display:inline-flex;align-items:center;gap:6px}
.chead.air{background:var(--c)}
.chead.air .in{padding:17px var(--gut) 15px}
.chead.air h2{font-size:25px}
.chead.air .csub{font-size:14.5px;margin-top:4px}
.jumpbtn{display:inline-flex;align-items:center;gap:7px;border:1.5px solid var(--line);border-radius:999px;
 padding:0 15px;height:42px;font-size:13.5px;font-weight:700;margin:15px 0 4px}

/* ---------------- days and stops ---------------- */
.day{scroll-margin-top:calc(var(--stick) + 69px)}
.dayhd{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;padding:22px 0 8px}
.dayhd .dn{font-size:27px;font-weight:800;letter-spacing:-.035em;line-height:1}
.dayhd .wd{font-size:12px;color:var(--muted);font-weight:800;text-transform:uppercase;letter-spacing:.07em}
.dayhd .cnt{margin-left:auto;font-size:12px;color:var(--muted);font-weight:700}
.dayhd .th{flex-basis:100%;font-size:14.5px;color:#3d4043;border-left:3px solid var(--c);padding-left:10px;
 margin-top:3px;line-height:1.35}
.stops{margin:0 0 4px}
.stop{display:grid;grid-template-columns:84px 1fr 14px;gap:12px;align-items:center;width:100%;
 padding:11px 0;border-top:1px solid var(--line)}
.stop:active{background:var(--soft)}
.stop .ph{position:relative;width:84px;aspect-ratio:1;border-radius:12px;overflow:hidden;background:#eceff1;
 align-self:start}
.stop .ph img,.stop .ph .noimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.stop .n{position:absolute;left:5px;top:5px;min-width:21px;height:21px;border-radius:11px;
 background:rgba(26,28,30,.88);color:#fff;font-size:11.5px;font-weight:800;display:grid;place-items:center;padding:0 5px}
.stop .bg{position:absolute;right:4px;bottom:4px;width:23px;height:23px;border-radius:50%;background:var(--c);
 display:grid;place-items:center;font-size:11px;box-shadow:0 1px 4px rgba(0,0,0,.3)}
.stop .tx{min-width:0}
.stop .slot{display:block;font-size:10.5px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--c)}
.stop .slot i{font-style:normal;font-weight:700;letter-spacing:0;text-transform:none;color:var(--muted)}
.stop .ttl{display:block;font-size:16.5px;font-weight:700;letter-spacing:-.018em;line-height:1.2;margin:3px 0 3px}
.stop .one{font-size:13.5px;line-height:1.36;color:var(--muted);display:-webkit-box;-webkit-line-clamp:2;
 -webkit-box-orient:vertical;overflow:hidden;margin:0}
.stop .pl{display:inline-block;margin-top:6px;font-size:10.5px;font-weight:800;color:#fff;padding:3px 9px;
 border-radius:999px;letter-spacing:.02em}
.stop .chev{color:#b9bec4;align-self:center}
.trans{display:grid;grid-template-columns:auto 1fr;gap:12px;background:var(--soft);border-radius:12px;
 padding:13px 14px;margin:11px 0;border-left:4px solid #607D8B;align-items:start}
.trans .ti{color:#607D8B;margin-top:1px}
.trans b{font-size:16px;letter-spacing:-.015em}
.trans .ts{font-size:10.5px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:#607D8B;display:block}
.trans .one{font-size:14px;margin:3px 0 0}
.trans .tip{font-size:13px;color:var(--muted);margin:5px 0 0;line-height:1.4}
.far{margin:12px 0 0;font-size:13px;color:var(--muted)}
.far b{color:var(--ink)}

/* ---------------- chips, small print, refs ---------------- */
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:12.5px;font-weight:700;color:var(--t);background:var(--tbg);border:1px solid var(--tbd);
 border-radius:8px;padding:5px 9px}
.chips.big .chip{font-size:14px;padding:7px 12px}
details.fine{margin-top:13px}
details.fine summary{font-size:13px;font-weight:700;color:var(--muted);cursor:pointer;list-style:none;
 display:inline-flex;align-items:center;gap:7px;padding:9px 14px;min-height:40px;box-sizing:border-box;
 border:1px solid var(--line);border-radius:999px}
details.fine summary::-webkit-details-marker{display:none}
details.fine summary:before{content:"+";font-size:15px;line-height:1}
details.fine[open] summary:before{content:"\\2013"}
details.fine p{font-size:14.5px;margin:12px 0 0;max-width:66ch;line-height:1.56;color:#33363a}
.cp{display:inline-flex;align-items:center;gap:8px;max-width:100%;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
 font-size:12.5px;line-height:1.4;background:var(--soft);border:1px solid var(--line);border-radius:9px;
 padding:8px 11px;color:#33363a;word-break:break-word;min-height:40px}
.cp span{min-width:0}
.cp svg{color:#90A4AE}
.cp.done{border-color:#2E7D32;color:#2E7D32}
.cp.done svg{color:#2E7D32}
.rlist{margin:13px 0 0;display:grid;gap:8px}
.rlist .rk{font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);
 display:block;margin-bottom:4px}
.rlist .rv{font-size:14.5px}

/* ---------------- reference rows ---------------- */
.grouphead{display:flex;align-items:center;gap:11px;margin:30px 0 2px;scroll-margin-top:calc(var(--stick) + 62px)}
.grouphead .gi{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;color:#fff;background:#607D8B;flex:none}
.grouphead h3{font-size:21px;margin:0;letter-spacing:-.02em}
.row{padding:20px 0;border-top:1px solid var(--line);scroll-margin-top:calc(var(--stick) + 62px)}
.row .side{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:9px}
.row .pill2{display:inline-block;font-size:11.5px;font-weight:800;color:#fff;padding:5px 11px;border-radius:999px}
.row .when{font-size:14px;font-weight:700}
.row .clock{font-size:13px;color:var(--muted);display:inline-flex;align-items:center;gap:5px}
.row h4{margin:0 0 3px;font-size:20px;letter-spacing:-.025em;line-height:1.2}
.row .cn{font-size:14px;color:var(--muted);margin:0 0 10px}
.row .line{font-size:15.5px;line-height:1.5;max-width:64ch;margin:11px 0 0}
.row .jump{display:inline-flex;align-items:center;gap:5px;font-size:13px;font-weight:700;color:var(--muted);
 margin-top:11px;border:1px solid var(--line);border-radius:999px;padding:8px 13px}
.route{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:10px;max-width:520px}
.route .t{font-size:23px;font-weight:800;letter-spacing:-.035em;line-height:1}
.route .c{font-size:12.5px;font-weight:700;color:var(--muted);margin-top:3px}
.route .n{font-size:11px;color:var(--muted);margin-top:1px}
.route .mid{display:flex;align-items:center;gap:4px;color:#b0bec5}
.route .mid i{flex:1;height:2px;background:currentColor;border-radius:2px;display:block}
.route .r{text-align:right}
.legs{display:grid;gap:11px;margin:15px 0 0}
.leg{border:1px solid var(--line);border-radius:13px;padding:13px 15px 14px;border-top:5px solid #607D8B}
.leg .lno{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:11px}
.leg .lno b{font-size:16px;letter-spacing:-.01em}
.leg .lno span{font-size:12.5px;color:var(--muted)}
.leg .ld{font-size:12px;color:var(--muted);margin-top:10px;border-top:1px solid var(--line);padding-top:8px}
.addrblock{margin:14px 0 0;border:1px solid var(--line);border-radius:13px;overflow:hidden}
.addrblock .en{padding:11px 14px;font-size:14.5px;line-height:1.4;border-bottom:1px solid var(--line)}
.addrblock .cnaddr{display:block;width:100%;padding:14px;background:var(--soft);text-align:left}
.addrblock .cnaddr b{display:block;font-size:19px;font-weight:700;line-height:1.35;letter-spacing:.01em}
.doc .addrblock .cnaddr b{font-size:27px;line-height:1.3}
.doc .addrblock .cnaddr{padding:18px 16px}
.addrblock .cnaddr em{display:flex;align-items:center;gap:6px;font-style:normal;font-size:11px;font-weight:700;
 color:var(--muted);margin-top:7px;letter-spacing:.06em;text-transform:uppercase}
.addrblock .cnaddr.done em{color:#2E7D32}
.addrblock .tel{display:flex;align-items:center;gap:9px;padding:12px 14px;border-top:1px solid var(--line);
 font-size:15px;font-weight:700;text-decoration:none;min-height:48px}
.addrblock .tel em{font-style:normal;font-size:11px;font-weight:700;color:var(--muted);margin-left:auto;
 letter-spacing:.06em;text-transform:uppercase}
.addrblock .tel svg{color:#607D8B}
.tiles{display:grid;gap:12px;margin-top:16px}
.tile{border:1px solid var(--line);border-radius:14px;padding:16px 17px 17px}
.tile .th{display:flex;align-items:center;gap:11px;margin-bottom:11px}
.tile .th .ti{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;background:var(--soft);color:#37474F;flex:none}
.tile .th b{font-size:17.5px;letter-spacing:-.02em}
.tile .line{font-size:15px;line-height:1.5;margin:10px 0 0}

/* ---------------- map view ---------------- */
.mapwrap{position:relative}
.map{height:var(--mh,58vh);min-height:300px;display:none}
.map.on{display:block}
.mk{width:28px;height:28px;border-radius:50%;color:#fff;font-weight:800;font-size:13px;display:grid;
 place-items:center;border:2.5px solid #fff;box-shadow:0 1px 5px rgba(0,0,0,.4)}
.mk.star{width:36px;height:36px;font-size:20px;background:#1a1c1e}
.leaflet-popup-content{font-family:inherit;font-size:14px;line-height:1.35}
.maphint{font-size:12.5px;color:var(--muted);padding:9px var(--gut) 0}

/* ---------------- story index rows ---------------- */
.sx{display:grid;grid-template-columns:62px 1fr 14px;gap:12px;align-items:center;width:100%;
 padding:11px 0;border-top:1px solid var(--line)}
.sx:active{background:var(--soft)}
.sx .ph{position:relative;width:62px;aspect-ratio:1;border-radius:10px;overflow:hidden;background:#eceff1}
.sx .ph img,.sx .ph .noimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.sx .ph .bg{position:absolute;right:3px;bottom:3px;width:19px;height:19px;border-radius:50%;background:var(--c);
 display:grid;place-items:center;font-size:9.5px}
.sx .ttl{display:block;font-size:15.5px;font-weight:700;letter-spacing:-.015em;line-height:1.22}
.sx .mt{display:block;font-size:12px;color:var(--muted);margin-top:3px}
.sx .chev{color:#b9bec4}
.citytag{display:inline-block;font-size:19px;font-weight:800;letter-spacing:-.02em;color:#fff;background:var(--c);
 padding:6px 13px;border-radius:9px;margin:26px 0 2px;scroll-margin-top:calc(var(--stick) + 62px)}

/* ---------------- the sheet ---------------- */
.sheet{position:fixed;inset:0;z-index:90;display:none}
.sheet.on{display:block}
.sheet .scrim{position:absolute;inset:0;background:rgba(0,0,0,.45)}
.sheet .panel{position:absolute;inset:0;background:#fff;display:flex;flex-direction:column;
 animation:rise .2s ease-out}
@keyframes rise{from{transform:translateY(26px);opacity:.5}to{transform:none;opacity:1}}
.shd{flex:none;display:flex;align-items:center;gap:6px;padding:7px 10px 7px 6px;border-bottom:1px solid var(--line);
 padding-top:calc(7px + var(--sat));background:#fff}
.shd .x{width:42px;height:42px;display:grid;place-items:center;border-radius:50%}
.shd .x:active{background:var(--soft)}
.shd .lbl{font-size:12.5px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);
 min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.shd .nav{margin-left:auto;display:flex;gap:4px;flex:none}
.shd .nav button{width:42px;height:42px;display:grid;place-items:center;border-radius:50%;color:var(--muted)}
.shd .nav button:disabled{opacity:.28}
.shd .nav button:active:not(:disabled){background:var(--soft)}
.sbody{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;
 padding-bottom:calc(36px + var(--sab))}
.doc .dph{position:relative;aspect-ratio:16/10;background:#eceff1}
.doc .dph img,.doc .dph .noimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.doc .dph .badge{position:absolute;left:12px;top:12px;width:36px;height:36px;border-radius:50%;display:grid;
 place-items:center;background:var(--c);font-size:17px;box-shadow:0 2px 8px rgba(0,0,0,.32)}
.doc .dph .n{position:absolute;right:12px;top:12px;min-width:29px;height:29px;padding:0 9px;border-radius:15px;
 background:rgba(26,28,30,.9);color:#fff;font-weight:800;display:grid;place-items:center;font-size:14px}
.doc .dbody{padding:17px var(--gut) 0}
.doc .dmeta{display:flex;flex-wrap:wrap;gap:5px 9px;font-size:12px;font-weight:700;color:var(--muted);
 text-transform:uppercase;letter-spacing:.05em}
.doc .dmeta b{color:var(--c)}
.doc h2{font-size:26px;line-height:1.14;letter-spacing:-.03em;margin:7px 0 0;font-weight:800}
.doc .dlead{font-size:17px;line-height:1.5;margin:10px 0 0;color:#33363a}
.doc .dtip{margin:15px 0 0;background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:13px 15px;
 font-size:14.5px;line-height:1.5}
.doc .dtip b{display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.07em;text-transform:uppercase;
 color:var(--muted);margin-bottom:6px}
.doc .dacts{display:flex;flex-wrap:wrap;gap:8px;margin:15px 0 0}
.doc .dacts button{display:inline-flex;align-items:center;gap:7px;border:1.5px solid var(--line);border-radius:999px;
 padding:0 14px;height:42px;font-size:13.5px;font-weight:700}
.doc .dacts button.gate{background:var(--c);border-color:var(--c);color:#fff}
.doc .dacts .amap{display:inline-flex;align-items:center;gap:7px;border:1.5px solid var(--ink);
 background:var(--ink);color:#fff;border-radius:999px;padding:0 15px;height:42px;
 font-size:13.5px;font-weight:700;text-decoration:none}
.addrblock .tel.go,.addrblock .tel.go svg{color:var(--ink)}
.doc .story{margin-top:18px;border-top:1px solid var(--line);padding-top:16px}
.doc .story p{margin:0 0 13px;font-size:16.5px;line-height:1.62;max-width:64ch}
.doc .credit{font-size:11.5px;color:var(--muted);margin-top:14px}
.doc .credit a{color:var(--muted)}

footer{border-top:1px solid var(--line);margin-top:34px;padding:20px var(--gut) 34px;font-size:12.5px;color:var(--muted)}

/* ---------------- desktop ---------------- */
@media (min-width:820px){
 :root{--gut:28px;--app:56px;--tabh:50px;--tab:0px}
 body{font-size:17px}
 .wrap{max-width:1180px;margin:0 auto}
 main{padding-bottom:60px}
 .abrow{max-width:1180px;margin:0 auto;gap:22px}
 .appbar{background:#fff;backdrop-filter:none;-webkit-backdrop-filter:none}
 .brand{font-size:19px}
 .brand span{font-size:12px}
 .tabs{top:var(--app);bottom:auto;border-top:0;border-bottom:1px solid var(--line);padding:0}
 .tabin{display:flex;gap:4px;max-width:1180px;margin:0 auto;padding:0 var(--gut);height:var(--tabh);align-items:center}
 .tabs button{height:38px;flex-direction:row;gap:7px;font-size:14.5px;padding:0 15px;border-radius:999px}
 .tabs button[aria-selected=true]{background:var(--ink);color:#fff}
 .tabs button[aria-selected=true]:before{display:none}
 .tabs .bub{position:static;margin-left:2px}
 .sub .scroller,.sub .rail,.sub .crow{max-width:1180px;margin:0 auto}
 .crow{padding-top:9px;gap:7px}
 .crow button{flex:0 0 auto;padding:0 16px;height:32px;font-size:13.5px;border-radius:999px}
 .railin{grid-template-columns:repeat(15,1fr);gap:6px;width:100%;max-width:820px}
 .rd{width:auto}
 .rd b{font-size:19px}
 .rd span{font-size:10px}
 .nowstrip{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(272px,1fr));
  overflow:visible;padding-top:22px}
 .nu{width:auto;max-width:none}
 .striphd{max-width:1180px;margin:0 auto}
 .tod{max-width:1180px;margin:22px auto 0}
 .chead{border-radius:0;margin-top:52px}
 .chead .in{padding:44px var(--gut) 38px;max-width:1180px;margin:0 auto}
 .chead.air .in{padding:26px var(--gut) 24px}
 .chead.air h2{font-size:34px}
 .chead h2{font-size:60px}
 .chead .csub{font-size:19px}
 .chead .meta{font-size:14px;gap:8px}
 h2.big{font-size:52px}
 p.lead{font-size:18px}
 .dayhd{padding:30px 0 12px}
 .dayhd .dn{font-size:38px}
 .grouphead h3{font-size:25px}
 .stops{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:18px;margin:6px 0 10px}
 .stop{grid-template-columns:1fr;gap:0;padding:0;border:1px solid var(--line);border-top:5px solid var(--c);
  border-radius:13px;overflow:hidden;align-items:stretch;transition:box-shadow .15s,transform .15s}
 .stop:hover{box-shadow:0 6px 20px rgba(0,0,0,.09);transform:translateY(-2px)}
 .stop .ph{width:100%;aspect-ratio:16/10;border-radius:0}
 .stop .ph .n{left:10px;top:10px;min-width:27px;height:27px;font-size:13.5px}
 .stop .ph .bg{right:9px;bottom:9px;width:31px;height:31px;font-size:15px}
 .stop .tx{padding:12px 15px 15px}
 .stop .ttl{font-size:18px}
 .stop .one{font-size:14.5px;-webkit-line-clamp:3}
 .stop .chev{display:none}
 .trans{grid-column:1/-1;align-items:center}
 .row{display:grid;grid-template-columns:200px 1fr;gap:10px 28px;padding:26px 0}
 .row .side{display:block;margin:0}
 .row .when{margin-top:9px;font-size:16px}
 .row .clock{display:flex;margin-top:3px}
 .row h4{font-size:23px}
 .legs{grid-template-columns:repeat(auto-fit,minmax(262px,1fr))}
 .tiles{grid-template-columns:repeat(auto-fit,minmax(308px,1fr));gap:15px}
 .sx{grid-template-columns:86px 1fr 14px}
 .sx .ph{width:86px}
 .sx .ttl{font-size:17px}
 .map{border-radius:14px;border:1px solid var(--line);min-height:420px}
 .mapwrap{max-width:1180px;margin:0 auto;padding:0 var(--gut)}
 .maphint{max-width:1180px;margin:0 auto}
 .sheet .panel{inset:auto;left:50%;top:3vh;transform:translateX(-50%);width:min(760px,94vw);height:94vh;
  border-radius:18px;overflow:hidden;box-shadow:0 26px 70px rgba(0,0,0,.34)}
 @keyframes rise{from{transform:translateX(-50%) translateY(26px);opacity:.5}to{transform:translateX(-50%);opacity:1}}
 .doc h2{font-size:34px}
 .doc .dbody{padding:22px 30px 0}
 .doc .story p{font-size:17px}
 footer{max-width:1180px;margin:44px auto 0}
}
@media (max-height:520px){
 .maphint{display:none}
 .map{min-height:200px}
 .chead .in{padding:14px var(--gut) 13px}
 .chead h2{font-size:27px}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
@media print{
 .appbar,.tabs,.sub,.map,.sheet,.chead .quick,.stop .chev{display:none!important}
 .view{display:block!important}
 main{padding:0}
 .stop,.row,.tile,.leg{break-inside:avoid}
 details.fine{display:none}
}
</style></head><body>
""")
w(sprite())

def airday(idx, aiso, title, theme):
    """A flying day, rendered in the Plan in the same shape as a city day."""
    segs = AIRSEGS[aiso]
    wd, dn, mo = segs[0]["date"].split()
    stops = [segs[0]["an"].split(" \u00b7 ")[0]] + [g["bn"].split(" \u00b7 ")[0] for g in segs]
    route = " \u2192 ".join(stops)
    w('<div class="chead air" data-city="air" style="--c:#546E7A"><div class="in">')
    w(f'<h2>{E(title)}</h2><div class="csub">{E(route)}</div>')
    w(f'<div class="meta"><span>{ic("clock",13)}{wd} {dn} {mo}</span>'
      f'<span>{ic("plane",13)}{len(segs)} flights</span>'
      f'<span>{ic("alert",13)}No checked bag</span></div>')
    w('</div></div><div class="wrap">')
    w(f'<section class="day" id="day-air-{idx}" data-iso="{aiso}" style="--c:#546E7A">')
    w(f'<div class="dayhd"><span class="wd">{wd}</span><span class="dn">{dn} {mo}</span>'
      f'<span class="cnt">{len(segs)} flights</span><span class="th">{E(theme)}</span></div>')
    w('<div class="legs">')
    for g in segs:
        w(f'<div class="leg"><div class="lno"><b>{E(g["no"])}</b><span>{E(g["date"])}</span></div>'
          f'<div class="route">')
        w(f'<div><div class="t">{E(g["at"])}</div><div class="c">{E(g["a"])}</div>'
          f'<div class="n">{E(g["an"])}</div></div>')
        w(f'<div class="mid"><i></i>{ic("plane",14)}<i></i></div>')
        w(f'<div class="r"><div class="t">{E(g["bt"])}</div><div class="c">{E(g["b"])}</div>'
          f'<div class="n">{E(g["bn"])}</div></div>')
        w(f'</div><div class="ld">{E(g["dur"])} \u00b7 {E(g["note"])}</div></div>')
    w('</div>')
    w(f'<button type="button" class="jumpbtn" data-go="travel" data-anchor="flights">'
      f'{ic("plane",16)}Booking codes and the small print</button>')
    w('</section></div>')

# ===================== chrome =====================
TABS = [("plan", "cal", "Plan"), ("map", "map", "Map"), ("tickets", "ticket", "Tickets"),
        ("travel", "plane", "Travel"), ("stories", "book", "Stories")]
todo_n = sum(1 for b in bookings.values() if b["state"] == "todo")

w('<header class="appbar"><div class="abrow">')
w('<a class="brand" href="#/plan">China 2026<span>19 Sep \u2013 3 Oct \u00b7 four of us</span></a>')
w(f'<button class="taxi" type="button" id="taxibtn">{ic("taxi",19)}<span>Taxi</span>'
  f'<span class="sr">: the hotel address in Chinese</span></button>')
w('</div></header>')
# The tab bar is a sibling of the header, never a child: backdrop-filter on .appbar makes it
# a containing block, which would pin this "fixed" bar to the header instead of the viewport.
w('<nav class="tabs" role="tablist" aria-label="Sections"><div class="tabin">')
for key, icon, label in TABS:
    bub = f'<span class="bub">{todo_n}</span>' if (key == "tickets" and todo_n) else ''
    w(f'<button type="button" role="tab" data-tab="{key}" aria-selected="false" '
      f'aria-controls="v-{key}">{ic(icon,21)}<b>{label}</b>{bub}</button>')
w('</div></nav><main>')

# ===================== PLAN =====================
w('<section class="view" id="v-plan" role="tabpanel" aria-label="Plan">')

# sticky city jump, then the sticky day rail
w('<div class="sub"><div class="crow">')
for c in cities:
    w(f'<button type="button" class="cj" data-cj="{c["id"]}" style="--c:{c["color"]}">'
      f'<i></i>{E(c["name"])}</button>')
w('</div><div class="rail"><div class="railin">')
for idx, (cid, dn, mo) in enumerate(ribbon):
    iso = isoof(dn, mo)
    hol = HOL.get(idx)
    stl = f'--c:{CCOL[cid]}' + (f';--h:{hol[1]}' if hol else '')
    ttl = f' title="{E(hol[0])}"' if hol else ''
    w(f'<button type="button" class="rd{" hol" if hol else ""}" style="{stl}" '
      f'data-day="{FIRSTBLOCK[iso]}" data-iso="{iso}" data-city="{cid}"{ttl}>'
      f'<b>{dn}</b><span>{mo}</span></button>')
w('</div></div></div>')

# countdown / today banner, filled in by JS
w(f'<div class="tod" id="todbar" hidden><span class="tdi">{ic("cal",21)}</span><div><b id="todb"></b>'
  f'<span id="todl"></span></div></div>')

# the things that still need doing
# the count is what is still open, not how many cards there are: the settled card says
# "nothing left", and counting it made the red number claim one more job than exists
open_n = sum(1 for n in nextup if n["tone"] != "k")
w(f'<div class="striphd"><h3>Needs you</h3><span class="cnt">{open_n}</span></div>')
w('<div class="nowstrip">')
for n in nextup:
    t = TONE[n["tone"]]
    sub = f' <em>{E(n["sub"])}</em>' if n["sub"] else ''
    w(f'<div class="nu" style="--t:{t}"><span class="nw">{ic(n["icon"],15)}{E(n["when"])}{sub}</span>'
      f'<b class="nh">{E(n["head"])}</b><span class="nl">{E(n["line"])}</span></div>')
w('</div>')

airday(0, AIR_ISO[0], "Getting there",
       "Out of Cairo at " + flights["segs"][0]["at"] + ", and into Beijing at "
       + AIRSEGS[AIR_ISO[0]][-1]["bt"] + " the next afternoon.")

# city blocks
for c in cities:
    cid = c["id"]; col = c["color"]
    citems = [it for it in items if it[1] == cid]
    g = (f'linear-gradient(100deg,{rgba(col,.95)} 0%,{rgba(col,.8)} 44%,{rgba(col,.25)} 78%,{rgba(col,0)} 100%)')
    w(f'<div class="chead" id="{cid}" data-city="{cid}" style="--c:{col};--g:{g}">')
    w(img(heroes[cid], "hero")); w('<div class="tint"></div>')
    w('<div class="in">')
    w(f'<h2>{E(c["name"])}</h2><div class="csub">{E(c["sub"])}</div>')
    w(f'<div class="meta"><span>{ic("clock",13)}{E(c["dates"])}</span>'
      f'<span>{ic("bed",13)}{E(c["hotel"].split(",")[0])}</span>'
      f'<span>{ic("pin",13)}{c["nights"]} nights</span>'
      + "".join(f'<span class="hol">{ic("alert",13)}{E(h)}</span>' for h in holchips(cid))
      + '</div>')
    w(f'<div class="quick"><button type="button" data-go="map" data-city="{cid}">{ic("map",15)}Map</button>'
      f'<button type="button" data-go="travel" data-anchor="hotel-{cid}">{ic("bed",15)}Hotel</button>'
      f'<button type="button" data-taxi="{cid}">{ic("taxi",15)}Taxi card</button></div>')
    w('</div></div><div class="wrap">')

    for di, (dlabel, theme) in enumerate(days[cid]):
        wd, dn, mo = dlabel.split()
        stops = [it for it in citems if it[2] == di]
        real = [it for it in stops if it[4] != "transit"]
        iso = f'2026-{MONTH[mo]}-{int(dn):02d}'
        w(f'<section class="day" id="day-{cid}-{di}" data-iso="{iso}" style="--c:{col}">')
        w(f'<div class="dayhd"><span class="wd">{wd}</span><span class="dn">{dn} {mo}</span>'
          f'<span class="cnt">{len(real)} stop{"s" if len(real)!=1 else ""}</span>'
          f'<span class="th">{E(theme)}</span></div>')
        w('<div class="stops">')
        for it in stops:
            pid, _, d, slot, cat, title, one, tip, story, far = it
            ccol, emoji, catlab = CAT[cat]
            if cat == "transit":
                w(f'<div class="trans"><span class="ti">{ic("train",24)}</span><div>'
                  f'<span class="ts">{E(slot)}</span><b>{E(title)}</b>'
                  f'<p class="one">{E(one)}</p><p class="tip">{E(tip)}</p></div></div>')
                continue
            farlab = ' <i>(out of town)</i>' if far else ''
            bk = bookings.get(pid)
            pill = (f'<span class="pl" style="background:{BST[bk["state"]][0]}">{E(bk["pill"])}</span>') if bk else ''
            w(f'<button type="button" class="stop" data-doc="{pid}" style="--c:{ccol}">'
              f'<span class="ph">{img(pid)}<span class="n">{NUMS[pid]}</span>'
              f'<span class="bg" title="{catlab}">{emoji}</span></span>'
              f'<span class="tx"><span class="slot">{E(slot)}{farlab}</span>'
              f'<span class="ttl">{E(title)}</span><p class="one">{E(one)}</p>{pill}</span>'
              f'<span class="chev">{ic("chev",15)}</span></button>')
        w('</div></section>')
    fars = [it for it in citems if it[9]]
    if fars:
        w('<p class="far">Off the edge of the map: '
          + " · ".join(f'<b>{NUMS[it[0]]}</b> {E(it[5])}' for it in fars) + '</p>')
    w('</div>')
airday(1, AIR_ISO[-1], "Getting home",
       "You leave the hotel at 22:30 on the 2nd. Wheels up at "
       + AIRSEGS[AIR_ISO[-1]][0]["at"] + ", Cairo at " + AIRSEGS[AIR_ISO[-1]][-1]["bt"] + ".")
w('</section>')

# ===================== MAP =====================
w('<section class="view" id="v-map" role="tabpanel" aria-label="Map">')
w('<div class="sub"><div class="scroller">')
for c in cities:
    w(f'<button type="button" class="seg mapcity" data-city="{c["id"]}" style="--c:{c["color"]}" '
      f'aria-pressed="false"><span class="sd"></span>{E(c["name"])}</button>')
w('</div></div>')
w('<p class="maphint">Numbers match the Plan \u00b7 black pin is your hotel \u00b7 tap a pin for its story</p>')
w('<div class="mapwrap">')
for c in cities:
    w(f'<div class="map" id="lmap-{c["id"]}"></div>')
w('</div></section>')

# ===================== TICKETS =====================
counts = {k: sum(1 for b in bookings.values() if b["state"] == k) for k in BST}
w('<section class="view" id="v-tickets" role="tabpanel" aria-label="Tickets">')
w('<div class="sub"><div class="scroller">')
w('<button type="button" class="seg tkf on" data-state="all" aria-pressed="true">Everything</button>')
for k, (kcol, klab) in BST.items():
    if counts[k]:
        w(f'<button type="button" class="seg tkf" data-state="{k}" aria-pressed="false" style="--c:{kcol}">'
          f'<span class="sd"></span>{counts[k]} {E(klab.lower())}</button>')
w('</div></div>')
w('<div class="wrap"><div style="padding-top:20px"><h2 class="big">Tickets</h2>')
w('<p class="lead">What is bought, what is not, and what to do at each gate. Numbers and PINs are on every row — tap one to copy it.</p></div>')
for c in cities:
    cid = c["id"]
    rows = [it for it in items if it[1] == cid and it[0] in bookings]
    if not rows: continue
    w(f'<div class="grouphead"><span class="gi" style="background:{c["color"]}">{ic("ticket",20)}</span>'
      f'<h3>{E(c["name"])}</h3></div>')
    for it in rows:
        pid, _, d, slot, cat, title, one, tip, story, far = it
        b = bookings[pid]; bcol, _lab = BST[b["state"]]
        w(f'<div class="row tkrow" id="ticket-{pid}" data-state="{b["state"]}"><div class="side">')
        w(f'<span class="pill2" style="background:{bcol}">{E(b["pill"])}</span>')
        w(f'<span class="when">{E(b["when"])}</span>'
          f'<span class="clock">{ic("clock",13)}{E(b["clock"])}</span></div><div>')
        w(f'<h4>{E(title)}</h4>')
        w(chips(b["chips"]))
        w(f'<p class="line">{E(b["line"])}</p>')
        if b.get("ref"):
            w('<div class="rlist"><div><span class="rk">Reference</span>'
              + copyable(b["ref"], "booking reference") + '</div></div>')
        w(fine(b["fine"]))
        w(f'<button type="button" class="jump" data-doc="{pid}">{ic("up",13)}Open the stop</button>')
        w('</div></div>')
w('</section>')

# ===================== TRAVEL =====================
w('<section class="view" id="v-travel" role="tabpanel" aria-label="Travel">')
w('<div class="sub"><div class="scroller">')
for anc, lab in [("hotels", "Hotels"), ("trains", "Trains"), ("flights", "Flights"), ("prep", "Before you fly")]:
    w(f'<button type="button" class="seg jumpto" data-anchor="{anc}">{E(lab)}</button>')
w('</div></div><div class="wrap">')
w('<div style="padding-top:20px"><h2 class="big">Flights, trains, hotels</h2>')
w('<p class="lead">Every reference, seat and address from the confirmations. Passport numbers are not here — the gates read the passport itself.</p></div>')

# hotels first: the address is the thing you need in a hurry
w(f'<div class="grouphead" id="hotels"><span class="gi">{ic("bed",20)}</span><h3>Hotels</h3></div>')
for h in hotels:
    c = CBY[h["city"]]
    w(f'<div class="row" id="hotel-{h["city"]}"><div class="side">')
    w(f'<span class="pill2" style="background:{c["color"]}">{E(c["name"])}</span>')
    w(f'<span class="when">{E(h["inn"])}</span>'
      f'<span class="clock">{ic("clock",13)}out {E(h["out"])}</span>'
      f'<span class="clock">{ic("bed",13)}{E(h["nights"])}</span></div><div>')
    w(f'<h4>{E(h["name"])}</h4><p class="cn">{E(h["cn"])}</p>')
    w(chips(h["chips"]))
    w(f'<p class="line">{E(h["line"])}</p>')
    w('<div class="addrblock">')
    w(f'<div class="en">{E(h["addr"])}</div>')
    w(f'<button type="button" class="cnaddr" data-copy="{E(h["addrcn"])}"><b>{E(h["addrcn"])}</b>'
      f'<em>{ic("copy",13)}<span>Show this to the driver · tap to copy</span></em></button>')
    w(f'<a class="tel" href="tel:{h["phone"].replace(" ","")}">{ic("phone",18)}{E(h["phone"])}'
      f'<em>Tap to call</em></a>')
    w(f'<a class="tel go" href="{amap_url(h["addrcn"], h["city"])}" target="_blank" rel="noopener">{ic("nav",18)}Directions in Amap<em>Opens the app</em></a>')
    w('</div>')
    w('<div class="rlist">' + ''.join(
        f'<div><span class="rk">{E(what)}</span>{copyable(no + "  " + pin, "booking")}</div>'
        for no, pin, what in h["refs"]) + '</div>')
    w(fine(h["fine"]))
    w('</div></div>')

w(f'<div class="grouphead" id="trains"><span class="gi">{ic("train",20)}</span><h3>Trains</h3></div>')
for t in trains:
    bcol, _lab = BST[t["state"]]
    w(f'<div class="row"><div class="side">')
    w(f'<span class="pill2" style="background:{bcol}">{E(t["pill"])}</span>')
    w(f'<span class="when">{E(t["date"])}</span>'
      f'<span class="clock">{ic("clock",13)}{E(t["dur"])} · {E(t["no"])}</span></div><div>')
    w('<div class="route">')
    w(f'<div><div class="t">{E(t["at"])}</div><div class="c">{E(t["a"])}</div><div class="n">{E(t["acn"])}</div></div>')
    w(f'<div class="mid"><i></i>{ic("train",15)}<i></i></div>')
    w(f'<div class="r"><div class="t">{E(t["bt"])}</div><div class="c">{E(t["b"])}</div><div class="n">{E(t["bcn"])}</div></div>')
    w('</div>')
    w('<div style="margin-top:14px">' + chips(t["chips"]) + '</div>')
    w(f'<p class="line">{E(t["line"])}</p>')
    w('<div class="rlist"><div><span class="rk">Seats</span><span class="rv">' + E(t["seats"]) + '</span></div>'
      '<div><span class="rk">Reference</span>' + copyable(t["ref"], "train booking") + '</div></div>')
    w(fine(t["fine"]))
    w('</div></div>')

w(f'<div class="grouphead" id="flights"><span class="gi">{ic("plane",20)}</span><h3>Flights</h3></div>')
w('<div style="margin-top:14px">' + chips(flights["chips"]) + '</div>')
w(f'<p class="line" style="margin-top:12px">{E(flights["line"])}</p>')
w('<div class="legs">')
for g in flights["segs"]:
    w(f'<div class="leg"><div class="lno"><b>{E(g["no"])}</b><span>{E(g["date"])}</span></div><div class="route">')
    w(f'<div><div class="t">{E(g["at"])}</div><div class="c">{E(g["a"])}</div><div class="n">{E(g["an"])}</div></div>')
    w(f'<div class="mid"><i></i>{ic("plane",14)}<i></i></div>')
    w(f'<div class="r"><div class="t">{E(g["bt"])}</div><div class="c">{E(g["b"])}</div><div class="n">{E(g["bn"])}</div></div>')
    w(f'</div><div class="ld">{E(g["dur"])} · {E(g["note"])}</div></div>')
w('</div>')
w('<div class="rlist">' + ''.join(
    f'<div><span class="rk">{E(nm)} · e-ticket {E(t)}</span>{copyable(p, "booking code")}</div>'
    for p, nm, t in flights["refs"]) + '</div>')
w(fine(flights["fine"]))

w(f'<div class="grouphead" id="prep"><span class="gi">{ic("passport",20)}</span><h3>Before you fly</h3></div>')
w('<p class="lead" style="margin-top:8px">Six things to have sorted. Nothing else needs doing.</p><div class="tiles">')
for p in prep:
    w(f'<div class="tile"><div class="th"><span class="ti">{ic(p["icon"],20)}</span><b>{E(p["t"])}</b></div>')
    w(chips(p["chips"]))
    w(f'<p class="line">{E(p["line"])}</p>')
    w(fine(p["fine"], "More"))
    w('</div>')
w('</div></div></section>')

# ===================== STORIES (index only) =====================
w('<section class="view" id="v-stories" role="tabpanel" aria-label="Stories">')
w('<div class="sub"><div class="scroller">')
w('<button type="button" class="seg stf on" data-city="all" aria-pressed="true">Whole trip</button>')
for c in cities:
    w(f'<button type="button" class="seg stf" data-city="{c["id"]}" style="--c:{c["color"]}" '
      f'aria-pressed="false"><span class="sd"></span>{E(c["name"])}</button>')
w('</div></div><div class="wrap">')
w('<div style="padding-top:20px"><h2 class="big">The stories</h2>')
w(f'<p class="lead">{len(ORDER)} of them, in day order. Tap one and read straight through with the arrows — built for the train, not the street.</p></div>')
for c in cities:
    cid = c["id"]
    w(f'<div class="stgroup" data-city="{cid}">')
    w(f'<span class="citytag" id="stories-{cid}" style="--c:{c["color"]}">{E(c["name"])}</span>')
    for it in [i for i in items if i[1] == cid and i[8]]:
        pid, _, d, slot, cat, title, one, tip, story, far = it
        ccol, emoji, catlab = CAT[cat]
        w(f'<button type="button" class="sx" data-doc="{pid}" style="--c:{ccol}">'
          f'<span class="ph">{img(pid)}<span class="bg">{emoji}</span></span>'
          f'<span><span class="ttl">{E(title)}</span>'
          f'<span class="mt">{E(days[cid][d][0])} · {E(slot)} · {catlab}</span></span>'
          f'<span class="chev">{ic("chev",15)}</span></button>')
    w('</div>')
w('</div></section>')

w('<footer>Last updated ' + datetime.date.today().strftime('%-d %B %Y')
  + ' · Photos from Wikimedia Commons, showing the place or the dish, not always the exact venue.'
  ' · No passport numbers on this page, ever.</footer>')
w('</main>')

# ===================== sheet + hidden document bank =====================
w('<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="Story" hidden>')
w('<div class="scrim" data-close></div><div class="panel">')
w(f'<div class="shd"><button class="x" type="button" data-close aria-label="Close">{ic("close",22)}</button>')
w('<span class="lbl" id="sheetlbl"></span>')
w(f'<span class="nav"><button type="button" id="sprev" aria-label="Previous stop">{ic("left",20)}</button>'
  f'<button type="button" id="snext" aria-label="Next stop">{ic("chev",20)}</button></span></div>')
w('<div class="sbody" id="sbody"></div></div></div>')

w('<div id="bank" hidden>')
for c in cities:
    cid = c["id"]
    for it in [i for i in items if i[1] == cid and i[8]]:
        pid, _, d, slot, cat, title, one, tip, story, far = it
        ccol, emoji, catlab = CAT[cat]
        p = P.get(pid, {})
        bk = bookings.get(pid)
        w(f'<div class="doc" id="doc-{pid}" data-label="{E(c["name"])} · {E(days[cid][d][0])}" '
          f'style="--c:{ccol}">')
        w(f'<div class="dph">{img(pid)}<span class="badge" title="{catlab}">{emoji}</span>'
          f'<span class="n">{NUMS[pid]}</span></div><div class="dbody">')
        farlab = '<span>Out of town</span>' if far else ''
        w(f'<div class="dmeta"><b>{catlab}</b><span>{E(days[cid][d][0])}</span><span>{E(slot)}</span>{farlab}</div>')
        w(f'<h2>{E(title)}</h2><p class="dlead">{E(one)}</p>')
        if tip:
            w(f'<div class="dtip"><b>{ic("alert",13)}The practical bit</b>{E(tip)}</div>')
        w('<div class="dacts">')
        _am = amap_for(title, cid, pid)
        if _am:
            w(f'<a class="amap" href="{_am}" target="_blank" rel="noopener">'
              f'{ic("nav",16)}Directions in Amap</a>')
        if bk:
            w(f'<button type="button" class="gate" data-go="tickets" data-anchor="ticket-{pid}">'
              f'{ic("ticket",16)}{E(bk["pill"])} — see the ticket</button>')
        w(f'<button type="button" data-go="map" data-city="{cid}" data-pin="{pid}">{ic("map",16)}Show on the map</button>')
        w(f'<button type="button" data-go="plan" data-anchor="day-{cid}-{d}">{ic("cal",16)}Back to {E(days[cid][d][0])}</button>')
        w('</div>')
        w('<div class="story">' + ''.join(f'<p>{E(para)}</p>' for para in story.split("\n\n")) + '</div>')
        if p.get("imgpage"):
            w(f'<div class="credit"><a href="{p["imgpage"]}" target="_blank" rel="noopener">Photo: Wikimedia Commons</a></div>')
        w('</div></div>')

# taxi cards: the hotel address in Chinese, one tap from anywhere
for h in hotels:
    c = CBY[h["city"]]
    w(f'<div class="doc" id="doc-taxi-{h["city"]}" data-label="Taxi card · {E(c["name"])}" '
      f'style="--c:{c["color"]}"><div class="dbody" style="padding-top:22px">')
    w(f'<div class="dmeta"><b>{E(c["name"])}</b><span>{E(c["dates"])}</span></div>')
    w(f'<h2>{E(h["name"])}</h2><p class="dlead">{E(h["cn"])}</p>')
    w('<div class="addrblock">')
    w(f'<button type="button" class="cnaddr" data-copy="{E(h["addrcn"])}"><b>{E(h["addrcn"])}</b>'
      f'<em>{ic("copy",13)}<span>Show this to the driver · tap to copy</span></em></button>')
    w(f'<div class="en">{E(h["addr"])}</div>')
    w(f'<a class="tel" href="tel:{h["phone"].replace(" ","")}">{ic("phone",18)}{E(h["phone"])}'
      f'<em>Tap to call</em></a>')
    w(f'<a class="tel go" href="{amap_url(h["addrcn"], h["city"])}" target="_blank" rel="noopener">{ic("nav",18)}Directions in Amap<em>Opens the app</em></a>')
    w('</div>')
    w(f'<div class="dtip"><b>{ic("clock",13)}Check in and out</b>In {E(h["inn"])}. Out {E(h["out"])}.</div>')
    w('<div class="dacts">'
      f'<button type="button" data-go="travel" data-anchor="hotel-{h["city"]}">{ic("bed",16)}Full hotel details</button>'
      f'<button type="button" data-go="map" data-city="{h["city"]}">{ic("map",16)}Map</button></div>')
    w('</div></div>')
w('</div>')

# ===================== data for the map and the calendar =====================
mapdata = {}
hotelpins = {"beijing": (39.9405, 116.3935), "xian": (34.2610, 108.9455),
             "chengdu": (30.6640, 104.0435), "chongqing": (29.5610, 106.5690)}
for c in cities:
    cid = c["id"]; pts = []
    for it in items:
        if it[1] != cid or it[4] == "transit": continue
        p = P[it[0]]
        pts.append(dict(n=NUMS[it[0]], lat=p["lat"], lng=p["lng"], title=it[5],
                        day=days[cid][it[2]][0], slot=it[3], col=CAT[it[4]][0], far=it[9], id=it[0],
                        amap=amap_for(it[5], cid, it[0])))
    mapdata[cid] = dict(pts=pts, hotel=hotelpins[cid], hname=c["hotel"],
                        hamap=amap_url(HOTELCN[cid], cid))

caldays = []
for cid, dn, mo in ribbon:
    di = DAYKEY.get((cid, dn, mo))
    i = isoof(dn, mo)
    caldays.append(dict(iso=i, city=cid, target=FIRSTBLOCK[i],
                        theme=(days[cid][di][1] if di is not None else "In the air"),
                        cityname=(CBY[cid]["name"] if cid in CBY else "In the air")))

w('<script>')
w('const DATA=' + json.dumps(mapdata, ensure_ascii=False) + ';')
w('const CAL=' + json.dumps(caldays, ensure_ascii=False) + ';')
w('const ORDER=' + json.dumps(ORDER, ensure_ascii=False) + ';')
w(r"""
const $=(s,r)=>(r||document).querySelector(s), $$=(s,r)=>Array.prototype.slice.call((r||document).querySelectorAll(s));
const tabBtns=$$('.tabs button'), views={};
tabBtns.forEach(function(b){views[b.dataset.tab]=document.getElementById('v-'+b.dataset.tab);});
const sheet=$('#sheet'), sbody=$('#sbody'), slbl=$('#sheetlbl'), prevB=$('#sprev'), nextB=$('#snext'),
      sheetNav=$('.shd .nav'), rail=$('#v-plan .rail'), todbar=$('#todbar');
let cur='plan', curCity='beijing', sheetOpen=null, sheetPushed=false, lastPush=false,
    pending={}, mapLoaded=false, mapLoading=false, mapObj={}, mapMarks={}, pendingPin=null;
const scrollMem={};

function iso(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
const TODAY=iso(new Date()), TODAYi=CAL.findIndex(function(c){return c.iso===TODAY;});
if(TODAYi>=0){for(let i=TODAYi;i<CAL.length;i++){if(DATA[CAL[i].city]){curCity=CAL[i].city;break;}}}

/* ---------- tabs and routing ---------- */
function stickBottom(){const s=$('.sub',views[cur]);return s?s.getBoundingClientRect().bottom:0;}
function showTab(name){
  if(!views[name])name='plan';
  if(cur!==name)scrollMem[cur]=window.scrollY;
  cur=name;
  for(const k in views)views[k].classList.toggle('on',k===name);
  document.body.classList.toggle('mapview',name==='map');
  tabBtns.forEach(function(b){b.setAttribute('aria-selected',b.dataset.tab===name?'true':'false');});
  const anchor=pending.anchor;
  if(anchor){
    const el=document.getElementById(anchor);
    if(el){requestAnimationFrame(function(){el.scrollIntoView({block:'start'});});}
  }else{window.scrollTo(0,scrollMem[name]||0);}
  if(name==='map')ensureMap();
  if(name==='plan')spy();
}
function nav(hash,opts){
  pending=opts||{};
  const replacing=!!sheetOpen;
  if(sheetOpen)closeSheet({silent:true});
  if(location.hash!==hash){
    if(replacing){history.replaceState({},'',hash);lastPush=false;}
    else{history.pushState({},'',hash);lastPush=true;}
  }else lastPush=false;
  applyHash(hash);
}
function applyHash(h){
  h=(h||'').replace(/^#/,'');
  const p=pending; pending={};
  if(!h){showTab('plan');return;}
  if(h.charAt(0)==='/'){
    const bits=h.split('/'), tab=bits[1], arg=bits[2];
    if(tab==='doc'){openDoc(arg);return;}
    if(sheetOpen)closeSheet({silent:true});
    if(tab==='map'&&arg)curCity=arg;
    pending=p; showTab(tab); pending={};
    if(tab==='map')selectMapCity(curCity);
    return;
  }
  if(sheetOpen)closeSheet({silent:true});
  if(h.indexOf('story-')===0){openDoc(h.slice(6));return;}
  if(h.indexOf('ticket-')===0){pending={anchor:h};showTab('tickets');return;}
  if(h.indexOf('hotel-')===0){pending={anchor:h};showTab('travel');return;}
  if(h.indexOf('day-')===0){pending={anchor:h};showTab('plan');return;}
  if(h.indexOf('stories-')===0){pending={anchor:h};showTab('stories');return;}
  if(h.indexOf('map-')===0){curCity=h.slice(4);showTab('map');selectMapCity(curCity);return;}
  if(h==='prep'||h==='travel'){pending={anchor:h==='prep'?'prep':'hotels'};showTab('travel');return;}
  if(h==='tickets'||h==='stories'){showTab(h);return;}
  if(DATA[h]){pending={anchor:h};showTab('plan');return;}
  showTab('plan');
}
window.addEventListener('popstate',function(){pending={};applyHash(location.hash);});
tabBtns.forEach(function(b){b.addEventListener('click',function(){
  const t=b.dataset.tab; nav('#/'+t+(t==='map'?'/'+curCity:''));
});});

/* ---------- the story sheet ---------- */
function openDoc(id){
  const src=document.getElementById('doc-'+id);
  if(!src){showTab('plan');return;}
  sbody.innerHTML='<div class="doc" style="'+(src.getAttribute('style')||'')+'">'+src.innerHTML+'</div>';
  sbody.scrollTop=0;
  slbl.textContent=src.getAttribute('data-label')||'';
  const i=ORDER.indexOf(id);
  sheetNav.style.display=i<0?'none':'';
  if(i>=0){prevB.disabled=i<=0;nextB.disabled=i>=ORDER.length-1;}
  sheet.hidden=false;sheet.classList.add('on');document.body.classList.add('locked');
  sheetOpen=id;sheetPushed=lastPush;
  sheet.focus&&sheet.focus();
}
function closeSheet(o){
  o=o||{};
  if(!sheetOpen)return;
  const wasPushed=sheetPushed;
  sheetOpen=null;sheetPushed=false;
  sheet.classList.remove('on');sheet.hidden=true;
  document.body.classList.remove('locked');sbody.innerHTML='';
  if(o.silent)return;
  if(wasPushed){history.back();}
  else{history.replaceState({},'','#/'+cur+(cur==='map'?'/'+curCity:''));}
}
function step(d){
  if(!sheetOpen)return;
  const i=ORDER.indexOf(sheetOpen);
  if(i<0)return;
  const j=i+d;
  if(j<0||j>=ORDER.length)return;
  const id=ORDER[j];
  history.replaceState({},'','#/doc/'+id);
  const keep=sheetPushed; sheetOpen=null; openDoc(id); sheetPushed=keep;
}
prevB.addEventListener('click',function(){step(-1);});
nextB.addEventListener('click',function(){step(1);});
document.addEventListener('keydown',function(e){
  if(!sheetOpen)return;
  if(e.key==='Escape'){closeSheet();}
  else if(e.key==='ArrowRight'){step(1);}
  else if(e.key==='ArrowLeft'){step(-1);}
});

/* ---------- moving within the Plan ----------
   Motion is worth having for the arrival and nothing else. Chrome caps a smooth scroll at
   about 780ms whatever the distance, so gliding the 11,262px from Beijing to Chongqing is
   seventeen screens a second -- a blur that orients nobody, and eighty photos repainted on
   the way. So hop to within a screen and a half of the target instantly, then glide that
   last stretch. A screen and a half is measured, not guessed: it is the gap between
   consecutive day blocks in 16 of the 17 cases, so tapping the next day along is smooth end
   to end, and only the long hauls arrive instead of flying.
   A tab switch stays instant, because the whole view changed and there is nothing to carry. */
function goTo(el){
  if(!el)return;
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches){
    el.scrollIntoView({block:'start'});return;}
  const m=parseFloat(getComputedStyle(el).scrollMarginTop)||0;
  const dest=el.getBoundingClientRect().top+window.scrollY-m;
  const glide=Math.round(window.innerHeight*1.5), d=dest-window.scrollY;
  if(Math.abs(d)>glide)window.scrollTo(0,dest-(d>0?glide:-glide));
  el.scrollIntoView({block:'start',behavior:'smooth'});
}

/* ---------- one delegated click handler ---------- */
function copyValue(el){
  const t=el.getAttribute('data-copy')||'';
  const done=function(){
    el.classList.add('done');
    const s=el.querySelector('em span');
    if(s){const old=s.textContent;s.textContent='Copied';
      setTimeout(function(){s.textContent=old;el.classList.remove('done');},1700);}
    else setTimeout(function(){el.classList.remove('done');},1700);
  };
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(t).then(done,function(){fallback(t);done();});
  }else{fallback(t);done();}
}
function fallback(t){
  const ta=document.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');
  ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();
  try{document.execCommand('copy');}catch(e){}
  document.body.removeChild(ta);
}
document.addEventListener('click',function(e){
  const t=e.target;
  const cl=t.closest('[data-close]'); if(cl){e.preventDefault();closeSheet();return;}
  const cp=t.closest('[data-copy]'); if(cp){e.preventDefault();copyValue(cp);return;}
  const tx=t.closest('[data-taxi]'); if(tx){e.preventDefault();nav('#/doc/taxi-'+(tx.dataset.taxi||curCity));return;}
  const go=t.closest('[data-go]');
  if(go){e.preventDefault();
    const d=go.dataset.go;
    if(go.dataset.city)curCity=go.dataset.city;
    if(go.dataset.pin)pendingPin=go.dataset.pin;
    nav('#/'+d+(d==='map'?'/'+curCity:''),{anchor:go.dataset.anchor||null});
    return;}
  const dc=t.closest('[data-doc]'); if(dc){e.preventDefault();nav('#/doc/'+dc.dataset.doc);return;}
  const cj=t.closest('[data-cj]');
  if(cj){e.preventDefault();
    const id=cj.dataset.cj, el=document.getElementById(id);
    curCity=id;
    if(cur!=='plan'){nav('#/plan',{anchor:id});}
    else{goTo(el);}
    return;}
  const rd=t.closest('.rd');
  if(rd){e.preventDefault();
    const tgt=rd.dataset.day;
    const el=document.getElementById(tgt);
    if(cur!=='plan'){nav('#/plan',{anchor:tgt});}
    else{goTo(el);}
    return;}
  const j=t.closest('.jumpto');
  if(j){e.preventDefault();goTo(document.getElementById(j.dataset.anchor));return;}
  const mc=t.closest('.mapcity'); if(mc){e.preventDefault();selectMapCity(mc.dataset.city);
    history.replaceState({},'','#/map/'+mc.dataset.city);return;}
  const tk=t.closest('.tkf'); if(tk){e.preventDefault();filterTickets(tk);return;}
  const st=t.closest('.stf'); if(st){e.preventDefault();filterStories(st);return;}
  const a=t.closest('a[href^="#"]'); if(a){e.preventDefault();nav(a.getAttribute('href'));return;}
});
$('#taxibtn').addEventListener('click',function(){
  nav('#/doc/taxi-'+(DATA[curCity]?curCity:'beijing'));
});

/* ---------- filters ---------- */
function filterTickets(btn){
  const s=btn.dataset.state;
  $$('.tkf').forEach(function(x){const on=x===btn;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on?'true':'false');});
  $$('.tkrow').forEach(function(r){r.style.display=(s==='all'||r.dataset.state===s)?'':'none';});
  $$('#v-tickets .grouphead').forEach(function(g){
    let n=0,el=g.nextElementSibling;
    while(el&&!el.classList.contains('grouphead')){if(el.classList.contains('tkrow')&&el.style.display!=='none')n++;el=el.nextElementSibling;}
    g.style.display=n?'':'none';
  });
  window.scrollTo(0,0);
}
function filterStories(btn){
  const c=btn.dataset.city;
  $$('.stf').forEach(function(x){const on=x===btn;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on?'true':'false');});
  $$('.stgroup').forEach(function(g){g.style.display=(c==='all'||g.dataset.city===c)?'':'none';});
  window.scrollTo(0,0);
}

/* ---------- the day rail follows where you are ---------- */
const dayEls=$$('#v-plan .day'), railChips=$$('#v-plan .rd'), cjBtns=$$('#v-plan .cj'),
      cityMarks=$$('#v-plan .chead');
let ticking=false, lastHere=null, lastCity=null;
function spy(){
  if(cur!=='plan')return;
  const line=stickBottom()+72;
  /* Which city you are in is the last city header you have scrolled past, not the last day
     block: a hero is ~250px tall, so between the header and its first day the day-based
     answer is still the previous city -- and that is what the Taxi button hands you. */
  let cm=null;
  for(let i=0;i<cityMarks.length;i++){if(cityMarks[i].getBoundingClientRect().top<=line)cm=cityMarks[i];}
  const city=cm?cm.dataset.city:'';
  if(city!==lastCity){
    lastCity=city;
    if(DATA[city])curCity=city;
    cjBtns.forEach(function(b){b.classList.toggle('here',b.dataset.cj===city);});
  }
  let active=null;
  for(let i=0;i<dayEls.length;i++){if(dayEls[i].getBoundingClientRect().top<=line)active=dayEls[i];}
  if(!active)active=dayEls[0];
  if(!active||active.id===lastHere)return;
  lastHere=active.id;
  let chip=null;
  railChips.forEach(function(c){const on=c.dataset.day===active.id;c.classList.toggle('here',on);if(on)chip=c;});
  if(chip&&rail){
    const want=chip.offsetLeft-rail.clientWidth/2+chip.offsetWidth/2;
    rail.scrollTo({left:Math.max(0,want),behavior:'smooth'});
  }
}
window.addEventListener('scroll',function(){
  if(ticking)return;ticking=true;
  requestAnimationFrame(function(){ticking=false;spy();});
},{passive:true});

/* ---------- today ---------- */
(function(){
  railChips.forEach(function(c){
    if(c.dataset.iso===TODAY){c.insertAdjacentHTML('beforeend','<span class="tdot"></span>');}
    if(c.dataset.iso<TODAY)c.classList.add('past');
  });
  const b=$('#todb'), l=$('#todl');
  if(TODAYi>=0){
    const d=CAL[TODAYi];
    b.textContent='Today · day '+(TODAYi+1)+' of 15 · '+d.cityname;
    l.textContent=d.theme===d.cityname?'':d.theme;
    todbar.hidden=false;
    if(!location.hash&&d.target){
      const el=document.getElementById(d.target);
      if(el)requestAnimationFrame(function(){el.scrollIntoView({block:'start'});});
    }
  }else if(TODAY<CAL[0].iso){
    const days=Math.round((new Date(CAL[0].iso)-new Date(TODAY))/864e5);
    b.textContent=days===1?'One day to go':days+' days to go';
    l.textContent='QR 1302 leaves Cairo at 19:55 on Saturday 19 September.';
    todbar.hidden=false;
  }
})();

/* ---------- the maps, loaded only when you open them ---------- */
function ensureMap(){
  if(mapLoaded){selectMapCity(curCity);return;}
  if(mapLoading)return;
  mapLoading=true;
  const l=document.createElement('link');
  l.rel='stylesheet';l.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
  document.head.appendChild(l);
  const s=document.createElement('script');
  s.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
  s.onload=function(){mapLoaded=true;mapLoading=false;selectMapCity(curCity);};
  s.onerror=function(){mapLoading=false;$('.maphint').textContent='The map could not load — no connection. The plan and the tickets still work.';};
  document.head.appendChild(s);
}
function buildMap(cid){
  const d=DATA[cid];
  const m=L.map('lmap-'+cid,{scrollWheelZoom:false});
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}).addTo(m);
  const b=[d.hotel];
  L.marker(d.hotel,{icon:L.divIcon({className:'',html:'<div class="mk star">\u{1F3E8}</div>',
    iconSize:[36,36],iconAnchor:[18,18]}),zIndexOffset:1000}).addTo(m).bindPopup('<b>Hotel</b><br>'+d.hname);
  mapMarks[cid]={};
  d.pts.forEach(function(p){
    const mk=L.marker([p.lat,p.lng],{icon:L.divIcon({className:'',
      html:'<div class="mk" style="background:'+p.col+'">'+p.n+'</div>',iconSize:[28,28],iconAnchor:[14,14]})}).addTo(m);
    mk.bindPopup('<b>'+p.n+'. '+p.title+'</b><br>'+p.day+' · '+p.slot+'<br><a href="#/doc/'+p.id+'">Read the story</a>');
    mapMarks[cid][p.id]=mk;
    if(!p.far)b.push([p.lat,p.lng]);
  });
  m.fitBounds(b,{padding:[30,30]});
  mapObj[cid]=m;
  return m;
}
function sizeMap(){
  const host=$('.mapwrap');if(!host||cur!=='map')return;
  const tabs=$('.tabs').getBoundingClientRect();
  const floor=(tabs.top>window.innerHeight/2)?tabs.top:window.innerHeight;
  const floorH=window.innerHeight<520?180:300;
  const h=Math.max(floorH,Math.round(floor-host.getBoundingClientRect().top-10));
  document.documentElement.style.setProperty('--mh',h+'px');
  for(const k in mapObj)mapObj[k].invalidateSize();
}
window.addEventListener('resize',function(){if(cur==='map')sizeMap();});
window.addEventListener('orientationchange',function(){setTimeout(function(){if(cur==='map')sizeMap();},260);});
function selectMapCity(cid){
  if(!DATA[cid])cid='beijing';
  curCity=cid;
  $$('.mapcity').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.city===cid?'true':'false');});
  $$('.map').forEach(function(m){m.classList.toggle('on',m.id==='lmap-'+cid);});
  sizeMap();
  if(!mapLoaded)return;
  if(!mapObj[cid])buildMap(cid);
  else setTimeout(function(){mapObj[cid].invalidateSize();},50);
  if(pendingPin){
    const mk=mapMarks[cid]&&mapMarks[cid][pendingPin];pendingPin=null;
    if(mk)setTimeout(function(){mapObj[cid].setView(mk.getLatLng(),16);mk.openPopup();},120);
  }
}

/* ---------- go ---------- */
showTab('plan');
$$('.mapcity').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.city===curCity?'true':'false');});
$$('.map').forEach(function(m){m.classList.toggle('on',m.id==='lmap-'+curCity);});
if(location.hash){pending={};applyHash(location.hash);}
else history.replaceState({},'','#/plan');
spy();
</script></body></html>""")

open("China-Must-Do-List-Tarek.html", "w").write("\n".join(out))
print("ok", len(items), "items,", len(ORDER), "stories")
