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
sticky bars. `railtest.py` walks all 15 chips and asserts exactly that, then the same
property one level up for the four city buttons: you stay in the Plan, the first day on
screen belongs to that city, its hero header sits under the bars, and only that button is lit.

The test measures the sticky bars instead of hard-coding their height. An earlier version
compared against a literal `116`, and when the header grew by seven pixels every chip
started "failing" while the page was in fact correct. Measure the chrome, never assume it.

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
4. **Food where locals actually eat** — **but no offal.** Tarek does not want it: no intestine,
   tripe, brain, kidney, lung, blood or head as the point of a dish. This overrides how good or
   how local a place is, and it is why Ming Ting, the best-regarded restaurant that was ever on
   this list, was dropped on 18 Sep. A market or a hotpot having offal on the menu is fine; a
   dish or a card that leads with it is not. Do not propose 卤煮, 爆肚, 夫妻肺片 or
   脑花 again.

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
| **Stories** | An index of all 83 stories. Tapping one opens the same sheet the Plan does. |

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

### Directions: never ship our own coordinates to Amap

Every stop, hotel and taxi card has a **Directions in Amap** button. It is a keyword search
against Amap's own POI database, scoped to the city — `uri.amap.com/search?keyword=…&city=…`
— and it deliberately carries **no coordinates**. Three reasons, all found the hard way:

1. **Coordinate systems.** Amap draws on GCJ-02, the mandated Chinese offset grid. Ours are
   WGS-84 from OpenStreetMap and Wikimedia. Handing them over unconverted puts every pin
   300–500m out. Converting is easy, and it is not enough.
2. **Our coordinates are not metre-accurate and cannot be made so.** An audit of the 86
   places found 26 stored coarsely enough to be 60–740m wrong at source. OpenStreetMap has
   no record at all for 13 of them (交通茶馆, 重庆工业博物馆, 红卫兵墓园, MAO Livehouse), and
   fuzzy geocoding made it worse: "足疗 西安市" matched a foot massage shop in Toronto,
   "坚果 重庆市" a school in Japan. There is no open source of truth for Chinese POIs.
3. **Venues move.** Nuts Livehouse relocated in 2026; our stored pin was still its 2009–2014
   address in Shapingba, about 10km out. Amap's record tracks the move. A coordinate never
   will.

A search also handles chains correctly — 南城香 has 160 branches, and Amap sorts them by
distance from wherever you are standing, which one pin never could.

So the two coordinate systems never meet. The site's Leaflet map stays WGS-84, which is
correct for OSM tiles and is for orientation. Navigation is Amap's job, by name.

`build.py` derives the search term from the Chinese name in the title — Chinese characters
and digits only, because letting Latin in drags trailing English into the query. Where the
derived term is wrong or too vague, put an explicit `"amap"` field on that place in
`places.json`; that is why `maocq` searches "MAO Livehouse" and `muxidi` searches
"木樨地地铁站" rather than a 40km avenue. Terms like 足疗, 按摩 and 烤鱼 are left generic on
purpose: those stops mean "find one near you".

**Every stop needs its Chinese name in the title** — the brief already said so, and the
directions button now depends on it.

**Jumping to a city.** Four buttons sit above the day rail, in the same sticky block: city
colour, city name, and the one you are in is filled. They do not scroll sideways — all four
are one tap from anywhere in the Plan, which is the whole point — so they are `flex:1 1 auto`
and size to their names, because equal quarters clipped "Chongqing" at 320px.

Which city you are in is read from the **last city header you scrolled past**, not the last
day block. A hero is about 250px tall, so between a city's header and its first day a
day-based answer still says the previous city — and that is the city the Taxi button was
handing you. `spy()` tracks `.chead[data-city]` for that reason.

**Jumps glide the last stretch, and only the last stretch.** `goTo()` in the JS hops to
within a screen and a half of the target instantly, then smooth-scrolls the rest. Chrome
caps a smooth scroll at about 780ms *whatever the distance*, so animating the 11,262px from
Beijing to Chongqing is seventeen screens a second — a blur that orients nobody, and eighty
photos repainted on the way (worst frame 47ms, against 21ms capped). A screen and a half is
measured, not guessed: it is the gap between consecutive day blocks in 16 of 17 cases, so
tapping the next day along stays smooth end to end. `prefers-reduced-motion` lands instantly,
and a tab switch always does — the whole view changed, so there is no continuity to carry.

`railtest.py` waits for the page to stop moving rather than for a fixed number of
milliseconds. A fixed wait raced the 655ms animation and would have gone flaky on a slow
phone before it ever failed here.

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
- The 15-day ribbon is now the **sticky day rail** at the top of Plan: it marks today with a
  dot, follows your scroll, and jumps you to any day in one tap. Above it, the four **city
  buttons**. The row the city buttons needed came from the holiday bands, which used to be a
  labelled row of their own: a holiday is now a coloured cap across the top of the days it
  covers (`.rd.hol`), and its name lives on the city header, narrowed to the days you are
  actually in that city — "Mid-Autumn 25–26 Sep" on Xi'an, "27 Sep" on Chengdu. Both are
  derived from `bands` in `data.py`; nothing about a holiday is written twice.
- There is no category key row. Five categories, each already wearing its emoji badge on
  every photo, did not need a legend taking a line off the top of the Plan.
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
are empty on 27–29 Sep. Both ticketed shows in the window — God Is An Astronaut and Naire —
are dropped, so live music is door-only now and decided on the night.

