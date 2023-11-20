import json
from tqdm import tqdm
import time
import os
from pathlib import Path
import csv

from tree_dist import distance, Tree

# {A
#     {B
#         {X}
#         {Y}
#         {F}
#     }
#     {C}
# }
def build_tree(path):
    return Tree.from_text("{" + _build_tree(path) + "}")

def _build_tree(path):
    output = path.name
    for entry in path.iterdir():
        current = ""
        if entry.is_symlink():
            continue
        elif entry.is_file():
            current = entry.name
        elif entry.is_dir() and entry.name != ".git":
            current = _build_tree(entry)
        else:
            continue
        output += "{" + current + "}"
    return output

def load_repos(path):
    path = Path(path)
    output = {}
    for repo in path.iterdir():
        output[int(repo.name)] = [build_tree(repo)]
    return output

print("Loading file trees...")
file_trees = load_repos("../collection/github/repos/") | load_repos("../collection/gitlab/repos/")

print("Loading potential pairs...")
with open("./maybe_downloads_pairs.json") as f:
    potential_pairs = json.loads(f.read())


with open("out.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    for pair in tqdm(potential_pairs):
        project_tree = file_trees[pair["id1"]][0]
        other_project_tree = file_trees[pair["id2"]][0]

        treeDist = distance(project_tree, other_project_tree)
        levDist = pair["levenshteinDistance"]

        total = treeDist + levDist

        writer.writerow([pair["id1"], pair["id2"], treeDist, levDist, total])

        
