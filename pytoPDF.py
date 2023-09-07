import PyPDF2
import nltk
import re
from nltk.tokenize import sent_tokenize
import fitz
import csv
import os
import string
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
import fitz

def extract_text_from_pdf(file_path):
    report_text = ""
    with fitz.open(file_path) as pdf_document:
        num_pages = pdf_document.page_count
        for page_num in range(num_pages):
            page = pdf_document[page_num]
            report_text += page.get_text("text")
    return report_text

def calculate_digit_percentage(sentence):
    # Helper function to calculate the percentage of digits in a string
    total_chars = len(sentence)
    digit_chars = sum(char.isdigit() for char in sentence)
    return (digit_chars / total_chars) * 100

def tokenize_sentences(text):
    return sent_tokenize(text)

def split_long_sentences(sentence, max_length=512):
    # Helper function to split long sentences into chunks
    words = sentence.split()
    chunks = []
    current_chunk = ""
    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_length:  # +1 for space
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

def remove_table_of_contents(sentences, min_words=3):
    cleaned_sentences = []
    for sentence in sentences:
        # Removing leading and trailing whitespaces
        sentence = sentence.strip()

        # Ignore sentences starting with "Table of Contents" or "Contents"
        if (
            sentence.lower().startswith("table of contents")
            or sentence.lower().startswith("contents")
            or re.search(r'\.{6,}', sentence)  # Check for multiple dots
            or re.search(r'-\s*-\s*-', sentence)
        ):
            continue

        # Split long sentences into shorter chunks
        chunks = split_long_sentences(sentence)

        for chunk in chunks:
            # Counting words in the chunk
            num_words = len(chunk.split())

            # Exclude chunks that have fewer words than the minimum threshold
            if num_words >= min_words:
                # Removing extra whitespace characters
                chunk = re.sub(r'\s+', ' ', chunk)

                # Calculate the percentage of digits in the chunk
                digit_percentage = calculate_digit_percentage(chunk)

                # Exclude chunks containing more than 50% digits
                if digit_percentage <= 50:
                    cleaned_sentences.append(chunk)

    return cleaned_sentences


# import PDF file
report_text = extract_text_from_pdf(file_path='input.pdf')
sents = tokenize_sentences(report_text)
# cleaned_sentences = [sentence.replace("\n", " ") for sentence in sents]
cleaned_sentences = remove_table_of_contents(sents)

print("sentence number =", len(cleaned_sentences))

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create a CSV file in the same directory as the script
output_file_path = os.path.join('', "sentences_output.csv")

# Write sentences to the CSV file
with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(["Sentence Index", "Sentence"])
    for index, sentence in enumerate(cleaned_sentences, start=1):
        csv_writer.writerow([index, sentence])

print("Sentences written to:", output_file_path)
