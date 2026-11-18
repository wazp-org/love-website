"""
Builds the Website Shop (/shop/): a simple, fast shopping page with
search, category tiles, filters, a product view, a basket and checkout.

Run from the website folder:  python3 tools/build_shop.py
(build_pages.py also runs it at the end.)

Payments: set "gateway" in exclusives.json -> settings once the Barclaycard
gateway is live. Until then, checkout offers PayPal (whole basket total) and
order by email, so the shop works today.
"""
import json, re, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.loveandbeautysales.co.uk"
src = open(os.path.join(ROOT, "products.js"), encoding="utf-8").read()
ALL = json.loads(re.search(r"LB_PRODUCTS = (\[.*\]);", src, re.S).group(1))
UPDATED = re.search(r'LB_UPDATED = "([^"]+)"', src).group(1)
EX = json.load(open(os.path.join(ROOT, "exclusives.json"), encoding="utf-8"))
S = EX.get("settings", {})
PAYPALME = re.sub(r"^https?://(www\.)?(paypal\.me|paypal\.com/paypalme)/", "", S.get("paypalme", "").strip(), flags=re.I).split("/")[0].lstrip("@")
EMAIL = "sales@loveandbeautysales.co.uk"
GATEWAY = S.get("gateway") or {}          # e.g. {"live": true, "provider": "barclaycard", "checkoutUrl": "..."}
PHOTOS = {}
pp = os.path.join(ROOT, "images", "shop", "photos.json")
if os.path.exists(pp):
    PHOTOS = json.load(open(pp, encoding="utf-8"))   # eBay item id -> improved photo file in /images/shop/

ADULT_RE = re.compile(r"masturbat|stroker|fleshlight|fleshjack|pocket pussy|bj blaster|men.s classic|onahole|tenga|blowtech|pocket pal|aliens pie|streetgirl|launch", re.I)
def is_adult(p): return p["c"] == "realistic" or (p["c"] == "him" and bool(ADULT_RE.search(p["t"])))
NO_DISCOUNT = ["lamai"]
def price(p):
    if any(w in p["t"].lower() for w in NO_DISCOUNT): return p["p"]
    return round(p["p"] * 0.85 + 1e-9, 2)

import sys; sys.path.insert(0, os.path.join(ROOT, "tools"))
from brands import brand_of  # shared with build_pages.py

CATS = [  # key, label, tile image keyword
  ("lingerie", "Lingerie"), ("vibes", "Vibrators"), ("anal", "Anal Play"), ("rings", "Cock Rings"),
  ("him", "For Him"), ("bondage", "Bondage"), ("clubwear", "Clubwear"), ("menswear", "Menswear"),
  ("lube", "Lube & Care"), ("gifts", "Gifts"), ("beauty", "Beauty")]
CATNAME = dict(CATS)

items = []
for p in ALL:
    if is_adult(p) or p["c"] not in CATNAME: continue
    sp = price(p)
    img = PHOTOS.get(p["i"])
    items.append({"i": p["i"], "t": p["t"], "c": p["c"], "b": brand_of(p["t"]) or "",
                  "p": sp, "w": p["p"], "g": p["g"], **({"m": img} if img else {}), **({"o": 1} if p.get("oos") else {})})
# "Recommended" order: mix the categories (lingerie, vibrators, anal, ...) so the
# first screen shows a bit of everything, LELO/Satisfyer and lingerie near the top.
from collections import OrderedDict
star = re.compile(r"lelo|satisfyer|womanizer|we-vibe|le wand|rocks-off|cottelli|leg avenue|abierta|amorable", re.I)
groups = OrderedDict((k, []) for k, _ in CATS)
for x in items: groups[x["c"]].append(x)
top = re.compile(r"lelo|satisfyer|womanizer|we-vibe|le wand", re.I)
def rank(x):
    return (1 if x.get("o") else 0, 0 if top.search(x["t"]) else (1 if star.search(x["t"]) else 2), 0 if x.get("m") is None else 1)
