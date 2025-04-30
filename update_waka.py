import requests
import os

README = "README.md"
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"

api_url = f"https://{'wakatime.com'}/api/v1/users/Syu/stats"
response = requests.get(api_url).json()["data"]

l = [f"Coding Time：{response['categories'][0]['text']}"]
l.append("## Language：")
for i in response['languages'][:5]:
    name = i['name']
    time = i['text']
    percent = i['percent']
    l.append(f"- {name}: {time} ({percent:.1f}%)")
s = "\n".join(l)

with open(README, "r", encoding="utf-8") as f:
    old = f.read()

start = old.find(START)
end = old.find(END)

new = old[:start + len(START)] + "\n" + s + "\n" + old[end:]
with open(README, "w", encoding="utf-8") as f:
    f.write(new)

def main():
    data = fetch("Syu")
    result = format(data)
    #update(result)

if __name__ == "__main__":
    main()
