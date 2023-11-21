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

with open("basic.json") as f:
    data = json.load(f)

for i, repo in enumerate(data):
    eprint(i, repo["path_with_namespace"])
    commit_ids = get_commit_ids(repo['id'])
    
    new_repo = {
        "forge": "gitlab",
        "id": repo['id'],
        "name": repo['path'],
        "full_name": repo['path_with_namespace'],
        "description": repo['description'],
        "created_at": repo['created_at'],
        "updated_at": repo['updated_at'],

        "allow_forking": repo['forking_access_level'] == "enabled",
        "forks_count": repo['forks_count'],

        "stars": repo['star_count'],

        "owner_id": None,
        "owner_username": None,

        "commit_ids": commit_ids,

        "fork": repo.get("forked_from_project", None) != None,
        "parent_id": None,
        "parent_name": None,
        "parent_full_name": None,
        "parent_creator_id": None,

        "source_id": None,
        "source_name": None,
        "source_full_name": None,
        "source_creator_id": None,
    }

    if repo.get("owner"):
        new_repo["owner_id"] = repo['owner']['id']
        new_repo["owner_username"] = repo['owner']['username']

    if new_repo["fork"] == True:
        new_repo["parent_id"] = repo['forked_from_project']['id']
        new_repo["parent_name"] = repo['forked_from_project']['path']
        new_repo["parent_full_name"] = repo['forked_from_project']['path_with_namespace']

    new_data.append(new_repo)

print(json.dumps(new_data, indent=4))


