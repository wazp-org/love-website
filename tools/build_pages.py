"""
Builds a separate page for each shop category (e.g. /vibrators/), plus
sitemap.xml and robots.txt, from the product list in products.js.

Run from the website folder:  python3 tools/build_pages.py
Re-run it whenever products.js is refreshed from eBay.
"""
import json, re, html, os, datetime

SITE = "https://www.loveandbeautysales.co.uk"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EBAY_SHOP = "https://ebay.io/m/vXRRmt"

src = open(os.path.join(ROOT, "products.js"), encoding="utf-8").read()
PRODUCTS = json.loads(re.search(r"LB_PRODUCTS = (\[.*\]);", src, re.S).group(1))
UPDATED = re.search(r'LB_UPDATED = "([^"]+)"', src).group(1)

# Explicit items (male masturbators/strokers and all realistic toys & dildos) are kept off the
# main site and only shown on the separate 18+ page /masturbators-and-dildos/.
# The same rule is used in index.html (ADULT_RE) - keep the two in step.
ADULT_RE = re.compile(r"masturbat|stroker|fleshlight|onahole|tenga|blowtech|pocket pal|aliens pie|streetgirl|launch", re.I)
def is_adult(p):
    return p["c"] == "realistic" or (p["c"] == "him" and bool(ADULT_RE.search(p["t"])))
ALL_PRODUCTS = PRODUCTS
ADULT = [p for p in ALL_PRODUCTS if is_adult(p)]
PRODUCTS = [p for p in ALL_PRODUCTS if not is_adult(p)]

