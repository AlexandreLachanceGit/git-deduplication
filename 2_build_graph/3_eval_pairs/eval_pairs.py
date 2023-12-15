import json
from tqdm import tqdm
import time
import os
import subprocess
from pathlib import Path
import csv

from tree_dist import distance, Tree

def build_trees(path, commit_ids):
    if len(commit_ids) > 1:
        return [
            build_tree_at_commit(path, commit_ids[len(commit_ids) - 2]),
            build_tree_at_commit(path, commit_ids[0])
        ]
    else:
        tree = build_tree_at_commit(path, commit_ids[0])
        return [tree, tree]

def build_tree_at_commit(path, commit_id):
    os.chdir(path)
    subprocess.run(["git", "checkout", commit_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.chdir("../../../../2_build_graph/3_eval_pairs/")
    return build_tree(path)

def build_tree(path):
    tree = _build_tree(path)
    return (Tree.from_text("{" + tree[0] + "}"), tree[1])


def _build_tree(path):
    output = path.name
    nb_files = 1
    for entry in path.iterdir():
        current = ""
        if entry.is_symlink():
            continue
        elif entry.is_file():
            current = entry.name
            nb_files += 1
        elif entry.is_dir() and entry.name != ".git":
            current = _build_tree(entry)
            nb_files += current[1]
        else:
            continue
        output += "{" + current[0] + "}"
    return (output, nb_files)

def load_repos():
    with open("../../1_collection/full.json") as f:
        repos = json.load(f)

    output = {}
    for repo in tqdm(repos, desc="Loading file trees"):
        if repo["forge"] == "github":
            path = Path(f"../../1_collection/github/repos/{repo['id']}")
        elif repo["forge"] == "gitlab":
            path = Path(f"../../1_collection/gitlab/repos/{repo['id']}")

        output[repo["id"]] = build_trees(path, repo["commit_ids"])
    return output

with open("../maybe_downloads_pairs.json") as f:
    potential_pairs = json.load(f)

file_trees = load_repos()

with open("distance.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    for pair in tqdm(potential_pairs, desc="Calculating pair distances"):
        project_tree = file_trees[pair["id1"]][1]
        potential_match_tree = file_trees[pair["id2"]][0]

        if max(project_tree[1], potential_match_tree[1]) / min(project_tree[1], potential_match_tree[1]) < 2:
            treeDist = distance(project_tree[0], potential_match_tree[0])
        else:
            treeDist = None
        levDist = pair["levenshteinDistance"]

        if treeDist:
            total = treeDist + levDist
        else:
            total = None

        writer.writerow([pair["id1"], pair["id2"], project_tree[1], potential_match_tree[1], treeDist, levDist, total])

        
