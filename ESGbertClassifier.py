import pandas as pd
import transformers
from transformers import pipeline,AutoTokenizer
import csv
import os

classifier = pipeline("text-classification", model="nbroad/ESG-BERT", device='cpu')
tokenizer = AutoTokenizer.from_pretrained("nbroad/ESG-BERT")
output_folder = "output"

def get_report_score(sentences,file):
    scores = [0.0]*26
    for sent in sentences:
        result = classifier(sent[0],top_k=None)
        for i in range(26):
            scores[i] += result[i]['score']


    csv_filename = os.path.join(output_folder, f"{file}.csv")

    # Write the label-score pairs to the CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Label', 'Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(26):
            label = result[i]['label']
            score = scores[i]
            writer.writerow({'Label': label, 'Score': score})
        