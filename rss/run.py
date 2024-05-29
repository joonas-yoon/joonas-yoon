import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

LIST_SIZE = 5
RSS_URL = 'https://blog.joonas.io/rss'
INJECT_FILE = 'README.md'
STARTING_FLAG = '<!-- feed start -->'
ENDING_FLAG = '<!-- feed end -->'

# get xml from given rss url
res = requests.get(RSS_URL)
root = ET.fromstring(res.text)
channel = root.find('channel')
items = channel.findall('item')
items_output = []
for item in items[:LIST_SIZE]:
    title = item.find('title').text
    link = item.find('link').text
    pub_date = item.find('pubDate').text
    date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
    ymd = datetime.strftime(date, '%Y/%m/%d')
    markdown = f"* {ymd} - [{title}]({link})"
    items_output.append(markdown)

content = "\n".join(items_output)

# read file and find flag to replace content
with open(INJECT_FILE, 'r', encoding='utf-8') as f:
    readme = ''.join(f.readlines())
    try:
        start_index = readme.index(STARTING_FLAG)
    except ValueError:
        print("Failed to find starting flag to replace", file=sys.stderr)
    try:
        end_index = readme.index(ENDING_FLAG)
    except ValueError:
        print("Failed to find ending flag to replace", file=sys.stderr)

    precontent = readme[:start_index]
    postcontent = readme[end_index+len(ENDING_FLAG):]

    output = f"{precontent}{STARTING_FLAG}\n{content}\n{ENDING_FLAG}{postcontent}"

# overwrite target file
with open(INJECT_FILE, 'w', encoding='utf-8') as f:
    f.write(output)
