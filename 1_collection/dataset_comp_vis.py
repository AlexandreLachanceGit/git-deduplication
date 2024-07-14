import json
import matplotlib.pyplot as plt


with open('full.json') as repoFiles:
    repos = json.load(repoFiles)

gitlab_count = 0
github_count = 0
for repo in repos:
    if repo['forge'] == 'github':
        github_count += 1
    else:
        gitlab_count += 1

categories = ['GitHub', 'GitLab']
values = [github_count, gitlab_count]
print(values)

plt.bar(categories, values, color=['blue', 'orange'])

plt.xlabel('Forges')
plt.ylabel('Number of Repos')
plt.title('GitLab vs GitHub Repos')

plt.savefig('forge_dist.svg')