# slug, sub-categories, nav name, page title, H1, meta description, intro paragraphs
PAGES = [
  dict(slug="sex-toys", subs=["vibes","anal","rings","him"], order=["vibes","vibes","vibes","rings","vibes","anal","vibes","him"], name="Sexual Wellness",
       title="Sex Toys & Sexual Wellness UK | Vibrators, Massagers & More | Love and Beauty",
       h1="SEXUAL WELLNESS",
       desc="Shop {n} sexual wellness products and sex toys from LELO, Satisfyer, CalExotics, Rocks-Off and more: vibrators and massagers, anal play, couples rings and toys for him. Discreet UK delivery from Rotherham.",
       intro=["Our sexual wellness collection: vibrators and massagers, anal play, cock rings and couples enhancers, and toys for him, from trusted brands including LELO, Satisfyer, CalExotics, Rocks-Off and ToyJoy.",
              "Love and Beauty Limited is a family-run business in Rotherham, South Yorkshire. Every order is packed by hand and sent in plain, unbranded packaging, with secure checkout through our eBay shop."]),
  dict(slug="vibrators", subs=["vibes"], name="Vibrators & Massagers",
       title="Vibrators & Massagers UK | Rabbit, Wand & Clitoral Vibrators | Love and Beauty",
       h1="VIBRATORS & MASSAGERS",
       desc="Shop {n} vibrators and massagers: rabbit vibrators, wand massagers, clitoral suction toys, G-spot vibrators, bullets and love eggs from LELO, Satisfyer and more. Discreet UK delivery.",
       intro=["Rabbit vibrators, wand massagers, air-pulse clitoral stimulators, G-spot vibrators, bullets, finger vibes and remote-control love eggs, from LELO, Satisfyer, Le Wand, CalExotics, Rocks-Off, Love to Love and more.",
              "Most are rechargeable, body-safe silicone and waterproof. All orders are sent discreetly from Rotherham, South Yorkshire."]),
  dict(slug="anal-toys", subs=["anal"], name="Anal Play",
       title="Anal Toys UK | Butt Plugs, Anal Beads & Prostate Massagers | Love and Beauty",
       h1="ANAL PLAY",
       desc="Shop {n} anal toys: butt plugs, anal beads, vibrating plugs, prostate massagers, anal training kits and douches from LELO, b-Vibe and more. Discreet UK delivery.",
       intro=["Butt plugs, anal beads, vibrating and remote-control plugs, prostate massagers, beginner training kits and douches from LELO, b-Vibe, Rocks-Off, CalExotics, Dorcel and more.",
              "Beginner-friendly through to advanced, sent discreetly from Rotherham, South Yorkshire."]),
  dict(slug="cock-rings", subs=["rings"], name="Cock Rings & Enhancers",
       title="Cock Rings UK | Vibrating Cock Rings & Couples Enhancers | Love and Beauty",
       h1="COCK RINGS & ENHANCERS",
       desc="Shop {n} cock rings and enhancers: vibrating cock rings, couples rings, stretchy ring sets and ball stretchers from Hot Octopuss, CalExotics, Rocks-Off and more. Discreet UK delivery.",
       intro=["Vibrating cock rings, rechargeable couples enhancers, stretchy ring sets and ball stretchers from Hot Octopuss, CalExotics, Rocks-Off, ToyJoy and more.",
              "Sent in plain packaging from our family-run business in Rotherham, South Yorkshire."]),
  dict(slug="male-sex-toys", subs=["him"], name="Toys for Him",
       title="Toys for Him UK | Penis Pumps, Extenders & Chastity | Love and Beauty",
       h1="TOYS FOR HIM",
       desc="Shop {n} products for him: penis pumps, extenders, chastity devices and massagers from CalExotics, Pumped, MaleEdge and more. Discreet UK delivery.",
       intro=["Penis pumps, extenders, chastity devices and massagers for him from CalExotics, Pumped, MaleEdge, ManCage and more.",
              "Every order is sent in plain, unbranded packaging from Rotherham, South Yorkshire."]),
  dict(slug="lingerie", subs=["lingerie","clubwear"], name="Lingerie", img="lingerie.jpg",
       filters=[("Bra Sets", r"\bbra\b|bralette"), ("Basques & Corsets", r"basque|corset|bustier"),
                ("Bodies & Teddies", r"\bbody\b|bodysuit|teddy|catsuit"), ("Babydolls & Chemises", r"babydoll|chemise|slip\b|negligee"),
                ("Stockings & Suspenders", r"stocking|suspender|garter|tights|hold.?ups"), ("Plus Size", r"plus size|curves|queen|xl-|3xl|4xl"),
                ("Dresses & Clubwear", r"dress|skirt|wet ?look|vinyl|latex|clubwear|jumpsuit")],
       title="Lingerie UK | Bra Sets, Basques, Bodies & Stockings | Love and Beauty",
       h1="LINGERIE",
       desc="Shop {n} lingerie and clubwear pieces: lace bra sets, basques and corsets, bodies, babydolls, stockings and suspenders, dresses and wet look clubwear from Cottelli, Leg Avenue, Abierta Fina, Noir Handmade and more, including plus sizes. UK delivery.",
       intro=["Silk, lace and quiet confidence. Lace bra and thong sets, basques and corsets, bodies and teddies, babydolls, stockings and suspender belts, plus dresses and wet look clubwear for a night out.",
              "We stock Cottelli, Leg Avenue, Abierta Fina, Amorable by Rimba, Le Desir, Noir Handmade and Black Level, in sizes from S to 4XL. Every order is wrapped with care and sent discreetly from Rotherham, South Yorkshire."],
       extra=[("Sizes S to 4XL", "Most sets come in several sizes and many are available in plus sizes. If you're between sizes, email us and we'll help."),
              ("Gift-ready", "Buying for someone else? Every order is packed in plain, unbranded packaging, ready to give."),
              ("Real stock, ready to send", "Everything you see is in our Rotherham stock room and dispatched quickly.")]),
  dict(slug="bondage", subs=["bondage"], name="Bondage & Restraints",
       title="Bondage Gear UK | Cuffs, Collars, Floggers & Restraints | Love and Beauty",
       h1="BONDAGE & RESTRAINTS",
       desc="Shop {n} bondage items: leather cuffs, collars, floggers, gags, hoods, bed restraints and nipple clamps from Rimba, Rouge Garments, Ouch! and more. Discreet UK delivery.",
       intro=["Leather wrist and ankle cuffs, collars and leads, floggers, gags, hoods and masks, bed restraint systems and nipple clamps from Rimba, Rouge Garments, Ouch!, CalExotics and more.",
              "Sent in plain packaging from our family-run business in Rotherham, South Yorkshire."]),
  dict(slug="fetishwear", subs=["clubwear","menswear"], name="Fetish & Clubwear",
       title="Fetishwear & Clubwear UK | Wet Look, Vinyl, Latex & Men's Underwear | Love and Beauty",
       h1="FETISH & CLUBWEAR",
       desc="Shop {n} fetishwear and clubwear pieces: wet look and vinyl dresses, latex, catsuits, costumes, men's underwear and harnesses from Noir Handmade, Black Level, Svenjoyment and more.",
       intro=["Wet look and vinyl dresses, latex, catsuits and costumes, plus men's underwear, jockstraps and harnesses from Noir Handmade, Black Level, Rimba, Svenjoyment, NEK and more.",
              "Sent discreetly from Rotherham, South Yorkshire."]),
  dict(slug="lubricants", subs=["lube"], name="Lubes & Intimate Care",
       title="Lubricants & Intimate Care UK | Kegel Balls, Dilators & Toy Cleaner | Love and Beauty",
       h1="LUBRICANTS & INTIMATE CARE",
       desc="Shop {n} intimate care products: lubricant, kegel balls and pelvic floor trainers, dilator sets, menstrual cups and toy cleaner from LELO, CalExotics and more. Discreet UK delivery.",
       intro=["Lubricant, kegel balls and smart pelvic floor trainers, dilator sets, menstrual cups and toy cleaner from LELO, CalExotics, Satisfyer and more.",
              "Self-care, softly spoken, and sent discreetly from Rotherham, South Yorkshire."]),
  dict(slug="gifts", subs=["gifts"], name="Gifts & Calendars",
       title="Adult Gifts & Advent Calendars UK | Couples Gift Sets | Love and Beauty",
       h1="GIFTS & ADVENT CALENDARS",
       desc="Shop {n} adult gifts: 2026 adult advent calendars with Womanizer and We-Vibe, couples gift sets and starter kits. Discreet UK delivery.",
       intro=["Adult advent calendars, couples gift sets, starter kits and novelty gifts, perfect for birthdays, anniversaries and Christmas.",
              "Sent in plain packaging from Rotherham, South Yorkshire."]),
  dict(slug="beauty", subs=["beauty","lube"], name="Beauty & Self-Care", img="beauty.jpg",
       pick=r"lamai|beauty|face|skin|kegel|pelvic|dilator|menstrual|geisha|love balls|ben wa|luna",
       drop=r"vibrat|e-stim|electro|pleasure|thumping|motor|remote|krush",
       filters=[("Skincare & Face Cloths", r"lamai|beauty|face|skin"), ("Pelvic Floor & Intimate Health", r"kegel|pelvic|dilator|menstrual|geisha|love balls|ben wa|luna")],
       title="Beauty & Self-Care | Face Cloths, Skincare & Pelvic Floor Trainers | Love and Beauty",
       h1="BEAUTY & SELF-CARE",
       desc="Shop beauty and self-care from Love and Beauty Limited: soft face cleansing cloths, compressed travel face towels, and pelvic floor and kegel trainers from LELO and more. Trade supply for beauty salons. UK delivery.",
       intro=["Little rituals, beautifully done. Soft, biodegradable face cleansing cloths and compressed travel towels from Lamai Beauty, alongside pelvic floor trainers and intimate health products from LELO, CalExotics and more.",
              "As well as customers at home, we supply beauty salons, and we're adding new skincare lines all the time."],
       extra=[("For beauty salons", "We supply salons with face cloths and treatment essentials at trade prices. Email sales@loveandbeautysales.co.uk with what you need and roughly how many, and we'll send you a quote."),
              ("Gentle on skin", "Our Lamai cloths are ultra soft, wet or dry, and biodegradable, made for everyday cleansing and make-up removal."),
              ("Pelvic floor health", "Kegel balls and pelvic floor trainers are designed to help you exercise and strengthen your pelvic floor. Body-safe silicone, sent discreetly.")]),
]
SUBNAME = {"vibes":"Vibrators & Massagers","realistic":"Realistic Toys & Dildos","anal":"Anal Play",
  "rings":"Cock Rings & Enhancers","him":"Toys for Him","lingerie":"Lingerie","bondage":"Bondage & Restraints",
  "clubwear":"Fetish & Clubwear","menswear":"Men's Underwear & Harnesses","lube":"Lubricants & Intimate Care",
  "gifts":"Gifts & Calendars","beauty":"Beauty"}
