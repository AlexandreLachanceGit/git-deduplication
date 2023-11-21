import json
import os
import time

with open("../more.json") as f:
    data = json.load(f)

for repo in data:
    os.system(f"git clone {repo['html_url']} {repo['id']}")
    time.sleep(1)


