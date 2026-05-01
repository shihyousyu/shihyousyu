import os
import requests
import re

README = "README.md"
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"
API_KEY = os.environ.get("WAKATIME_API_KEY", "")

# 這是我 wakatime 壞掉遺失的時數，我沒作弊
DELTA = {
    "languages": {
        "C++":      597 * 60,
        "Java":     650 * 60,
        "Markdown": 383 * 60,
        "Python":   379 * 60,
        "Dart":      82 * 60,
        "HTML":      49 * 60,
        "C":        126 * 60,
        "Other":     54 * 60,
        "Assembly": 113 * 60,
        "Vue.js":    55 * 60,
        "Bash":      40 * 60,
        "Go":        31 * 60,
        "Text":      13 * 60,
        "CSS":        6 * 60,
        "YAML":      14 * 60,
    },
    "operating_systems": {
        "Windows": 1688 * 60,
        "Mac":      599 * 60,
        "Linux":    279 * 60,
    },
}

r = requests.get(
    "https://api.wakatime.com/api/v1/users/current/stats/all_time",
    params={"api_key": API_KEY}
)
res = r.json()["data"]

def parse(text):
    h = m = s = 0
    match_h = re.search(r'(\d+)\s*hr', text)
    if match_h:
        h = int(match_h.group(1))
    match_m = re.search(r'(\d+)\s*min', text)
    if match_m:
        m = int(match_m.group(1))
    match_s = re.search(r'(\d+)\s*sec', text)
    if match_s:
        s = int(match_s.group(1))
    return h*60 + m + s/60  # 分鐘


def toHour(total_minutes):
    h = int(total_minutes // 60)
    m = int(total_minutes % 60)
    return f"{h} hrs {m} mins"


def apply_delta(items, delta_map):
    if not delta_map:
        return items

    # 補時數
    existing = {i["name"] for i in items}
    for item in items:
        if item["name"] in delta_map:
            item["total_seconds"] += delta_map[item["name"]]

    for name, secs in delta_map.items():
        if name not in existing:
            items.append({"name": name, "total_seconds": secs, "percent": 0})

    new_total = sum(i["total_seconds"] for i in items)
    for item in items:
        item["percent"] = round(item["total_seconds"] / new_total * 100, 2) if new_total else 0
        item["text"] = toHour(item["total_seconds"] / 60)

    items.sort(key=lambda x: x["total_seconds"], reverse=True)
    return items


res["languages"] = apply_delta(res["languages"], DELTA["languages"])
res["operating_systems"] = apply_delta(res["operating_systems"], DELTA["operating_systems"])

total_minutes = sum(i["total_seconds"] for i in res["languages"]) / 60
s = toHour(total_minutes)


l = ["<details>", f"<summary><h2>WakaTime：{s}</h2></summary>"]
l.append("<h3>Language</h3>")
for i in res['languages']:
    name = i['name']
    time = i['text']
    percent = i['percent']
    l.append("█" * (int(percent) // 2) + "░" * (50 - int(percent) // 2) + "    " + f"- {name}: {time} ({percent:.1f}%)  ")

l.append("<h3>Operating system</h3>")
for i in res['operating_systems']:
    name = i['name']
    time = i['text']
    percent = i['percent']
    l.append("█" * (int(percent) // 2) + "░" * (50 - int(percent) // 2) + "    " + f"- {name}: {time} ({percent:.1f}%)  ")
l.append("</details>")

s = "\n".join(l)

with open(README, "r", encoding="utf-8") as f:
    old = f.read()

start = old.find(START)
end = old.find(END)

new = old[:start + len(START)] + "\n" + s + "\n" + old[end:]
with open(README, "w", encoding="utf-8") as f:
    f.write(new)