ADULT_PAGE = "/masturbators-and-dildos/"
SUBPAGE = {"vibes":"vibrators","anal":"anal-toys","rings":"cock-rings","him":"male-sex-toys"}
BRANDS = ["LELO","Satisfyer","CalExotics","Calextics","Rocks-Off","Doc Johnson","ToyJoy","Pipedream","Le Wand","Fleshlight","Tenga",
  "Hot Octopuss","b-Vibe","Womanizer","Magic Shiver","Rimba","Amorable","Cottelli","Leg Avenue","Abierta Fina","Le Desir","Noir Handmade",
  "Black Level","Svenjoyment","NEK","Rouge","Ouch!","Love to Love","Pretty Love","VIVE","Vive","Dream Toys","Dreamtoys","Xocoon","Shots",
  "Secret Kisses","NS Novelties","Nu Sensuelle","Pillow Talk","OhMiBod","Svakom","Kiiroo","Evolved","ElectraStim","Lovetoy","Dorcel",
  "Marc Dorcel","Strap-on-me","Sportsheets","Clone-A-Willy","Blush","Bad Kitty","Daring Intimates","Mapale","Taboom","Lamai","FemmeFunn",
  "Je Joue","Gvibe","INYA","B Swish","Nasstoys","Master Series","WhipSmart","Pumped","MaleEdge","Man Cage","ManCage","Zado","Avanza","IntoYou"]

e = lambda s: html.escape(str(s), quote=True)

def brand_of(t):
    for b in sorted(BRANDS, key=len, reverse=True):
        if t.lower().startswith(b.lower()+" ") or t.lower().startswith(b.lower()):
            return {"Calextics":"CalExotics","Vive":"VIVE","Dreamtoys":"Dream Toys","Amorable":"Amorable by Rimba","ManCage":"Man Cage"}.get(b,b)
    return None

def card(p):
    url = f"https://www.ebay.co.uk/itm/{p['i']}"
    img = f"https://i.ebayimg.com/images/g/{p['g']}/s-l500.jpg"
    return (f'<article class="card" data-price="{p["p"]}" data-t="{e(p["t"].lower())}">'
            f'<a class="img" href="{url}" target="_blank" rel="noopener" aria-label="{e(p["t"])} on eBay"><img src="{img}" alt="{e(p["t"])}" loading="lazy" width="500" height="500"></a>'
            f'<div class="body"><div class="cat">{e(SUBNAME[p["c"]])}</div><h4>{e(p["t"])}</h4>'
            f'<div class="foot"><span class="price gold">£{p["p"]:.2f}</span>'
            f'<a class="btn btn-gold buy" href="{url}" target="_blank" rel="noopener">Buy on eBay</a></div></div></article>')

def nav_links(active):
    items = [("sex-toys","All Sexual Wellness")] + [(SUBPAGE[s], SUBNAME[s]) for s in ["vibes","anal","rings","him"]]
    return items

def cat_footer():
    links = "".join(f'<a href="/{p["slug"]}/">{e(p["name"])}</a>' for p in PAGES)
    return (f'<div class="cat-links"><p class="eyebrow">Shop by category</p><div class="cat-links-row">{links}</div>'
            f'<p class="adult-link">Adults only: <a href="{ADULT_PAGE}">Male Masturbators &amp; Realistic Dildos (18+)</a></p></div>')

