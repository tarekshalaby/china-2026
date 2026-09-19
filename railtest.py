import os, sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else "file:///home/user/china-2026/China-Must-Do-List-Tarek.html"
ok=fail=0
def chk(l,g,wv):
    global ok,fail
    if g==wv: ok+=1
    else: fail+=1; print(f"  FAIL {l}: got {g!r} want {wv!r}")
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium",
        proxy={"server":os.environ.get("HTTPS_PROXY")},args=["--ignore-certificate-errors"])
    c=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,ignore_https_errors=True)
    pg=c.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(3000)
    isos=pg.evaluate("[...document.querySelectorAll('.rd')].map(c=>c.dataset.iso)")
    print(f"{len(isos)} chips in the rail")
    for i in isos:
        pg.click(".tabs button[data-tab='plan']"); pg.wait_for_timeout(250)
        pg.click(f".rd[data-iso='{i}']"); pg.wait_for_timeout(700)
        r=pg.evaluate("""(iso)=>{
          const view=[...document.querySelectorAll('.view')].find(v=>v.classList.contains('on')).id;
          const chip=document.querySelector(`.rd[data-iso="${iso}"]`);
          const tgt=document.getElementById(chip.dataset.day);
          const hd=tgt?tgt.querySelector('.dayhd'):null;
          const top=hd?hd.getBoundingClientRect().top:null;
          // what is actually under the sticky bars right now? measure them, never assume:
          // the chrome has changed height before and a hard-coded number quietly lies.
          const bar=document.querySelector('#v-plan .sub').getBoundingClientRect().bottom;
          const days=[...document.querySelectorAll('#v-plan .day')];
          const onscreen=days.filter(d=>{const b=d.getBoundingClientRect();return b.top<bar+180&&b.bottom>bar;});
          return {view, blockIso:tgt?tgt.dataset.iso:null, headerTop:top, bar,
                  landedOn:onscreen.length?onscreen[0].dataset.iso:null,
                  landedId:onscreen.length?onscreen[0].id:null};}""", i)
        chk(f"{i} stays in Plan", r["view"], "v-plan")
        chk(f"{i} target date matches chip", r["blockIso"], i)
        chk(f"{i} lands on that date", r["landedOn"], i)
        chk(f"{i} header below the sticky bars", bool(r["headerTop"] is not None
            and r["bar"]-20 < r["headerTop"] < r["bar"]+70), True)
    # 24/27/30 Sep must land on the FIRST block for the date, not the arrival city
    for i,expect in [("2026-09-24","day-beijing-4"),("2026-09-27","day-xian-3"),("2026-09-30","day-chengdu-3")]:
        got=pg.evaluate(f"document.querySelector('.rd[data-iso=\"{i}\"]').dataset.day")
        chk(f"{i} points at the first block of the day", got, expect)

    # the city buttons: same property, one level up. Tapping one leaves you in the Plan,
    # on a day that belongs to that city, with that city's hero header at the top.
    cids=pg.evaluate("[...document.querySelectorAll('.cj')].map(c=>c.dataset.cj)")
    print(f"{len(cids)} city buttons")
    for cid in cids:
        # start from somewhere else every time, so a pass cannot mean "was already there"
        pg.click(".tabs button[data-tab='stories']"); pg.wait_for_timeout(250)
        pg.click(".tabs button[data-tab='plan']"); pg.wait_for_timeout(250)
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
        pg.click(f".cj[data-cj='{cid}']"); pg.wait_for_timeout(800)
        r=pg.evaluate("""(cid)=>{
          const view=[...document.querySelectorAll('.view')].find(v=>v.classList.contains('on')).id;
          const bar=document.querySelector('#v-plan .sub').getBoundingClientRect().bottom;
          const hero=document.getElementById(cid).getBoundingClientRect();
          const days=[...document.querySelectorAll('#v-plan .day')];
          const onscreen=days.filter(d=>{const b=d.getBoundingClientRect();return b.top<bar+400&&b.bottom>bar;});
          return {view, heroTop:hero.top, bar,
                  landedCity:onscreen.length?onscreen[0].id.split('-')[1]:null,
                  lit:[...document.querySelectorAll('.cj.here')].map(x=>x.dataset.cj),
                  taxi:window.getComputedStyle(document.body).length>0};}""", cid)
        chk(f"{cid} stays in Plan", r["view"], "v-plan")
        chk(f"{cid} hero header sits under the sticky bars",
            bool(r["bar"]-24 < r["heroTop"] < r["bar"]+24), True)
        chk(f"{cid} first day on screen is that city's", r["landedCity"], cid)
        chk(f"{cid} is the only lit button", r["lit"], [cid])
    print(f"\n{ok} passed, {fail} failed, JS errors: {errs[:4] if errs else 'none'}")
    b.close()
