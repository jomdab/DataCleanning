import PyPDF2
import spacy
import csv
import os
import string
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
nlp = spacy.load("en_core_web_sm")

# import PDF file
annual_report = open(r"D:\NLP for ESG project\annual report\4.ADVANCE.PDF", mode='rb')
pdf_reader = PyPDF2.PdfFileReader(annual_report, strict=False)

print("page number =", pdf_reader.numPages)

all_page = ''
for page in range(pdf_reader.numPages):
    all_page += pdf_reader.getPage(page).extractText()

# extract sentence
doc = nlp(all_page)
sents = []
for sent in doc.sents:
    sents.append(sent.text)
    # print(sent)
    # print("-------------------------------------------------------------------------------------")

print("sentence number =", len(sents))

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create a CSV file in the same directory as the script
output_file_path = os.path.join(current_dir, "sentences_output.csv")

# Write sentences to the CSV file
with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(["Sentence Index", "Sentence"])
    for index, sentence in enumerate(sents, start=1):
        csv_writer.writerow([index, sentence])

print("Sentences written to:", output_file_path)