HEAD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Love and Beauty Limited">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{site}/images/welcome.jpg">
<meta name="theme-color" content="#07050a">
<link rel="icon" type="image/png" href="/images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Cormorant+Garamond:ital,wght@1,400;1,500&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
{jsonld}
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="star" viewBox="0 0 24 24"><path fill="currentColor" d="M12 0c.6 6.3 5.7 11.4 12 12-6.3.6-11.4 5.7-12 12-.6-6.3-5.7-11.4-12-12C6.3 11.4 11.4 6.3 12 0Z"/></symbol></svg>
<div id="age-gate" role="dialog" aria-modal="true" aria-labelledby="gate-title">
  <div class="gate">
    <img src="/images/logo.png" alt="Love and Beauty Limited logo">
    <p class="eyebrow">Welcome to Love and Beauty</p>
    <h2 id="gate-title" class="gold">Are you 18 or over?</h2>
    <p>Our shop includes adult wellness products. Please confirm your age to continue.</p>
    <div class="gate-actions"><button class="btn btn-gold" id="gate-enter">I'm 18 or over</button><a class="btn" href="https://www.google.co.uk">Leave</a></div>
    <small>Discreet, plain packaging on every order.</small>
  </div>
</div>
<header class="site">
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="Love and Beauty Limited, home"><img src="/images/logo-small.png" alt=""><span>LOVE AND BEAUTY<small>LIMITED</small></span></a>
    <nav class="links" aria-label="Main">
      <a href="/lingerie/">Lingerie</a>
      <a href="/beauty/">Beauty</a>
      <a href="/sex-toys/">Sexual Wellness</a>
      <a href="/home-parties/">Home Parties</a>
      <a href="/#story">Our Story</a>
      <a class="nav-shop" href="/shop/">Website Shop</a>
      <a class="nav-ebay" href="/ebay-shop/">eBay Shop</a>
    </nav>
    <a class="btn btn-gold" href="/shop/">Shop Now</a>
  </div>
</header>
"""

FOOT = """
<footer>
  <div class="wrap">
    {catlinks}
    <img src="/images/logo-small.png" alt="">
    <div class="name gold">LOVE AND BEAUTY LIMITED</div>
    <div class="star-rule"><svg><use href="#star"/></svg></div>
    <div class="flinks"><a href="/">Home</a><a href="/home-parties/">Home Parties</a><a href="/#story">Our Story</a><a href="/#find-us">Find Us</a><a href="/#contact">Contact</a><a href="/shop/">Website Shop</a><a href="/ebay-shop/">eBay Shop</a></div>
    <p class="meta">Family-run in Rotherham, South Yorkshire · Discreet, plain packaging · Adult products are sold to over-18s only.<br>© {year} Love and Beauty Limited</p>
  </div>
