# Cleanup data and add commits
import sys
import os
import subprocess
import json

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_commit_ids(repo_id):
    os.chdir(f"repos/{repo['id']}")

    result = subprocess.run(["git", "log", "--pretty=oneline"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    raw_commits = output.splitlines()
    commit_ids = []
    for c in raw_commits:
        id = c.split(" ", 1)[0]
        commit_ids.append(id)

    os.chdir("../..")
    return commit_ids

new_data = []

with open("more.json") as f:
    data = json.load(f)

for i, repo in enumerate(data):
    eprint(i, repo["full_name"])
    commit_ids = get_commit_ids(repo['id'])
    
    new_repo = {
        "forge": "github",
        "id": repo['id'],
        "name": repo['name'],
        "full_name": repo['full_name'],
        "description": repo['description'],
        "created_at": repo['created_at'],
        "updated_at": repo['updated_at'],

        "allow_forking": repo['allow_forking'],
        "forks_count": repo['forks_count'],

        "stars": repo['stargazers_count'],

        "owner_id": repo['owner']['id'],
        "owner_username": repo['owner']['login'],

        "commit_ids": commit_ids,

        "fork": repo['fork'],
        "parent_id": None,
        "parent_name": None,
        "parent_full_name": None,
        "parent_creator_id": None,

        "source_id": None,
        "source_name": None,
        "source_full_name": None,
        "source_creator_id": None,
    }

    if repo["fork"] == True:
        new_repo["parent_id"] = repo['parent']['id']
        new_repo["parent_name"] = repo['parent']['name']
        new_repo["parent_full_name"] = repo['parent']['full_name']
        new_repo["parent_creator_id"] = repo['parent']['owner']['id']

        new_repo["source_id"] = repo['source']['id']
        new_repo["source_name"] = repo['source']['name']
        new_repo["source_full_name"] = repo['source']['full_name']
        new_repo["source_creator_id"] = repo['source']['owner']['id']

    new_data.append(new_repo)

print(json.dumps(new_data, indent=4))


