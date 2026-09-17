# China 2026 — the people's version

A one-page travel site for a four-person trip to China, 19 Sep – 3 Oct 2026.
Live at **https://tarekshalaby.github.io/china-2026/** (GitHub Pages, `main`, root).

Travellers: Tarek Shalaby, May ElMahdy (Mayouie), Mohamed Hamama, Nora Shalaby.

---

## How the site is built

```
data.py        all content and all reference data   <- edit this
places.json    photo + lat/lng per stop, keyed by id <- edit for a new stop
build.py       generator. DO NOT EDIT unless Tarek asks for a design change
     |
     v
index.html     committed, and what Pages serves
```

Workflow for any change:

```bash
# edit data.py (or places.json)
python3 build.py                              # writes China-Must-Do-List-Tarek.html
cp China-Must-Do-List-Tarek.html index.html   # index.html is what Pages serves
git add -A && git commit -m "short message" && git push origin main
```

`China-Must-Do-List-Tarek.html` is gitignored; `index.html` is the committed artifact.
Never hand-edit `index.html` — it is generated.

**Commit and push straight to `main`, never to a `claude/…` branch.** GitHub Pages
serves `main`, so anything pushed to a branch does nothing for the live site and leaves
Tarek merging it by hand from his phone. This applies to every change, in every session.

### Verify before pushing

Render it and look at it. Chromium is pre-installed but Playwright is not, and the browser is
not where Playwright expects, so both have to be pointed at:

```bash
pip install playwright     # the browser itself is already at /opt/pw-browsers/chromium
```

```python
import os
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                           proxy={"server": os.environ["HTTPS_PROXY"]},  # port changes per session
                           args=["--ignore-certificate-errors"])
    for w, h, tag in [(1440, 900, "desk"), (390, 844, "phone")]:
        pg = b.new_context(viewport={"width": w, "height": h}, is_mobile=(w < 820),
                           has_touch=(w < 820), ignore_https_errors=True).new_page()
        pg.goto("file:///home/user/china-2026/index.html"); pg.wait_for_timeout(2500)
        print(tag, pg.evaluate("document.documentElement.scrollWidth-window.innerWidth"),
                   pg.evaluate("document.documentElement.scrollHeight"))
```

Horizontal overflow must be 0 at both widths. Then actually read the screenshots.

Because it is an app now, rendering is not enough — **click through it**. At minimum: open a
stop from the Plan, use the sheet's prev/next, press the browser back button, tap a day in the
rail, filter the tickets, open the Taxi card and copy the address, switch to the Map and change
city. Check the console is clean. The Map tab must not scroll: it is sized to the viewport by
`sizeMap()` in JS, and the footer is hidden over it.

**Assert what a tap should do, not what the code does.** A test that said
`flying day -> flights` passed happily while tapping 19 Sep threw Tarek out of the Plan into
the middle of another tab. The useful check is the property: tapping any rail chip leaves you
in the Plan, on a day block whose date matches the chip, with its header just under the
sticky bars. `railtest.py` walks all 15 chips and asserts exactly that.

**A trap that has already bitten once:** `.tabs` must stay a *sibling* of `.appbar`, never a
child. `backdrop-filter` on `.appbar` makes it a containing block, which pins the "fixed"
bottom tab bar to the header instead of the viewport and silently breaks the whole phone
layout.

---

## The content brief

Priorities, in order:

1. **People's history** — class struggle, revolutions, protests, strikes, anti-colonial and
   anti-imperial history, labour history. Officially unmentionable sites (1989, the Cultural
   Revolution, Democracy Wall) belong on the list *because* they are silenced.
2. **Live music** — underground, local, passionate crowds. Listings come from Showstart 秀动
   and venue WeChat accounts, never Western aggregators.
3. **Working-class neighbourhoods**, and what gentrification and demolition did to them.
4. **Food where locals actually eat.** Offal welcome.

Not interested in: state-propaganda framing, folkloric tourist performances, tourist food
streets, generic landmark tourism. Big landmarks that the visa itinerary requires stay on the
list, but each one is reframed through its people's-history angle.

Pace: **2–3 must-dos a day.** If a day has more than that, say so.

Voice: direct and concrete. No hedging, no travel-brochure adjectives. Precise dates, names
and numbers. When a request conflicts with the brief above, say so once, offer the
alternative, then do what Tarek decides.

---

## Structure

**One file that behaves like an app.** `index.html` holds five views; only one is displayed at
a time, and a fixed tab bar switches between them with no network round trip. That is
deliberate: once the page has loaded at the hotel it keeps working when the signal drops in a
hutong or on a train, which separate pages would not.

