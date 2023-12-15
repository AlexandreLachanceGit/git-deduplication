import json
import os

with (open("./gitlab.json") as f):
    repos_json = json.load(f)

id_set = set()
for repo in repos_json:
    id_set.add(repo['id'])

missing = []
for repo in repos_json:
    if repo['parent_id'] != None and not repo['parent_id'] in id_set and not repo['parent_id'] in missing:
        missing.append(repo['parent_id'])

print(missing) # None