def brand_mix(lst):
    lst.sort(key=rank); seen = {}; out = []
    for x in lst:
        b = x["b"] or x["t"].split()[0]; seen[b] = seen.get(b, 0) + 1
        out.append((rank(x)[0], seen[b], rank(x)[1:], x))
    out.sort(key=lambda r: r[:3]); return [r[3] for r in out]
for k in groups: groups[k] = brand_mix(groups[k])
# weave: lingerie and vibrators appear most often near the top
PATTERN = ["lingerie", "vibes", "lingerie", "anal", "vibes", "clubwear", "lingerie", "bondage", "vibes",
           "rings", "lube", "menswear", "lingerie", "vibes", "him", "gifts"]
mixed = []
while any(groups.values()):
    for k in PATTERN:
        if groups[k]: mixed.append(groups[k].pop(0))
    for k in groups:
        if k not in PATTERN and groups[k]: mixed.append(groups[k].pop(0))
items = mixed
counts = {k: sum(1 for x in items if x["c"] == k) for k, _ in CATS}
# tile picture = first in-stock product of that category
tiles = []
for k, lab in CATS:
    if not counts[k]: continue
    first = next(x for x in items if x["c"] == k)
    tiles.append((k, lab, counts[k], first))

e = lambda s: html.escape(str(s), quote=True)
def img_url(x, size=500):
    return f"/images/shop/{x['m']}" if x.get("m") else f"https://i.ebayimg.com/images/g/{x['g']}/s-l{size}.jpg"

DATA = json.dumps(items, separators=(",", ":"), ensure_ascii=False)
CONF = json.dumps({"paypal": PAYPALME, "email": EMAIL, "gateway": GATEWAY, "nextDay": 4.99}, separators=(",", ":"))
n = len(items)
TILES = "".join(f'<button class="tile" data-c="{k}"><span class="tile-img"><img src="{img_url(f,300)}" alt="" loading="lazy"></span><span class="tile-t">{e(lab)}</span></button>' for k, lab, c, f in tiles)

PAGE = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>Shop Lingerie, Beauty &amp; Sexual Wellness | 15% Less Than eBay | Love and Beauty</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Shop {n} lingerie, beauty and sexual wellness products direct from Love and Beauty, 15% less than our eBay prices. Free discreet UK delivery, next day available.">
<link rel="canonical" href="{SITE}/shop/">
<meta property="og:title" content="Shop Love and Beauty – 15% less than eBay">
<meta property="og:image" content="{SITE}/images/welcome.jpg">
<meta name="theme-color" content="#07050a">
<link rel="icon" type="image/png" href="/images/favicon.png">
<link rel="preconnect" href="https://i.ebayimg.com">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Cormorant+Garamond:ital@1&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/shop/shop.css">
</head>
<body>
<div id="age-gate" role="dialog" aria-modal="true" aria-labelledby="gate-title" hidden>
  <div class="gate"><img src="/images/logo.png" alt="Love and Beauty">
    <h2 id="gate-title">Are you 18 or over?</h2>
    <p>Our shop includes adult products. Please confirm your age to continue.</p>
    <div class="row"><button class="b b-gold" id="gate-enter">Yes, I'm 18+</button><a class="b b-line" href="https://www.google.co.uk">Leave</a></div>
  </div>
</div>