| Tab | What is in it |
|---|---|
| **Plan** | All 15 days in one scroll, grouped by city. Opens on today's real date during the trip. |
| **Map** | One Leaflet map per city, lazy-loaded. Pin numbers match the Plan numbers. |
| **Tickets** | Booking rows, filterable by status. Tap any reference to copy it. |
| **Travel** | Hotels, trains, flights, before you fly — hotels first, because the address is the thing you need in a hurry. |
| **Stories** | An index of all 90 stories. Tapping one opens the same sheet the Plan does. |

A stop is a **compact row** on a phone (84px photo, slot, title, one-liner) and the same DOM
becomes a **photo card** in a grid at ≥820px. Tapping a stop opens a **full-screen sheet** with
the photo, the whole tip, the story, and prev/next arrows to read straight through. Stories are
rendered **once**, into a hidden `#bank`; the sheet copies them in. Never render a story twice.

A **Taxi** button in the top bar is on every screen: it opens the current city's hotel address
in large Chinese, tap-to-copy, with the phone as a tap-to-call link. "Current city" follows
whichever day you last scrolled past.

Routing is hash-based: `#/plan`, `#/map/chengdu`, `#/doc/panjiayuan`. Every old anchor
(`#story-x`, `#ticket-x`, `#hotel-x`, `#day-city-n`, `#beijing`, `#prep`) still resolves, so
links Tarek has already sent anyone keep working. The browser back button closes the sheet.

**The day rail must never leave the Plan.** It has a chip per ribbon day, so the Plan must
have a block for every one of those 15 days — including the two flying days, which are real
blocks (`day-air-0`, `day-air-1`) carrying their flight legs, not a jump to the Travel tab.
`FIRSTBLOCK` in `build.py` maps each date to the **first** block that renders for it, because
24, 27 and 30 Sep each appear twice — you start those days in one city and end them in the
next, and a chip that skipped to the arrival city skipped that last morning.

### Item tuple in `data.py`

```python
(id, city, day, slot, cat, title, oneliner, tip, story, far)
```

`cat` is one of: `struggle` ✊ #E53935 · `music` 🎸 #8E24AA · `food` 🍜 #FB8C00 ·
`landmark` 🏛️ #1E88E5 · `transit` 🚄 #607D8B

City colours: Beijing #F9A825 · Xi'an #00897B · Chengdu #43A047 · Chongqing #3949AB

**`build.py` numbers stops by iterating `items` in file order**, skipping `transit`. So a
block's physical position in the file must match its day order, or the row numbers stop
matching the map pins. When you move a stop between days, move the block too.

Every stop needs: a Wikimedia Commons photo, coordinates, a Chinese name in the title, and a
plain-English story with real dates and names. Fetch photos from the Commons API with a
descriptive User-Agent and strip `?utm_source=` from thumb URLs.

### Gotcha: apostrophe escaping in `data.py` is inconsistent

Some strings contain `\'`, others a plain `'`. Before any string replacement, check the exact
bytes: `grep -n "the text" data.py | cat -A`. Prefer line-range edits for whole tuples.

---

## Design language

Tarek's standing instruction: **no walls of text, visual wherever possible, nothing crowded.**

- Reference rows are always three layers: **fact chips** you can scan, **one short sentence**,
  then the caveats folded into a `<details>` "small print". Never a paragraph in the open.
- Chip tones: `k` settled/green, `w` needs attention/amber, `n` neutral fact.
- **Mobile first, literally.** The base CSS is the phone. `@media (min-width:820px)` is the
  only real upgrade, and it moves the tab bar from the bottom of the screen to under the
  title, and turns stop rows into photo cards. Never write a desktop rule and then undo it.
- Stop rows show the one-liner, never the tip. The tip belongs in the sheet, in full.
- Icons come from the `ICON` dict in `build.py` and are emitted **once** as a `<symbol>`
  sprite; `ic()` writes a `<use>`. Inlining them cost 110KB and thousands of DOM nodes.
- City headers are a hero photo with the city colour as a gradient panel.
- The 15-day ribbon is now the **sticky day rail** at the top of Plan: it carries the holiday
  bands, marks today with a dot, follows your scroll, and jumps you to any day in one tap.
- Helvetica-like, white background, vibrant Material colours, generous spacing.
- Avoid large red blocks — they read as errors.
- Tap targets are 40px minimum. Anything you might need in a panic (the Chinese address, a
  booking reference, the hotel phone) is one tap and copies or dials.

---

## Privacy

The site is **public and crawlable-adjacent** (`robots.txt` disallows all, `noindex` meta).
Tarek has accepted booking numbers, PINs, ticket numbers and flight references in plain text.

