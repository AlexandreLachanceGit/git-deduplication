import json
import os
from commits import github_to_schema, eprint
import requests
import time

with (open("./github.json") as f):
    repos_json = json.load(f)

id_set = set()
for repo in repos_json:
    id_set.add(repo['id'])

missing = []
for repo in repos_json:
    if repo['parent_id'] != None and not repo['parent_id'] in id_set and not repo['parent_id'] in missing:
        missing.append(repo['parent_id'])

new_repos = []
headers = {'Authorization': 'token ' + os.environ.get('GITHUB_TOKEN')}

for repo_id in missing:
    if repo_id == 579828356:
        continue
    res = requests.get(f"https://api.github.com/repositories/{repo_id}", headers=headers)
    repo = res.json()
    remaining_requests = int(res.headers.get('X-RateLimit-Remaining', 0))
    reset_time = int(res.headers.get('X-RateLimit-Reset', 0))
    
    if remaining_requests == 0:
        sleep_time = reset_time - int(time.time()) + 60
        eprint(f"Rate limit reached. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)

    
    repo_url = repo['clone_url']

    destination_path = f'./repos/{repo_id}'
    os.system(f'git clone {repo_url} {destination_path}')

    new_repos.append(github_to_schema(repo))

with open('missing.json', mode='w') as f:
    json.dump(new_repos, f)