</footer>
<script>
(function(){
  var gate=document.getElementById('age-gate');
  try{ if(localStorage.getItem('lb_age_ok')==='1') gate.hidden=true; }catch(e){}
  document.getElementById('gate-enter').addEventListener('click',function(){gate.hidden=true;try{localStorage.setItem('lb_age_ok','1');}catch(e){}});
  var grid=document.getElementById('grid'); if(!grid) return;
  var cards=[].slice.call(grid.children), q=document.getElementById('search'), s=document.getElementById('sort'), c=document.getElementById('count');
  var rx=null, types=document.getElementById('types');
  if(types) types.addEventListener('click',function(ev){
    var b=ev.target.closest('button'); if(!b) return;
    [].forEach.call(types.children,function(x){x.setAttribute('aria-pressed',x===b);});
    rx=b.dataset.rx?new RegExp(b.dataset.rx,'i'):null; apply();
  });
  function apply(){
    var t=(q.value||'').toLowerCase().trim(), shown=0;
    var list=cards.slice();
    if(s.value==='low') list.sort(function(a,b){return a.dataset.price-b.dataset.price;});
    if(s.value==='high') list.sort(function(a,b){return b.dataset.price-a.dataset.price;});
    list.forEach(function(el){ var ok=(!t||el.dataset.t.indexOf(t)>-1)&&(!rx||rx.test(el.dataset.t)); el.hidden=!ok; if(ok) shown++; grid.appendChild(el); });
    c.textContent=shown+(shown===1?' product':' products');
    document.getElementById('empty').hidden=shown>0;
  }
  q.addEventListener('input',apply); s.addEventListener('change',apply);
})();
</script>
</body>
</html>
"""

def jsonld(page, items, canon):
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"}]
    if page["slug"] != "sex-toys" and set(page["subs"]) <= {"vibes","anal","rings","him"}:
        crumbs.append({"@type":"ListItem","position":2,"name":"Sexual Wellness","item":SITE+"/sex-toys/"})
    crumbs.append({"@type":"ListItem","position":len(crumbs)+1,"name":page["name"],"item":canon})
    products = []
    for n, p in enumerate(items, 1):
        prod = {"@type":"Product","name":p["t"],"image":f"https://i.ebayimg.com/images/g/{p['g']}/s-l500.jpg",
                "url":f"https://www.ebay.co.uk/itm/{p['i']}",
                "offers":{"@type":"Offer","price":f"{p['p']:.2f}","priceCurrency":"GBP",
                          "availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition",
                          "url":f"https://www.ebay.co.uk/itm/{p['i']}"}}
        b = brand_of(p["t"])
        if b: prod["brand"] = {"@type":"Brand","name":b}
        products.append({"@type":"ListItem","position":n,"item":prod})
    data = [
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":crumbs},
      {"@context":"https://schema.org","@type":"CollectionPage","name":page["name"],"url":canon,"description":page["desc"].format(n=len(items)),
       "mainEntity":{"@type":"ItemList","numberOfItems":len(items),"itemListElement":products}},
    ]
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</","<\\/") + '</script>'

# featured order: mix sub-categories so pages with several types open with variety
def ordered(subs):
    buckets = {s:[p for p in PRODUCTS if p["c"]==s] for s in subs}
    out = []
    while any(buckets.values()):
        for s in subs:
            if buckets[s]: out.append(buckets[s].pop(0))
    return out

year = datetime.date.today().year
for page in PAGES:
    items = ordered(page.get("order") or page["subs"])
    if page.get("pick"):
        items = [p for p in items if re.search(page["pick"], p["t"], re.I)]
        items.sort(key=lambda p: p["c"] != "beauty")   # skincare first
    if page.get("drop"):
        items = [p for p in items if not re.search(page["drop"], p["t"], re.I)]
    if not items: continue
    canon = f"{SITE}/{page['slug']}/"
    desc = page["desc"].format(n=len(items))
    head = HEAD.format(title=e(page["title"]), desc=e(desc), canon=canon, site=SITE, ebay=EBAY_SHOP, jsonld=jsonld(page, items, canon))
    crumb = '<a href="/">Home</a>'
    if page["slug"] != "sex-toys" and set(page["subs"]) <= {"vibes","anal","rings","him"}:
        crumb += ' <span>›</span> <a href="/sex-toys/">Sexual Wellness</a>'
    crumb += f' <span>›</span> {e(page["name"])}'
    subnav = ""
    if page["slug"] == "sex-toys" or page["subs"][0] in SUBPAGE:
        subnav = '<div class="chips static-chips">' + "".join(
            f'<a class="chip" href="/{slug}/" aria-pressed="{"true" if slug==page["slug"] else "false"}">{e(nm)}</a>'
            for slug, nm in nav_links(page["slug"])) + '</div>'
    if page.get("filters"):
        fl = [(lab, rx, sum(1 for p in items if re.search(rx, p["t"], re.I))) for lab, rx in page["filters"]]
        subnav += ('<div class="chips type-chips" id="types"><button type="button" class="chip" aria-pressed="true" data-rx="">All <b>'
                   + str(len(items)) + '</b></button>' + "".join(
                   f'<button type="button" class="chip" aria-pressed="false" data-rx="{e(rx)}">{e(lab)} <b>{n}</b></button>'
                   for lab, rx, n in fl if n) + '</div>')
    if page["slug"] == "sex-toys":
        subnav += (f'<p class="adult-note">Looking for male masturbators or realistic dildos? They are in our separate '
                   f'<a class="gold" href="{ADULT_PAGE}">adults-only section (18+)</a>.</p>')
    intro = "".join(f"<p>{e(t)}</p>" for t in page["intro"])
    extra = ""
    if page.get("extra"):
        extra = '<div class="cat-extra">' + "".join(f'<div class="cat-extra-item"><h3 class="gold">{e(h)}</h3><p>{e(t)}</p></div>' for h, t in page["extra"]) + '</div>'
    if page.get("img"):
        hero_cls = "cat-hero cat-hero-split"
        hero_img = f'<img class="cat-hero-img" src="/images/{page["img"]}" alt="{e(page["name"])} collection, Love and Beauty" width="1080" height="1350">'
    else:
        hero_cls, hero_img = "cat-hero", ""
    body = f"""
<main>
<section class="{hero_cls}">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{crumb}</nav>
    <div class="cat-hero-grid">
      <div>
        <p class="eyebrow">Love and Beauty · {e(page['name'])}</p>
        <h1 class="gold">{e(page['h1'])}</h1>
        <div class="star-rule"><svg><use href="#star"/></svg></div>
        <div class="cat-intro">{intro}</div>
      </div>
      {hero_img}
    </div>
    {extra}
  </div>
</section>
<section class="shop cat-shop">
  <div class="wrap">
    {subnav}
    <div class="tools">
      <div><h2 class="gold cat-h2">{e(page['name'])}</h2><div class="count" id="count">{len(items)} products</div></div>
      <div class="tools-right">
        <input class="field-dark" id="search" type="search" placeholder="Search {e(page['name'].lower())}…" aria-label="Search">
        <select class="field-dark" id="sort" aria-label="Sort"><option value="featured">Featured</option><option value="low">Price: low to high</option><option value="high">Price: high to low</option></select>
      </div>
    </div>
    <div class="grid" id="grid">{''.join(card(p) for p in items)}</div>
    <p class="empty" id="empty" hidden>Nothing matches that search.</p>
    <p class="shop-note">Prices as listed on eBay (updated {e(UPDATED)}). Tap <em>Buy on eBay</em> to check out securely through our eBay shop. Every order is sent in plain, discreet packaging.</p>
  </div>