**Never put passport numbers on the page** — not even partially. Every gate reads the physical
passport, so the number serves no purpose, and three of the four passports belong to people who
did not choose to publish them. Note that Trip.com's Mutianyu cable-car email lists the four
"admission voucher codes" which are in fact the four passport numbers; they stay off the page.

---

## Fixed facts

Dates, hotels and trains are **booked and fixed** — never re-plan around them.

| | |
|---|---|
| Flights | QR 1302 Cairo 19:55 → Doha, 19 Sep · QR 892 Doha 02:10 → Beijing Daxing 15:00, 20 Sep · QR 881 Chongqing 01:50 → Doha, 3 Oct · QR 1307 Doha 07:35 → Cairo 11:00, 3 Oct. No checked baggage included. |
| Beijing | 20–24 Sep, Manxin Mansion, Houhai / Drum Tower. Two rooms. |
| Xi'an | 24–27 Sep, Jinjiang Bell Tower Original Copy. |
| Chengdu | 27–30 Sep, Wenjun Courtyard. |
| Chongqing | 30 Sep – 3 Oct, Miss Xie's House With Riverview. Desk closes 18:00. |
| Trains | G353 24 Sep Beijing West 12:55 → Xi'an North 17:08 · D1927 27 Sep Xi'an North 11:35 → Chengdu East 15:03 · G8619 30 Sep Chengdu East 12:50 → Shapingba 14:01. All ticketed. |

Holidays inside the trip: **Mid-Autumn 25–27 Sep** (all of Xi'an), **National Day Golden Week
1–7 Oct** (Chongqing sits in days 1–2; 30 Sep is the heaviest travel day of the Chinese year).
Mon 28 and Tue 29 Sep in Chengdu are the only clear days in the second half.

Music reality, established from Showstart: fRUITYSPACE, School Bar and .TAG do not publish
online at all (door/WeChat only). DDC is dark 19 Sep – 11 Oct. All four listed Chengdu venues
are empty on 27–29 Sep. The best show in the fortnight is God Is An Astronaut at 疆进酒 OMNI
SPACE on Wed 23 Sep, ¥320.

---

## Still to book

As of 17 Sep 2026. Everything else on the trip is booked and paid.

| What | When | Where | Who can do it |
|---|---|---|---|
| **Forbidden City** ¥60 x4 | Wed 23 Sep, afternoon | bookingticket.dpm.org.cn | Browser, Tarek's login |
| **Tiananmen Square** free | Wed 23 Sep | yuyue.tap.com.cn / WeChat mini-program | Phone, likely WeChat only |
| **God Is An Astronaut** ¥320 x4 | Wed 23 Sep, 20:00 | Showstart, at 疆进酒 OMNI SPACE | **Phone only** |
| **Naire 奈热** ¥158 x4 | Sat 26 Sep, doors 20:00 | Showstart, at 光圈CLUB | **Phone only** |
| **Xi'an food tour** | Thu 24 Sep, ask 19:00 | Lost Plate, direct | Browser + email |
| **Sichuan Cuisine Museum** ¥360 x4 | Mon 28 Sep, 13:50–17:40 | Direct or Trip.com | Browser |
| **Shaanxi History Museum** free | Sun 27 Sep, optional | Museum WeChat account | **Phone only** |
| **Jianchuan driver** | Tue 29 Sep, full day | Chengdu hotel desk | In person, on arrival |

Also outstanding: the **Temple of Heaven QR code** has not arrived. It is the entry
method for Mon 21 Sep. Chase +86 186 1124 1332.

Notes that cost time to rediscover:

- The Palace Museum releases at **20:00 Beijing, 7 days ahead**, and its API exposes a
  `canBuyDays` counter confirming the window. **Afternoon sessions survive longest.**
  Sold out at first look is not final — unpaid orders drop back into the pool roughly
  every ten minutes, and **20:30–21:00 Beijing** is the strongest refresh window.
- Do not script against their `/lotsapi/` endpoints. It is a real-name system with a
  daily cap; automated probing risks the account the tickets are booked in. Drive the
  normal UI.
- Showstart needs a Chinese number or a WeChat login. No browser reaches it.
- Tarek presses the pay button. Fill the forms, stop at checkout.

Settled, do not raise again: checked baggage **is** included on all four Qatar segments
(the confirmation PDFs are wrong, Manage Booking is the truth); seats are picked at
online check-in 48 hours out; the 13-day eSIM covers all 13 nights in China; no travel
insurance is wanted; **no cash will be carried at any point** — ATM on arrival if ever
needed.

---

## Working with Tarek

- Ask clarifying questions as **multiple-choice options**, always ending with an
  "Anything else to add?" option.
- Avoid acronyms and jargon; spell out and explain any unavoidable technical term on first use.
- Use his local git credentials. **Never ask him for tokens.**
- Report back with the live link only once it is actually loading.
