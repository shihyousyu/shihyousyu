import requests
import re

README = "README.md"
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"

url = f"https://wakatime.com/api/v1/users/Syu/stats"
res = requests.get(url).json()["data"]

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

l = [f"## WakaTime：{toHour(sum(parse(res["data"]["categories"][i]["text") for i in range(len(res["data"]["categories"]))))}"]
l.append("### Language：  ")
l.append("```  ")
for i in res['languages']:
    name = i['name']
    time = i['text']
    percent = i['percent']
    l.append("█" * (int(percent) // 2) + "░" * (50 - int(percent) // 2) + "    " + f"- {name}: {time} ({percent:.1f}%)  ")
l.append("```  ")

l.append("### Operating Systems：  ")
l.append("```  ")
for i in res['operating_systems']:
    name = i['name']
    time = i['text']
    percent = i['percent']
    l.append("█" * (int(percent) // 2) + "░" * (50 - int(percent) // 2) + "    " + f"- {name}: {time} ({percent:.1f}%)  ")
l.append("```  ")

s = "\n".join(l)

with open(README, "r", encoding="utf-8") as f:
    old = f.read()

start = old.find(START)
end = old.find(END)

new = old[:start + len(START)] + "\n" + s + "\n" + old[end:]
with open(README, "w", encoding="utf-8") as f:
    f.write(new)