<div class="strip"><div class="strip-in"><span>Free discreet UK delivery</span><span>Next day £4.99</span><span>15% less than our eBay prices</span><span>Family-run in Yorkshire</span></div></div>
<header class="hdr">
  <div class="hdr-in">
    <a class="logo" href="/" aria-label="Love and Beauty home"><img src="/images/logo-small.png" alt=""><span>LOVE AND BEAUTY</span></a>
    <form class="search" role="search" onsubmit="return false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 3a7.5 7.5 0 0 1 5.9 12.1l4.8 4.8-1.4 1.4-4.8-4.8A7.5 7.5 0 1 1 10.5 3Zm0 2a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11Z"/></svg>
      <input id="q" type="search" placeholder="Search lingerie, LELO, vibrators…" aria-label="Search products" autocomplete="off"><button type="button" id="q-x" class="q-x" aria-label="Clear search" hidden>×</button></form>
    <nav class="hnav"><a href="/lingerie/">Lingerie</a><a href="/sex-toys/">Wellness</a><a href="/home-parties/">Parties</a><a href="/#story">Our Story</a></nav>
    <button class="bag-btn" id="bag-open" aria-label="Open basket"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7V6a5 5 0 0 1 10 0v1h3l-1.3 13.1A2 2 0 0 1 16.7 22H7.3a2 2 0 0 1-2-1.9L4 7h3Zm2 0h6V6a3 3 0 0 0-6 0v1Z"/></svg><span id="bag-n" class="bag-n" hidden>0</span></button>
  </div>
</header>

<main>
  <section class="hero">
    <p class="eyebrow">Love and Beauty · Buy direct</p>
    <h1>WEBSITE SHOP</h1>
    <div class="star">✦</div>
    <p class="tag">Lingerie, beauty &amp; wellness, chosen with care</p>
    <p>{n} lingerie, beauty and wellness picks, <b>15% less than eBay</b>, sent free in plain packaging.</p>
  </section>

  <section class="tiles" aria-label="Shop by category"><button class="tile tile-all" data-c=""><span class="tile-img"><img src="/images/logo-small.png" alt=""></span><span class="tile-t">All</span></button>{TILES}</section>

  <div class="bar" id="bar">
    <div class="bar-l"><b id="count">{n}</b> <span id="count-l">products</span></div>
    <div class="bar-r">
      <button class="b b-sm b-line" id="filter-open">Filter</button>
      <label class="sort"><span>Sort</span><select id="sort"><option value="">Recommended</option><option value="low">Price: low to high</option><option value="high">Price: high to low</option><option value="az">Name A–Z</option></select></label>
    </div>
  </div>
  <div class="active" id="active"></div>

  <section class="grid" id="grid" aria-live="polite"></section>
  <p class="empty" id="empty" hidden>No matches. Try another word, or <button class="lnk" id="reset">clear filters</button>.</p>
  <div class="more"><button class="b b-line" id="more" hidden>Show more</button></div>

  <section class="trust">
    <div><b>Free delivery</b><span>Evri Tracked, plain unbranded packaging</span></div>
    <div><b>Next day £4.99</b><span>Order by noon, Mon–Fri</span></div>
    <div><b>Secure checkout</b><span>Apple Pay, Google Pay and cards</span></div>
    <div><b>Real people</b><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
  </section>
</main>

<footer class="ftr"><img src="/images/logo-small.png" alt=""><p>Love and Beauty Limited · Yorkshire · Adults 18+ only</p><p class="ftr-l"><a href="/">Home</a><a href="/lingerie/">Lingerie</a><a href="/beauty/">Beauty</a><a href="/sex-toys/">Sexual Wellness</a><a href="/home-parties/">Home Parties</a><a href="/ebay-shop/">eBay Shop</a><a href="/masturbators-and-dildos/">18+ section</a></p></footer>

