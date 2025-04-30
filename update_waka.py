import requests
import os

README = "README.md"
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"

def fetch(key):
    url = "https://wakatime.com/api/v1/users/current/stats/last_7_days"
    headers = {"Authorization": f"Bearer {key}"}
    res = requests.get(url, headers = headers)
    return res.json()

def format_stats(data):
    lines = [f"🕒 累積時間：{data['data']['text']}"]
    lines.append("## 最常用語言：")
    for lang in data['data']['languages'][:5]:
        name = lang['name']
        time = lang['text']
        percent = lang['percent']
        lines.append(f"- {name}: {time} ({percent:.1f}%)")
    return "\n".join(lines)

def update_readme(content):
    with open(README, "r", encoding="utf-8") as f:
        old = f.read()

    start = old.find(START)
    end = old.find(END)

    if start == -1 or end == -1:
        print("README.md 裡面找不到指定區塊")
        return

    new = old[:start + len(START)] + "\n" + content + "\n" + old[end:]
    with open(README, "w", encoding="utf-8") as f:
        f.write(new)

def main():
    key = os.getenv("WAKATIME_API_KEY")
    data = fetch(key)
    formatted = format_stats(data)
    update_readme(formatted)

if __name__ == "__main__":
    main()
