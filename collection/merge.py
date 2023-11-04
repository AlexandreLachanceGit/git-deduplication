import json

with open("github/github.json") as gh:
    gh_repos = json.load(gh)

with open("gitlab/gitlab.json") as gl:
    gl_repos = json.load(gl)

gh_repos.extend(gl_repos)

print(json.dumps(gh_repos, indent=4))
