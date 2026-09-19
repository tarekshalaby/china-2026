import os, sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else "file:///home/user/china-2026/China-Must-Do-List-Tarek.html"
ok=fail=0
SETTLE = """() => new Promise(done => {
  // a jump now glides the last stretch, so wait for the page to stop moving rather than
  // for a number of milliseconds: a fixed wait races the animation on a slow phone.
  let prev = -1, still = 0;
  const t0 = performance.now();
  const tick = () => {
    const y = Math.round(window.scrollY);
    still = (y === prev) ? still + 1 : 0; prev = y;
    if (still > 6 || performance.now() - t0 > 3000) done(true); else requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})"""
def settle(pg): pg.evaluate(SETTLE)
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
        pg.click(f".rd[data-iso='{i}']"); settle(pg)
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
        pg.evaluate("window.scrollTo(0,0)"); settle(pg)
        pg.click(f".cj[data-cj='{cid}']"); settle(pg)
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
    # a long jump must not animate the whole way, and reduced motion must not animate at all
    pg.evaluate("window.scrollTo(0,0)"); settle(pg)
    # where the page sits the instant the click returns is the end of the instant hop;
    # everything after that is the animation, and that is what must stay bounded.
    afterHop=pg.evaluate("""()=>{
      document.querySelector('.cj[data-cj="chongqing"]').click();
      return Math.round(window.scrollY);}""")
    settle(pg)
    glide=abs(pg.evaluate("Math.round(window.scrollY)")-afterHop)
    chk("a long jump animates at most a screen and a half", bool(glide <= round(844*1.5)+2), True)
    chk("...and still animates: it is a glide, not a teleport", bool(glide > 200), True)

    c2=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,
                     ignore_https_errors=True,reduced_motion="reduce")
    p2=c2.new_page(); p2.goto(URL); p2.wait_for_timeout(3000)
    p2.evaluate("window.scrollTo(0,0)"); settle(p2)
    moved=p2.evaluate("""()=>{const y=window.scrollY;
      document.querySelector('.cj[data-cj="chongqing"]').click();
      return Math.round(window.scrollY)-y;}""")
    chk("reduced motion lands in one frame, no animation", bool(abs(moved) > 9000), True)
    settle(p2)
    chk("reduced motion still lands on Chongqing",
        p2.evaluate("[...document.querySelectorAll('.cj.here')].map(x=>x.dataset.cj)"), ["chongqing"])

    print(f"\n{ok} passed, {fail} failed, JS errors: {errs[:4] if errs else 'none'}")
    b.close()