<!-- product view -->
<div class="ov" id="pv" hidden><div class="sheet pv" role="dialog" aria-modal="true" aria-labelledby="pv-t">
  <button class="x" data-close aria-label="Close">×</button>
  <div class="pv-img"><img id="pv-img" alt=""></div>
  <div class="pv-body">
    <div class="pv-brand" id="pv-b"></div>
    <h2 id="pv-t"></h2>
    <div class="pv-price"><span id="pv-p"></span><s id="pv-w"></s><em id="pv-s"></em></div>
    <label class="pv-opt" id="pv-opt-l">Size / colour <small>(if there's a choice)</small><input id="pv-opt" placeholder="e.g. Size M, Black"></label>
    <div class="qty"><button data-q="-1" aria-label="Less">−</button><span id="pv-q">1</span><button data-q="1" aria-label="More">+</button></div>
    <button class="b b-gold b-big" id="pv-add">Add to basket</button>
    <ul class="pv-perks"><li>Free discreet delivery, or next day for £4.99</li><li>Sent in plain packaging, no brand names</li><li>14-day returns on unopened items</li></ul>
    <a class="pv-more" id="pv-ebay" target="_blank" rel="noopener">More photos and full description</a>
  </div>
</div></div>

<!-- basket -->
<div class="ov ov-side" id="bag" hidden><aside class="side" role="dialog" aria-modal="true" aria-labelledby="bag-t">
  <div class="side-h"><h2 id="bag-t">Your basket</h2><button class="x" data-close aria-label="Close">×</button></div>
  <div class="side-list" id="bag-list"></div>
  <div class="side-f" id="bag-f">
    <fieldset class="ship"><legend>Delivery</legend>
      <label><input type="radio" name="ship" value="std" checked><span>Evri Tracked <small>2–3 days</small></span><b>FREE</b></label>
      <label><input type="radio" name="ship" value="nd"><span>Evri Next Day <small>order by noon</small></span><b>£4.99</b></label>
    </fieldset>
    <div class="tot"><span>Total</span><b id="bag-tot">£0.00</b></div>
    <button class="b b-gold b-big" id="go-checkout">Checkout</button>
    <button class="lnk" data-close>Continue shopping</button>
  </div>
</aside></div>

<!-- checkout -->
<div class="ov" id="co" hidden><div class="sheet co" role="dialog" aria-modal="true" aria-labelledby="co-t">
  <button class="x" data-close aria-label="Close">×</button>
  <h2 id="co-t">Checkout</h2>
  <div class="co-sum" id="co-sum"></div>
  <div class="express" id="express">
    <p class="small">Express checkout</p>
    <div class="row"><button class="pay pay-apple" data-pay="applepay" aria-label="Pay with Apple Pay"> Pay</button><button class="pay pay-google" data-pay="googlepay" aria-label="Pay with Google Pay">G Pay</button></div>
    <div class="or"><span>or pay by card</span></div>
  </div>
  <form id="co-form" autocomplete="on">
    <div class="f2"><label>First name<input name="first" autocomplete="given-name" required></label><label>Last name<input name="last" autocomplete="family-name" required></label></div>
    <label>Email<input name="email" type="email" autocomplete="email" required></label>
    <label>Phone <small>(for delivery updates)</small><input name="phone" type="tel" autocomplete="tel"></label>
    <label>Address<input name="addr1" autocomplete="address-line1" required></label>
    <label>Address line 2 <small>(optional)</small><input name="addr2" autocomplete="address-line2"></label>
    <div class="f2"><label>Town / city<input name="town" autocomplete="address-level2" required></label><label>Postcode<input name="postcode" autocomplete="postal-code" required></label></div>
    <label class="chk"><input type="checkbox" name="adult" required> I'm 18 or over</label>
    <button class="b b-gold b-big" id="co-pay" type="submit">Pay securely</button>
    <div class="co-alt" id="co-alt">
      <p class="small">Card payments are being switched on. For now you can pay the exact total with PayPal, or send the order and we'll reply with a payment link.</p>
      <div class="row"><a class="b b-line" id="co-paypal" target="_blank" rel="noopener">Pay with PayPal</a><a class="b b-line" id="co-email">Order by email</a></div>
    </div>
    <p class="small center">Your details are only used to send your order. Plain, discreet packaging.</p>
  </form>
</div></div>

<div class="toast" id="toast" role="status" hidden></div>

<script>window.LB_ITEMS={DATA};window.LB_CONF={CONF};window.LB_CATS={json.dumps(CATNAME)};</script>
<script src="/shop/shop.js"></script>
</body>
</html>
"""
os.makedirs(os.path.join(ROOT, "shop"), exist_ok=True)
open(os.path.join(ROOT, "shop", "index.html"), "w", encoding="utf-8").write(PAGE)
print(f"/shop/  {n} products (new shop)")
