from difflib import SequenceMatcher
import json
from tqdm import tqdm
import csv

with open('../../1_collection/full.json') as f:
    repos = json.load(f)
    repo_forge = {}
    for repo in repos:
        repo_forge[repo['id']] = repo['forge']


def compare_files(path1, path2):
    with open(path1, 'r') as file1:
        content1 = file1.read()
    with open(path2, 'r') as file2:
        content2 = file2.read()

    seq_matcher = SequenceMatcher(None, content1, content2)
    return seq_matcher.ratio()


def get_all_relative_paths(dir):
    for dir_path, dir_names, file_names in os.walk(dir):
        for file in file_names:
            relative_path = os.path.relpath(os.path.join(dir_path, file), dir)


def compare_directories(dir_1, dir_2):
    files_1 = get_all_relative_paths(dir_1)
    files_2 = get_all_relative_paths(dir_2)

    common_file_paths = list(set(files_1).intersection(files_2))
    total_file_count = len(list(set(files_1).symmetric_difference(files_2))) + len(common_files)

    total_score = 0.0
    for path in common_file_paths:
        total_score += compare_files(dir_1 + path, dir_2 + path)

    return total_score / total_file_count

def get_dir_path(repo_id):
    return f'../../1_collection/{repo_forge[repo_id]}/repos/{repo_id}/'


def compare_projects(project_id_1, project_id_2):
    return compare_directories(
            get_dir_path(project_id_1),
            get_dir_path(project_id_2)
            )


def compare_all():
    with open("../3_reduced_potential_pairs.json", 'r') as potential_pairs_file:
        potential_pairs = json.load(potential_pairs_file)
    with open("scores.csv") as scores_file:
        writer = csv.writer(scores_file)
        for pair in tqdm(potential_pairs):
            score = compare_projects(pair['id1'], pair['id2'])
            writer.writerow([pair['id1'], pair['id2'], score])


compare_all()
