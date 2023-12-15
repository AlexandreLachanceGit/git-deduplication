import csv
import random

def get_sample(file_path, threshold, sample_size):
    result = []
    with open(file_path, mode='r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            id1, id2, score = row
            if float(score) > threshold:
                result.append((id1, id2, score, None))
    return random.sample(result, sample_size)

sample = get_sample('../3_duplicate_deletion/4_compare/scores.csv', 0.75, 50)

with open('sample.csv', mode='w') as sample_file:
    writer = csv.writer(sample_file)
    writer.writerow(['id1', 'id2', 'score', 'true_duplicate'])
    writer.writerows(sample)

