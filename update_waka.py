import requests

README = "README.md"
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"

url = f"https://wakatime.com/api/v1/users/Syu/stats"
res = requests.get(url).json()["data"]

l = [f"## WakaTime：{res['categories'][0]['text']}"]
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
