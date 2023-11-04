import json
import os
import time

with open("../basic.json") as f:
    data = json.load(f)

for repo in data:
    os.system(f"git clone {repo['http_url_to_repo']} {repo['id']}")
    time.sleep(1)


