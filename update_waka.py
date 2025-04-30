import requests
import os

README = "README.md"
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"

def fetch(username):
    api_url = f"https://{'wakatime.com'}/api/v1/users/{username}/stats"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch WakaTime stats.")
    return response.json()["data"]

def format(data):
    l = []
    l.append("## Language：")
    for i in data['languages'][:5]:
        name = i['name']
        time = i['text']
        percent = i['percent']
        l.append(f"- {name}: {time} ({percent:.1f}%)")
    return "\n".join(l)

def update(content):
    with open(README, "r", encoding="utf-8") as f:
        old = f.read()

    start = old.find(START)
    end = old.find(END)

    new = old[:start + len(START)] + "\n" + content + "\n" + old[end:]
    with open(README, "w", encoding="utf-8") as f:
        f.write(new)

def main():
    data = fetch("Syu")
    result = format(data)
    print(result)
    update(result)

if __name__ == "__main__":
    main()
