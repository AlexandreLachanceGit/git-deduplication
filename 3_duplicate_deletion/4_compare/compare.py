from difflib import SequenceMatcher
import json
from tqdm import tqdm
import csv
import os
import subprocess

with open('../../1_collection/full.json') as f:
    repos = json.load(f)
    repo_info = {}
    for repo in repos:
        repo_info[repo['id']] = (repo['forge'], repo['commit_ids'][0])


def compare_files(path1, path2):
    with open(path1, 'r') as file1:
        content1 = file1.read()
    with open(path2, 'r') as file2:
        content2 = file2.read()

    seq_matcher = SequenceMatcher(None, content1, content2)
    return seq_matcher.ratio()


def get_all_relative_paths(dir):
    paths = []
    for dir_path, dir_names, file_names in os.walk(dir):
        for file in file_names:
            _, file_extension = os.path.splitext(os.path.join(dir_path, file))
            path = os.path.join(dir_path, file)
            if file_extension[1:] in ['p4', 'sh', 'py'] and not os.path.islink(path):
                paths.append(os.path.relpath(path, dir))
    return paths

# Make sure the project is at latest commit
def checkout_latest_commit(dir, id):
    current_dir = os.getcwd()
    os.chdir(dir)
    subprocess.run(["git", "checkout", repo_info[id][1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.chdir(current_dir)


def compare_directories(dir_1, dir_2): 
    files_1 = get_all_relative_paths(dir_1)
    files_2 = get_all_relative_paths(dir_2)

    common_file_paths = list(set(files_1).intersection(files_2))
    total_file_count = len(list(set(files_1).symmetric_difference(files_2))) + len(common_file_paths)

    if len(common_file_paths) == 0:
        return 0.0

    total_score = 0.0
    for path in common_file_paths:
        total_score += compare_files(dir_1 + path, dir_2 + path)

    return total_score / total_file_count

def get_dir_path(repo_id):
    return f'../../1_collection/{repo_info[repo_id][0]}/repos/{repo_id}/'


def compare_projects(project_id_1, project_id_2):
    dir_1 = get_dir_path(project_id_1)
    dir_2 = get_dir_path(project_id_2)
    checkout_latest_commit(dir_1, project_id_1)
    checkout_latest_commit(dir_2, project_id_2)

    return compare_directories(dir_1, dir_2)


def compare_all():
    with open("../3_reduced_potential_pairs.json", 'r') as potential_pairs_file:
        potential_pairs = json.load(potential_pairs_file)
    with open("scores.csv", mode='w', newline='') as scores_file:
        writer = csv.writer(scores_file)
        for pair in tqdm(potential_pairs):
            score = compare_projects(pair['id1'], pair['id2'])
            writer.writerow([pair['id1'], pair['id2'], score])


compare_all()