---

## Still to book

As of 17 Sep 2026, evening. Everything else on the trip is booked and paid.

Booked today: the **Forbidden City** (23 Sep afternoon, four standard, ¥240, no number
issued — the passport is the ticket), **Tiananmen Square** (23 Sep 06:03–12:00, free,
checkpoint 广场东侧路北安检03, ref R260917210725076173) and the **Sichuan Cuisine Museum
cooking class** (28 Sep, meet 12:50, three dishes, ¥1,390, Trip.com 1658115212363279 · PIN
3338). All three are in `bookings` in `data.py` and live on the Tickets tab.

**The Lost Plate Xi'an food tour is dropped** — Tarek does not want a tour aimed at foreigners,
and the fixed 18:00 departure did not survive a 17:08 arrival at Xi'an North anyway. The stop
is deleted, not deferred; do not reinstate it. Thursday night in Xi'an is the Bell Tower and
the wall, then Sajinqiao, which was always the un-touristed version of the same food.

| What | When | Where | Who can do it |
|---|---|---|---|
| **Huaiyang Fu dinner** | Sun 20 Sep, 19:30 | Message Manxin Mansion, who call 010 6426 5959 | Anyone, and it has to be today |
| **Jianchuan driver** | Tue 29 Sep, full day | Chengdu hotel desk | In person, on arrival |

**The Temple of Heaven QR codes arrived on 19 Sep** — four of them, one per person, in the
Trip.com app's Attractions & Tours chat rather than by email, which is why the inbox stayed
empty. Nothing is outstanding on Mon 21 Sep any more; do not re-raise the chase. Each code is
issued against one passport, so all four passports still travel to the gate. The message also
confirms the ticket is park admission only — Hall of Prayer, Echo Wall and Circular Mound
Altar excluded — and that the “English guide” is a web audio tour, not a person. **The codes
themselves, and the masked passport numbers printed beside each name, stay off the page.**

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

**Suppliers phone the contact number the day before.** Mutianyu calls by 22:00 on the 21st,
the cuisine museum by 20:00 on the 27th. The number on file is +20 1142002004, an Egyptian
mobile, and the eSIM is data only — so either keep Egyptian roaming alive for voice or watch
the Trip.com in-app messages daily. A missed call on a private charter is a real problem.

**Changed on 19 Sep: 20 Sep is Tarek's birthday.** The group wanted somewhere nice, so the
arrival-day dinner is now **Huaiyang Fu 淮扬府** (Michelin one star, Andingmen branch,
198 安定门外大街, ~¥200 a head, 15 min by taxi) and **Zhang Mama is dropped** — there was no
free dinner slot left in Beijing to move it to. Say so once and move on: a starred restaurant
is not "where locals actually eat", and it is his birthday.

The fallback is written into the stop's own tip rather than added as a second stop, the way
fRUITYSPACE carries Dorena: **Kaorouji 烤肉季** on Yinding Bridge, 1848, 13 minutes' walk,
walk-ins, ask upstairs for the iron griddle and the tower view.

Three things that decided it, so nobody re-litigates them:

- **Da Dong would have been the pick** — one star, the upscale duck — but **23 Sep dinner is
  already Peking duck** at Siji Minfu. Check the other days' dinners before proposing a
  restaurant.
- **Mei Mansion 梅府家宴 has closed.** It was the obvious courtyard answer on Houhai's south
  bank, next to Prince Gong's Mansion; the brand moved to Shanghai as Salon Mei. Do not
  propose it.
- **No Michelin-starred restaurant is within walking distance of Gulou.** The nearest are
  10–15 minutes by taxi: King's Joy 京兆尹 (two stars, vegetarian, Wudaoying), TRB Hutong
  (one star, French, in Zhizhu Temple), Huaiyang Fu, Da Dong.

**Dropped on 18 Sep, do not reinstate:** Ming Ting 明婷饭店 — the pig-brain mapo tofu is the
dish and Tarek will not eat it. Replaced by **Yutian 雨田饭店** on 红星路二段, opened 1985 by Lei
Ailing with ¥400 and four tables, doing lotus-leaf steamed pork, red-braised pork and lotus-root
soup at ¥40–60 a head.

**Dropped on 17 Sep, do not reinstate:** God Is An Astronaut (an Irish touring band, and only
ever the fallback if School Bar was dark), Naire 奈热 at 光圈CLUB on 26 Sep — the last ticketed
show, and the Aperture stop went with it — the Shaanxi History Museum (imperial bronzes, 90
rushed minutes before the 11:35 train, and furthest of anything from the brief), Chen Mapo Tofu
(the cooking class is that lunch, and no other day has a free lunch slot), Little Bar, Dongjiao
Memory and .TAG.

**The group splits on late nights.** Nora and May are not the late-night crowd. Tarek and Hamama
are happy with a drink at any bar, which needs no planning and no stop on the page — so do not
add club or late-gig stops for their sake. No concert is booked at all now: what is left is
door-only (School Bar, fRUITYSPACE), walked into on the night or skipped.

**Booking state lives in one place: the `bookings` dict in `data.py`, rendered on the Tickets
tab.** Do not start a side tracker in another file — a second source of truth is what caused
a whole session to be spent reconstructing what was already booked. If a local folder looks
empty or stale, it is not the repo: check `git remote -v`, and that a fetch refspec exists
(`git config --get-all remote.origin.fetch`), before concluding anything is missing.

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