</section>
</main>"""
    out = head + body + FOOT.replace('{catlinks}',cat_footer()).replace('{ebay}',EBAY_SHOP).replace('{year}',str(year))
    os.makedirs(os.path.join(ROOT, page["slug"]), exist_ok=True)
    open(os.path.join(ROOT, page["slug"], "index.html"), "w", encoding="utf-8").write(out)
    print(f"/{page['slug']}/  {len(items)} products")

# ---------------------------------------------------------------------------
# Two whole-shop pages:
#   /shop/       Website Shop - every eBay listing, 15% off, pay by PayPal or order by email
#   /ebay-shop/  eBay Shop    - every eBay listing at eBay price, buy on eBay
# ---------------------------------------------------------------------------
DISCOUNT = 0.15
NO_DISCOUNT = ["lamai"]          # sold at eBay price (they lose money if discounted)
EX = json.load(open(os.path.join(ROOT, "exclusives.json"), encoding="utf-8"))
SETTINGS = EX.get("settings", {})
PAYPALME = re.sub(r"^https?://(www\.)?(paypal\.me|paypal\.com/paypalme)/", "", SETTINGS.get("paypalme","").strip(), flags=re.I).split("/")[0].lstrip("@")
ORDER_EMAIL = SETTINGS.get("email") or "sales@loveandbeautysales.co.uk"
DELIVERY = SETTINGS.get("delivery") or "Free UK delivery, in plain, discreet packaging."
SHOP_ORDER = ["lingerie","beauty","vibes","anal","rings","him","clubwear","menswear","bondage","lube","gifts"]

def site_price(p):
    if any(w in p["t"].lower() for w in NO_DISCOUNT): return p["p"]
    return round(p["p"] * (1 - DISCOUNT) + 1e-9, 2)

def shop_card(p, direct):
    img = f"https://i.ebayimg.com/images/g/{p['g']}/s-l500.jpg"
    ebay = f"https://www.ebay.co.uk/itm/{p['i']}"
    if direct:
        sp = site_price(p); off = sp < p["p"]
        pr = (f'<span class="price gold">£{sp:.2f}</span>' + (f'<s class="was">£{p["p"]:.2f}</s>' if off else ''))
        return (f'<article class="card" id="p{p["i"]}" data-id="{p["i"]}" data-price="{sp}" data-was="{p["p"]}" data-c="{p["c"]}" data-t="{e(p["t"].lower())}" data-title="{e(p["t"])}" data-img="{img}">'
                f'<a class="img ws-open" href="#p{p["i"]}"><img src="{img}" alt="{e(p["t"])}" loading="lazy" width="500" height="500">'
                + ('<span class="ws-badge">15% OFF</span>' if off else '') + '</a>'
                f'<div class="body"><div class="cat">{e(SUBNAME[p["c"]])}</div><h4>{e(p["t"])}</h4>'
                f'<div class="foot"><span class="ws-prices">{pr}</span><a class="btn btn-gold buy ws-open" href="#p{p["i"]}">Buy now</a></div></div></article>')
    return (f'<article class="card" data-price="{p["p"]}" data-c="{p["c"]}" data-t="{e(p["t"].lower())}">'
            f'<a class="img" href="{ebay}" target="_blank" rel="noopener"><img src="{img}" alt="{e(p["t"])}" loading="lazy" width="500" height="500"></a>'
            f'<div class="body"><div class="cat">{e(SUBNAME[p["c"]])}</div><h4>{e(p["t"])}</h4>'
            f'<div class="foot"><span class="price gold">£{p["p"]:.2f}</span><a class="btn btn-gold buy" href="{ebay}" target="_blank" rel="noopener">Buy on eBay</a></div></div></article>')

SHOP_JS = """
<script>
(function(){
  var gate=document.getElementById('age-gate');
  try{ if(localStorage.getItem('lb_age_ok')==='1') gate.hidden=true; }catch(e){}
  document.getElementById('gate-enter').addEventListener('click',function(){gate.hidden=true;try{localStorage.setItem('lb_age_ok','1');}catch(e){}});
  var $=function(id){return document.getElementById(id);};
  var grid=$('grid'), cards=[].slice.call(grid.children), q=$('search'), s=$('sort'), cat=$('catsel');
  function apply(){
    var t=(q.value||'').toLowerCase().trim(), c=cat.value, shown=0, list=cards.slice();
    if(s.value==='low') list.sort(function(a,b){return a.dataset.price-b.dataset.price;});
    if(s.value==='high') list.sort(function(a,b){return b.dataset.price-a.dataset.price;});
    list.forEach(function(el){ var ok=(!t||el.dataset.t.indexOf(t)>-1)&&(!c||el.dataset.c===c); el.hidden=!ok; if(ok) shown++; grid.appendChild(el); });
    $('count').textContent=shown+(shown===1?' product':' products');
    $('empty').hidden=shown>0;
  }
  q.addEventListener('input',apply); s.addEventListener('change',apply); cat.addEventListener('change',apply);
  var modal=$('modal'); if(!modal) return;
  var PP=modal.dataset.paypal, EM=modal.dataset.email;
  function money(v){return '\\u00a3'+Number(v).toFixed(2);}
  function open(card){
    var d=card.dataset, price=Number(d.price), was=Number(d.was), title=d.title;
    $('m-img').src=d.img.replace('s-l500','s-l1600'); $('m-img').alt=title;
    $('m-title').textContent=title;
    $('m-cat').textContent=card.querySelector('.cat').textContent;
    $('m-price').innerHTML=money(price)+(price<was?' <s class="was">'+money(was)+'</s> <span class="ws-save">Save '+money(was-price)+'</span>':'');
    $('m-paypal').href='https://www.paypal.com/paypalme/'+encodeURIComponent(PP)+'/'+price.toFixed(2)+'GBP';
    var body='Hello, I would like to order:\\n\\n'+title+' ('+money(price)+')\\nRef: '+d.id+'\\nSize / colour (if any):\\n\\nMy name:\\nDelivery address:\\nPhone (optional):\\n\\nI confirm I am 18 or over.';
    $('m-email').href='mailto:'+EM+'?subject='+encodeURIComponent('Website order: '+title)+'&body='+encodeURIComponent(body);
    $('m-ebay').href='https://www.ebay.co.uk/itm/'+d.id;
    $('m-ref').textContent=d.id;
    $('m-price2').textContent=money(price);
    modal.hidden=false; document.body.style.overflow='hidden';
    try{history.replaceState(null,'','#p'+d.id);}catch(e){}
  }
  function close(){ modal.hidden=true; document.body.style.overflow=''; try{history.replaceState(null,'',location.pathname);}catch(e){} }
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('.ws-open'); if(a){ e.preventDefault(); open(a.closest('.card')); return; }
    if(e.target===modal) close();
  });
  $('m-close').addEventListener('click',close);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!modal.hidden) close(); });
  var h=location.hash.slice(1); if(h){ var c=document.getElementById(h); if(c) open(c); }
})();
</script>
</body>
</html>
"""

def build_shop(direct):
    items = [p for s in SHOP_ORDER for p in PRODUCTS if p["c"] == s]
    slug = "shop" if direct else "ebay-shop"
    canon = f"{SITE}/{slug}/"
    if direct:
        name, h1 = "Website Shop", "WEBSITE SHOP"
        title = "Shop Direct – 15% Off Every eBay Price | Love and Beauty"
        desc = f"Buy direct from Love and Beauty and save 15% on our eBay prices across {len(items)} lingerie, beauty and sexual wellness products. Pay by PayPal or order by email. Free discreet UK delivery."
        intro = [f"Every product from our eBay shop, sold direct from our family-run business in Rotherham, South Yorkshire, and <b>15% cheaper than our eBay prices</b>.",
                 "Pay securely with PayPal, or send us an order by email and we'll reply with how to pay. " + e(DELIVERY)]
        note = f"Prices are 15% below our eBay prices (updated {e(UPDATED)}). Stock is shared with our eBay shop, so if an item has just sold out we'll let you know and refund you in full straight away. Adults 18+ only."
    else:
        name, h1 = "eBay Shop", "EBAY SHOP"
        title = "Our eBay Shop – Lingerie, Beauty & Sexual Wellness | Love and Beauty"
        desc = f"Browse all {len(items)} products in the Love and Beauty eBay shop (loveandbeautyltd) and check out securely on eBay. Discreet UK delivery."
        intro = ["Our full eBay shop (<b>loveandbeautyltd</b>) in one place. Tap <em>Buy on eBay</em> to check out securely with eBay's buyer protection.",
                 'Want to save 15%? The same products are cheaper when you buy direct in our <a class="gold" href="/shop/">Website Shop</a>.']
        note = f'Prices as listed on eBay (updated {e(UPDATED)}). <a class="gold" href="{EBAY_SHOP}" target="_blank" rel="noopener">Open our eBay shop</a>. Every order is sent in plain, discreet packaging.'
    jl = json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":name,"url":canon,"description":desc}, ensure_ascii=False)
    head = HEAD.format(title=e(title), desc=e(desc), canon=canon, site=SITE, ebay=EBAY_SHOP,
                       jsonld=f'<script type="application/ld+json">{jl}</script>')
    opts = '<option value="">All categories</option>' + "".join(
        f'<option value="{s}">{e(SUBNAME[s])} ({sum(1 for p in items if p["c"]==s)})</option>' for s in SHOP_ORDER if any(p["c"]==s for p in items))
    switch = ('<div class="chips static-chips">'
              f'<a class="chip" href="/shop/" aria-pressed="{"true" if direct else "false"}">Website Shop · 15% off</a>'
              f'<a class="chip" href="/ebay-shop/" aria-pressed="{"false" if direct else "true"}">eBay Shop</a></div>')
    body = f"""
