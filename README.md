# love-website

Website for Love and Beauty Limited — https://www.loveandbeautysales.co.uk

- `index.html` — homepage (Sex Toys feature, shop, story, find us, contact)
- `products.js` — product list taken from the eBay shop (loveandbeautyltd)
- `tools/build_pages.py` — builds the category pages (`/sex-toys/`, `/vibrators/` …), `sitemap.xml` and `robots.txt` from `products.js`

After refreshing `products.js`, run `python3 tools/build_pages.py` and commit everything.

Site layout (Nov 2026): the homepage leads with three equal collections, Lingerie, Beauty and Sexual Wellness (/sex-toys/).
Male masturbators/strokers and all realistic toys & dildos are kept off the main site and shown only on the separate
18+ page /masturbators-and-dildos/ (its own age check every visit, noindex). The rule is ADULT_RE in tools/build_pages.py
and in index.html; build_pages.py fills the eBay part of that page between the ADULT-EBAY markers.
