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
          // what is actually under the sticky bars right now?
          const days=[...document.querySelectorAll('#v-plan .day')];
          const onscreen=days.filter(d=>{const b=d.getBoundingClientRect();return b.top<300&&b.bottom>116;});
          return {view, blockIso:tgt?tgt.dataset.iso:null, headerTop:top,
                  landedOn:onscreen.length?onscreen[0].dataset.iso:null,
                  landedId:onscreen.length?onscreen[0].id:null};}""", i)
        chk(f"{i} stays in Plan", r["view"], "v-plan")
        chk(f"{i} target date matches chip", r["blockIso"], i)
        chk(f"{i} lands on that date", r["landedOn"], i)
        chk(f"{i} header near the top", bool(r["headerTop"] is not None and 90 < r["headerTop"] < 200), True)
    # 24/27/30 Sep must land on the FIRST block for the date, not the arrival city
    for i,expect in [("2026-09-24","day-beijing-4"),("2026-09-27","day-xian-3"),("2026-09-30","day-chengdu-3")]:
        got=pg.evaluate(f"document.querySelector('.rd[data-iso=\"{i}\"]').dataset.day")
        chk(f"{i} points at the first block of the day", got, expect)
    print(f"\n{ok} passed, {fail} failed, JS errors: {errs[:4] if errs else 'none'}")
    b.close()
