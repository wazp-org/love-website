# love-website

Website for Love and Beauty Limited — https://www.loveandbeautysales.co.uk

- `index.html` — homepage (Sex Toys feature, shop, story, find us, contact)
- `products.js` — product list taken from the eBay shop (loveandbeautyltd)
- `tools/build_pages.py` — builds the category pages (`/sex-toys/`, `/vibrators/` …), `sitemap.xml` and `robots.txt` from `products.js`

After refreshing `products.js`, run `python3 tools/build_pages.py` and commit everything.
