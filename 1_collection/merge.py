import json

with open("github/github.json") as gh:
    gh_repos = json.load(gh)

with open("github/missing.json") as ghm:
    ghm_repos = json.load(ghm)

with open("gitlab/gitlab.json") as gl:
    gl_repos = json.load(gl)

with open("gitlab/missing.json") as glm:
    glm_repos = json.load(glm)

gh_repos.extend(gl_repos)
gh_repos.extend(ghm_repos)
gh_repos.extend(glm_repos)

print(json.dumps(gh_repos, indent=4))
