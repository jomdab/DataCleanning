import csv
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import fitz
import os


class AnnualReportClassifier:
    def __init__(self, file_path, esg_model_name='yiyanghkust/finbert-esg'):
        self.file_path = file_path
        self.esg_model_name = esg_model_name
        self.extracted_sentences = None
        self.E = 0
        self.S = 0
        self.G = 0
        self.N = 0

        # Load the esg-bert model and tokenizer
        self.finbert = BertForSequenceClassification.from_pretrained(self.esg_model_name, num_labels=4)
        self.tokenizer = BertTokenizer.from_pretrained(self.esg_model_name)
        self.nlp = pipeline("text-classification", model=self.finbert, tokenizer=self.tokenizer)

    def load_sentences_from_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            sentences = [line.strip() for line in f.readlines()[1:]]
        return sentences

    def classify_sentences(self,text):
        # Load the extracted sentences from "extracted_sentences.txt"
        self.extracted_sentences = text
        # Load the esg-bert model and tokenizer
        self.finbert = BertForSequenceClassification.from_pretrained(self.esg_model_name, num_labels=4)
        self.tokenizer = BertTokenizer.from_pretrained(self.esg_model_name)
        self.nlp = pipeline("text-classification", model=self.finbert, tokenizer=self.tokenizer)

        # Process each sentence and obtain classification results
        classification_results = []
        for sentence in self.extracted_sentences:
            result = self.nlp(sentence)
            label = result[0]["label"]
            if label == 'Environmental':
                self.E += 1
            if label == 'Social':
                self.S += 1
            if label == 'Governance':
                self.G += 1
            if label == 'None':
                self.N +=1
            classification_results.append((sentence, label))

        return classification_results

    def save_classification_to_csv(self, classification_results, output_file_path):
        with open(output_file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Sentence", "Category"])
            writer.writerows(classification_results)

    def exclude_none_esg_sentences(self, classification_results):
        valid_classification_results = [(sentence, category) for sentence, category in classification_results if category != "None"]
        return valid_classification_results

    def process_report(self,text):
        name = self.file_path[1]
        year = self.file_path[-1].split('.')[0]
        # Classify sentences
        classification_results = self.classify_sentences(text)
        # Excluding None-ESG sentences
        valid_classification_results = self.exclude_none_esg_sentences(classification_results)
        output_file_path = os.path.join('output', f"valid_{name}{year}.csv")
        self.save_classification_to_csv(valid_classification_results, output_file_path)
        # print(f"Valid classification results have been saved to {output_file_path}.")
        # print(f"E = {self.E} sentences")
        # print(f"S = {self.S} sentences")
        # print(f"G = {self.G} sentences")
        # print(f"N = {self.N} sentences")
        return valid_classification_results


if __name__ == "__main__":
    file_path = 'processed_sentences.csv'
    report_classifier = AnnualReportClassifier(file_path)
    report_classifier.process_report()
