import csv
import matplotlib.pyplot as plt

def generate_vis(scores):
    # plt.hist(scores, bins=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], alpha=0.75, color='b', edgecolor='black')
    plt.hist(scores, bins=10, alpha=0.75, color='b', edgecolor='black')

    plt.xlabel('Scores')
    plt.ylabel('Count')
    plt.title('Similarity Scores')

    plt.savefig('score_dist.svg')

scores = []

with open('scores.csv', newline='') as scoresFile:
    reader = csv.reader(scoresFile)
    for row in reader:
        scores.append(float(row[2]))
        if float(row[2]) > 0.75:
            print(row[2])

generate_vis(scores)
