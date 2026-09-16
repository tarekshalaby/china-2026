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

Render it and look at it. Chromium is available:

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for w, tag in [(1440, "desk"), (414, "phone")]:
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.goto("file:///<repo>/index.html"); pg.wait_for_timeout(2500)
        pg.add_style_tag(content="html{scroll-behavior:auto!important}")
        pg.screenshot(path=f"/tmp/{tag}.png")
        print(tag, pg.evaluate("document.documentElement.scrollWidth-window.innerWidth"))
```

Horizontal overflow must be 0 at both widths. Then actually read the screenshots.

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

Three layers, linked both ways:

1. **Day-by-day cards** per city — time slot, title, one-line what-it-is, one practical tip,
   a status pill if there is a booking, and a "Read the story" link.
2. **A Leaflet / OpenStreetMap map** per city. Card numbers match pin numbers.
3. **Reference sections** at the bottom: Flights/trains/hotels, Tickets, Before you fly, and
   the full stories.

### Item tuple in `data.py`

```python
(id, city, day, slot, cat, title, oneliner, tip, story, far)
```

`cat` is one of: `struggle` ✊ #E53935 · `music` 🎸 #8E24AA · `food` 🍜 #FB8C00 ·
`landmark` 🏛️ #1E88E5 · `transit` 🚄 #607D8B

City colours: Beijing #F9A825 · Xi'an #00897B · Chengdu #43A047 · Chongqing #3949AB

**`build.py` numbers cards by iterating `items` in file order**, skipping `transit`. So a
block's physical position in the file must match its day order, or card numbers stop matching
map pins. When you move a stop between days, move the block too.

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
- Card tips render as their **first sentence only**; the story below shows the whole thing.
- Icons are inline SVG from the `ICON` dict in `build.py`. No icon fonts, no external images.
- City headers are a hero photo with the city colour as a gradient panel on the left.
- The 15-day ribbon at the top carries the holiday bands. It replaces prose about dates.
- Helvetica-like, white background, vibrant Material colours, generous spacing, works on a phone.
- Avoid large red blocks — they read as errors.

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

## Working with Tarek

- Ask clarifying questions as **multiple-choice options**, always ending with an
  "Anything else to add?" option.
- Avoid acronyms and jargon; spell out and explain any unavoidable technical term on first use.
- Use his local git credentials. **Never ask him for tokens.**
- Report back with the live link only once it is actually loading.
