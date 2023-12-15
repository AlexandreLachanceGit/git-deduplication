import csv
import json
import matplotlib.pyplot as plt

TREE_DIST_WEIGHT = 0.8
LEV_DIST_WEIGHT = 0.2

def generate_vis(scores):
    plt.hist(scores, bins=50, alpha=0.75, color='b', edgecolor='black')

    plt.xlabel('Scores')
    plt.ylabel('Count')
    plt.title('Quick-Similarity Scores')

    plt.savefig('score_dist.png')


with open("../../1_collection/full.json") as f:
    repos = json.load(f)

name_lens = {}
for repo in repos:
    name_lens[repo['id']] = len(repo['name'])


scores = []
with open('distance.csv', newline='') as distance_file :
    reader = csv.reader(distance_file)
    with open("scores.csv", mode='w', newline='') as scores_file:
        writer = csv.writer(scores_file)

        for row in reader:
            id1 = int(row[0])
            nb_files1 = int(row[2])

            id2 = int(row[1])
            nb_files2 = int(row[3])

            # Normalize tree distance
            try:
                tree_dist = int(row[4])
                norm_tree_dist = 1 - (tree_dist / max(nb_files1, nb_files2))
            except:
                norm_tree_dist = 0.0

            # Normalize levenshtein distance
            lev_dist = int(row[5])
            norm_lev_dist = 1 - (lev_dist / max(name_lens[id1], name_lens[id2]))

            # Calculate similarity score
            score = norm_tree_dist * TREE_DIST_WEIGHT + norm_lev_dist * LEV_DIST_WEIGHT
            if score < 0:
                score = 0.0

            writer.writerow([id1, id2, score])

            scores.append(score)

generate_vis(scores)
