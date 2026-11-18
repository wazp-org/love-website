"""Brand names, shared by build_pages.py and build_shop.py."""
BRANDS = ["LELO","Satisfyer","CalExotics","Calextics","Rocks-Off","Doc Johnson","ToyJoy","Pipedream","Le Wand","Fleshlight","Tenga",
  "Hot Octopuss","b-Vibe","Womanizer","Magic Shiver","Rimba","Amorable","Cottelli","Leg Avenue","Abierta Fina","Le Desir","Noir Handmade",
  "Black Level","Svenjoyment","NEK","Rouge","Ouch!","Love to Love","Pretty Love","VIVE","Vive","Dream Toys","Dreamtoys","Xocoon","Shots",
  "Secret Kisses","NS Novelties","Nu Sensuelle","Pillow Talk","OhMiBod","Svakom","Kiiroo","Evolved","ElectraStim","Lovetoy","Dorcel",
  "Marc Dorcel","Strap-on-me","Sportsheets","Clone-A-Willy","Blush","Bad Kitty","Daring Intimates","Mapale","Taboom","Lamai","FemmeFunn",
  "Je Joue","Gvibe","INYA","B Swish","Nasstoys","Master Series","WhipSmart","Pumped","MaleEdge","Man Cage","ManCage","Zado","Avanza","IntoYou",
  "Obsessive","XR Brands","Inmi","Wand Essentials","Clean Stream","Fetish Collection","S-Line","Lubido","Mystim","CB-X","Genuine CB-3000","OVO","Linx",
  "Menzstuff","Adam & Eve","Loveline","She-E-O","Nexus","Magic Motion","Me You Us","MM Original","pjur","ID Free","ID Jelly","SKYN","Lovetoy"]


def brand_of(t):
    for b in sorted(BRANDS, key=len, reverse=True):
        if t.lower().startswith(b.lower()+" ") or t.lower().startswith(b.lower()):
            return {"Calextics":"CalExotics","Vive":"VIVE","Dreamtoys":"Dream Toys","Amorable":"Amorable by Rimba","ManCage":"Man Cage",
             "Marc Dorcel":"Dorcel","Inmi":"XR Brands","Wand Essentials":"XR Brands","Clean Stream":"XR Brands","Genuine CB-3000":"CB-X",
             "Rouge":"Rouge Garments","MM Original":"MM","ID Free":"ID Lubricants","ID Jelly":"ID Lubricants"}.get(b,b)
    return None

