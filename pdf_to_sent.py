import re
from nltk.tokenize import sent_tokenize
import fitz
from nltk.stem.snowball import SnowballStemmer
import fitz
import matplotlib.pyplot as plt
import statistics

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

def cal_limit(sentences,dev_fac=1):
    lengths = [len(sentence.split()) for sentence in sentences]
    std_dev = statistics.stdev(lengths)
    avg_length = avg_len(sentences)
    upper_limit = avg_length + (dev_fac * std_dev)
    lower_limit = avg_length - (dev_fac * std_dev)
    return upper_limit,lower_limit

def split_long_sentences(sentences,upper,lower):
    filtered_sentences = [sentence for sentence in sentences if lower <= len(sentence.split()) <= upper]
    return filtered_sentences

def remove_table_of_contents(sentences):
    cleaned_sentences = []
    for sentence in sentences:
        # Removing leading and trailing whitespaces
        sentence = sentence.strip()
        sentence = re.sub(r'\s+', ' ', sentence)

        # Ignore sentences starting with "Table of Contents" or "Contents"
        if (
            sentence.lower().startswith("table of contents")
            or sentence.lower().startswith("contents")
            or re.search(r'\.{6,}', sentence)  # Check for multiple dots
            or re.search(r'-\s*-\s*-', sentence)
            or calculate_digit_percentage(sentence) > 50
        ):
            continue
        else:
            cleaned_sentences.append(sentence)
    return cleaned_sentences

# def plot_sentence_length_distribution(sentences):
#     sentence_lengths = [len(sentence.split()) for sentence in sentences]
#     max_length = max(sentence_lengths)
#     sentence_lengths.sort()
#     print(sentence_lengths)
#     plt.hist(sentence_lengths, bins=range(0, max_length, 5), alpha=0.7, color='blue')
#     plt.xlabel('Sentence Length')
#     plt.ylabel('Frequency')
#     plt.title('Distribution of Sentence Lengths')
#     plt.grid(True)
#     plt.show()

def avg_len(sentences):
    num_sentences = len(sentences)
    avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / num_sentences
    return avg_sentence_length

# import PDF file
# import os
# import csv
# report_text = extract_text_from_pdf(file_path='done/ADVANC/ADVANC2018.pdf')
# sents = tokenize_sentences(report_text)
# cleaned_sentences = remove_table_of_contents(sents)

# print("sentence number =", len(cleaned_sentences))

# # Get the current working directory
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Create a CSV file in the same directory as the script
# output_file_path = os.path.join('', "sentences_output.csv")

# # Write sentences to the CSV file
# with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
#     csv_writer = csv.writer(output_file)
#     csv_writer.writerow(["Sentence Index", "Sentence"])
#     for index, sentence in enumerate(cleaned_sentences, start=1):
#         csv_writer.writerow([index, sentence])

# print("Sentences written to:", output_file_path)
