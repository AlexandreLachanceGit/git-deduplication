import time
import json
import requests
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

output = []

with open("basic.json") as f:
    data = json.load(f)

i = 0

# Your GitHub API token (replace 'YOUR_TOKEN' with your actual token)
headers = {'Authorization': 'token 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'}

for repo in data:
    i += 1
    name = repo["full_name"]
    
    # Make a request to the GitHub API
    res = requests.get(f"https://api.github.com/repos/{name}", headers=headers)
    
    # Check the rate limit information
    remaining_requests = int(res.headers.get('X-RateLimit-Remaining', 0))
    reset_time = int(res.headers.get('X-RateLimit-Reset', 0))
    
    if remaining_requests == 0:
        # Sleep until the rate limit resets, plus a little buffer (usually 60 seconds)
        sleep_time = reset_time - int(time.time()) + 60
        eprint(f"Rate limit reached. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
    
    output.append(res.json())

    eprint(i, name, res)
    time.sleep(0.5)

print(json.dumps(output, indent=4))

