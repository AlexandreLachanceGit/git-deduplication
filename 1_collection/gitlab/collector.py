import time
import json
import requests
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

output = []

headers = {'PRIVATE-TOKEN': '-'}

while True:
    params = {
        'with_programming_language': 'p4',
        'page': '1',
        'per_page': '48',
    }

    res = requests.get(f"https://gitlab.com/api/v4/projects", params=params, headers=headers)

    eprint(res)

    if not res.ok:
        eprint(res.json())
        time.sleep(10)
        continue
    else:
        output.extend(res.json())
        time.sleep(1)
        break
    

eprint("Total:", len(output))
print(json.dumps(output, indent=4))