<main>
<section class="cat-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span>›</span> {name}</nav>
    <p class="eyebrow">Love and Beauty · {"Buy direct and save 15%" if direct else "Buy on eBay"}</p>
    <h1 class="gold">{h1}</h1>
    <div class="star-rule"><svg><use href="#star"/></svg></div>
    <div class="cat-intro">{"".join(f"<p>{t}</p>" for t in intro)}</div>
  </div>
</section>
<section class="shop cat-shop">
  <div class="wrap">
    {switch}
    <div class="tools">
      <div><h2 class="gold cat-h2">{name}</h2><div class="count" id="count">{len(items)} products</div></div>
      <div class="tools-right">
        <input class="field-dark" id="search" type="search" placeholder="Search {len(items)} products…" aria-label="Search">
        <select class="field-dark" id="catsel" aria-label="Category">{opts}</select>
        <select class="field-dark" id="sort" aria-label="Sort"><option value="featured">Featured</option><option value="low">Price: low to high</option><option value="high">Price: high to low</option></select>
      </div>
    </div>
    <div class="grid" id="grid">{''.join(shop_card(p, direct) for p in items)}</div>
    <p class="empty" id="empty" hidden>Nothing matches that search.</p>
    <p class="shop-note">{note}</p>
  </div>
</section>
</main>"""
    if direct:
        body += f"""
