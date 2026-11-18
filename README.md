# The World in One Day — Wednesday 18 November 2026

One image summing up the world news of **Wednesday 18 November 2026**,
entered in make.fun's `news-image-20261118` competition.

![The front page](entry.png)

## What's on the page

- **Lead — Shenzhen:** Xi Jinping opens the APEC summit in Shenzhen;
  Donald Trump flies in from Manila ahead of Thursday's three-way
  meeting with Xi and Vladimir Putin.
- **The Gulf:** Kuwait and Bahrain intercept Iranian drones; a gas
  tanker burns in Hormuz and 21 crew are brought ashore; oil climbs.
- **Ukraine:** UN monitors count 372 civilians killed in October.
- **Business:** Nvidia posts $115.8 billion of quarterly revenue; its
  board rules out Jensen Huang's return as chief executive.
- **Weather:** Cyclone Akvan strengthens over the Bay of Bengal.
- **United States:** the NSA's classified internal network goes down.
- **Space:** SpaceX catches a returning Starship in mid-air.
- Briefs: Israel's new Knesset speaker, Latvia's confidence vote,
  Gaza aid kitchens, a U.S. sentencing, India's SAFF title, Zverev's
  year-end No. 1, deep-sea life, and the Siberia plane crash.

Every item was reported on 18 November 2026 (Le Monde, Al Jazeera,
ABC Australia, BBC World, the Guardian's live coverage, UN HRMMU
figures carried on the wires, the India Meteorological Department's
warnings, and Gizmodo's space reporting, all dated that day).

## How it is built

- `make_image.py` — draws the front page with Pillow: a navy masthead
  naming the day, a hand-drawn Shenzhen dusk skyline for the lead
  story, and a flat-illustration scene panel for each of the six
  cards. Real fonts throughout, so no text is garbled.
- `entry.png` — the rendered picture (1024×1024, ~143 KB).
- `main.py` — the entry program (Python 3.13, standard library only).
  It validates `entry.png` against the gate (PNG, ≤ 1 MiB,
  ≤ 1024×1024) and copies it byte for byte to the output directory,
  so both grader runs write identical bytes.

Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Redraw the picture with `python3 make_image.py` (needs Pillow; the
entry program itself needs nothing beyond the standard library).

## License

MIT — see `LICENSE`.
