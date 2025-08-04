Smart Ad Switcher 

A smart, location-aware ad switching system that dynamically selects which ad to display based on **area type** (e.g. downtown, park) and **weather conditions** (hot, mild, cold).

**How it Works**

- **Real-time input**: Simulates a route by slightly changing lat/lon values.
- **Scoring system**: Ads are matched based on the priority of location, then weather.
- **Image display**: Uses `Pillow` to show ad images like a digital billboard.

**Demo**

Run the following in your terminal:
```bash
python3 switcher.py --demo

**Rules**
Rules are defined in rules.json and scored for best match based on:
Location
Temperature


**Folder Structure**
Copy
Edit
smart_ad_switcher/
├── ads/
│   ├── downtown_bank.jpg
│   ├── park_energy.jpg
│   └── ...
├── rules.json
├── switcher.py
└── README.md
