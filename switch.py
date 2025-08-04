#!/usr/bin/env python3
"""
Smart Ad-Switcher demo for Movia
Author: <your name>  •  Date: 2025-08-03
Run: python switcher.py --demo      (simulated route)
     python switcher.py --lat 43.65 --lon -79.38   (single coord)
"""
import json, time, random, argparse, datetime
import pathlib, subprocess, sys, requests
from PIL import Image


ADS_DIR   = pathlib.Path(__file__).parent / "ads"
RULE_FILE = pathlib.Path(__file__).parent / "rules.json"

# ---------- helpers ----------------------------------------------------------
def get_weather(lat: float, lon: float) -> str:
    """Return 'hot' | 'mild' | 'cold' based on current temp (°C)."""
    url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={lat}&longitude={lon}&current_weather=true")
    try:
        temp = requests.get(url, timeout=5).json()["current_weather"]["temperature"]
    except Exception:
        temp = 15  # fallback
    if temp >= 25: return "hot"
    if temp <= 5:  return "cold"
    return "mild"

def classify_area(lat: float, lon: float) -> str:
    """Classify into 4 fake areas based on coordinates."""
    # Simple demo partitioning
    if lat > 43.66 and lon < -79.39:
        return "park"
    elif lat > 43.66 and lon >= -79.39:
        return "university"
    elif lat <= 43.66 and lon >= -79.39:
        return "downtown_financial"
    else:
        return "residential"


def load_rules():
    with open(RULE_FILE) as f:
        return json.load(f)

def select_ad(ctx: dict, rules: list) -> dict:
    """Score-based ad selection; prioritize location > hour > weather."""
    best_rule = None
    best_score = -1

    for rule in rules:
        score = 0
        if ctx["area"] in rule["area"]:
            score += 3  # Highest priority
        if rule["hour_range"][0] <= ctx["hour"] < rule["hour_range"][1]:
            score += 2
        if ctx["weather"] in rule["weather"]:
            score += 1

        if score > best_score:
            best_score = score
            best_rule = rule

    # If nothing matches, fall back
    return best_rule if best_rule else {"name": "Generic", "file": "generic_brand.jpg"}



def display(path: pathlib.Path):
    """Open image with Pillow; auto-closes old viewers on macOS/Win/Linux."""
    img = Image.open(path)
    img.show()                # opens default image viewer
    # optional: give OS a moment to launch viewer
    time.sleep(0.3)

# ---------- main loop --------------------------------------------------------
def run_demo():
    rules = load_rules()
    print("=== Starting simulated route (ctrl-c to quit) ===")
    lat, lon = 43.65, -79.38
    while True:
        # jitter position ±0.002°
        lat += random.uniform(-0.05, 0.05)
        lon += random.uniform(-0.05, 0.05)

        now      = datetime.datetime.now()
        weather  = get_weather(lat, lon)
        area     = classify_area(lat, lon)
        ctx      = {"weather": weather, "hour": now.hour, "area": area}
        ad       = select_ad(ctx, rules)

        print(f"{now:%H:%M:%S}  {weather:>4}  {area:<11}  →  {ad['name']}")
        display(ADS_DIR / ad["file"])
        time.sleep(10)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lon", type=float)
    ap.add_argument("--demo", action="store_true", default=False)
    opts = ap.parse_args()

    if opts.demo or (opts.lat is None and opts.lon is None):
        run_demo()
    else:
        # one-shot mode for scripted tests
        ctx = {
            "weather": get_weather(opts.lat, opts.lon),
            "hour": datetime.datetime.now().hour,
            "area": classify_area(opts.lat, opts.lon)
        }
        ad = select_ad(ctx, load_rules())
        print(json.dumps({"ctx": ctx, "ad": ad}, indent=2))
