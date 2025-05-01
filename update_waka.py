import requests

README = "README.md"
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"

url = f"https://wakatime.com/api/v1/users/Syu/stats"
res = requests.get(url).json()["data"]

l = [f"## WakaTime：{res['categories'][0]['text']}"]
l.append("### Language：")
for i in res['languages'][:5]:
    name = i['name']
    time = i['text']
    percent = i['percent']
    l.append(f"- {name}: {time} ({percent:.1f}%)")
    l.append("#" * int(percent) + "-" * (100 - int(percent)))
s = "\n".join(l)

with open(README, "r", encoding="utf-8") as f:
    old = f.read()

start = old.find(START)
end = old.find(END)

new = old[:start + len(START)] + "\n" + s + "\n" + old[end:]
with open(README, "w", encoding="utf-8") as f:
    f.write(new)