<div class="ex-modal" id="modal" hidden role="dialog" aria-modal="true" aria-labelledby="m-title" data-paypal="{e(PAYPALME)}" data-email="{e(ORDER_EMAIL)}">
  <div class="ex-dialog">
    <button class="ex-close" id="m-close" aria-label="Close">×</button>
    <div class="ex-dialog-grid">
      <div><div class="ex-main-img"><img id="m-img" alt=""></div></div>
      <div>
        <p class="eyebrow" id="m-cat"></p>
        <h2 class="gold" id="m-title"></h2>
        <div class="ex-price gold" id="m-price"></div>
        <p class="ex-stock">{e(DELIVERY)}</p>
        <div class="ex-buy">
          <a class="btn btn-gold" id="m-paypal" target="_blank" rel="noopener">Pay with PayPal</a>
          <a class="btn" id="m-email">Order by email</a>
        </div>
        <ol class="ex-howto">
          <li>Tap <b>Pay with PayPal</b>. The price (<span id="m-price2"></span>) is filled in for you.</li>
          <li>In the PayPal note, write the product name or ref <b id="m-ref"></b>, any size or colour, and your delivery address.</li>
          <li>We'll email you to confirm and send your order discreetly.</li>
          <li>Prefer not to use PayPal? Tap <b>Order by email</b> and we'll reply with other ways to pay.</li>
        </ol>
        <p class="ws-more"><a class="gold" id="m-ebay" target="_blank" rel="noopener">See full description and photos on eBay</a></p>
      </div>
    </div>
  </div>
</div>"""
    foot = FOOT.split("<script>")[0].replace('{catlinks}', cat_footer()).replace('{ebay}', EBAY_SHOP).replace('{year}', str(year))
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    open(os.path.join(ROOT, slug, "index.html"), "w", encoding="utf-8").write(head + body + foot + SHOP_JS)
    print(f"/{slug}/  {len(items)} products")

build_shop(True)
build_shop(False)

# /dildos/ moved into the 18+ section: leave a small page that forwards there
os.makedirs(os.path.join(ROOT, "dildos"), exist_ok=True)
open(os.path.join(ROOT, "dildos", "index.html"), "w", encoding="utf-8").write(
    f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Realistic Dildos | Love and Beauty</title>'
    f'<meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{ADULT_PAGE}">'
    f'<meta http-equiv="refresh" content="0; url={ADULT_PAGE}#dildos"></head><body>'
    f'<p>Realistic toys and dildos have moved to our <a href="{ADULT_PAGE}#dildos">adults-only section (18+)</a>.</p></body></html>')
print("/dildos/  -> forwards to", ADULT_PAGE)

# eBay explicit items go onto the 18+ page, between the ADULT-EBAY markers
ap = os.path.join(ROOT, ADULT_PAGE.strip("/"), "index.html")
ah = open(ap, encoding="utf-8").read()
mast = [p for p in ADULT if p["c"] == "him"]
dild = [p for p in ADULT if p["c"] == "realistic"]
def adult_block(hid, title, items):
    if not items: return ""
    return (f'<div class="adult-group" id="{hid}"><div class="tools"><div><h2 class="gold cat-h2">{e(title)}</h2>'
            f'<div class="count">{len(items)} products · buy on eBay</div></div></div>'
            f'<div class="grid">{"".join(card(p) for p in items)}</div></div>')
block = ("<!--ADULT-EBAY-START-->" + adult_block("masturbators", "Male Masturbators & Strokers", mast)
         + adult_block("dildos", "Realistic Toys & Dildos", dild) + "<!--ADULT-EBAY-END-->")
ah, n = re.subn(r"<!--ADULT-EBAY-START-->.*?<!--ADULT-EBAY-END-->", lambda m: block, ah, flags=re.S)
assert n == 1, "ADULT-EBAY markers missing from " + ap
open(ap, "w", encoding="utf-8").write(ah)
print(f"{ADULT_PAGE}  {len(mast)} masturbators + {len(dild)} dildos from eBay")

# hand-made pages share the same footer category links
for hp in ["index.html", "home-parties/index.html", "masturbators-and-dildos/index.html"]:
    fp = os.path.join(ROOT, hp); t = open(fp, encoding="utf-8").read()
    t, n = re.subn(r"<!--CATLINKS-START-->.*?<!--CATLINKS-END-->", lambda m: "<!--CATLINKS-START-->" + cat_footer() + "<!--CATLINKS-END-->", t, flags=re.S)
    if n: open(fp, "w", encoding="utf-8").write(t)

# sitemap + robots
today = datetime.date.today().isoformat()
urls = [SITE+"/", SITE+"/shop/", SITE+"/ebay-shop/", SITE+"/home-parties/"]   # 18+ page is noindex, so not listed + [f"{SITE}/{p['slug']}/" for p in PAGES]  # /dildos/ now forwards to the 18+ page
# brand images listed for the homepage so Google can show them under the result
HOME_IMAGES = ["ig-welcome","ig-lingerie","ig-new-in","ig-link-in-bio","ig-shop-with-us"]
def img_tags(u):
    if u != SITE+"/": return ""
    return "".join(f"<image:image><image:loc>{SITE}/images/{n}.jpg</image:loc></image:image>" for n in HOME_IMAGES)
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + \
     "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>{img_tags(u)}</url>\n" for u in urls) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {SITE}/sitemap.xml\n")
print("sitemap.xml + robots.txt written")

