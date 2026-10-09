"""Download the Noto fonts needed for Kannada / Tamil / Hindi / Telugu PDFs.
Run once:  python fetch_fonts.py
"""
import os, urllib.request

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl"
FONTS = {
    "NotoSansKannada-Regular.ttf": "notosanskannada/NotoSansKannada%5Bwdth,wght%5D.ttf",
    "NotoSansTamil-Regular.ttf": "notosanstamil/NotoSansTamil%5Bwdth,wght%5D.ttf",
    "NotoSansDevanagari-Regular.ttf": "notosansdevanagari/NotoSansDevanagari%5Bwdth,wght%5D.ttf",
    "NotoSansTelugu-Regular.ttf": "notosanstelugu/NotoSansTelugu%5Bwdth,wght%5D.ttf",
    "NotoSans-Regular.ttf": "notosans/NotoSans%5Bwdth,wght%5D.ttf",
}

os.makedirs("fonts", exist_ok=True)
for name, path in FONTS.items():
    dest = os.path.join("fonts", name)
    if os.path.exists(dest) and os.path.getsize(dest) > 50000:
        print("already present:", name)
        continue
    print("downloading", name, "...")
    urllib.request.urlretrieve(f"{BASE}/{path}", dest)
    print("  saved", os.path.getsize(dest), "bytes")
print("Done. Fonts are in ./fonts")
