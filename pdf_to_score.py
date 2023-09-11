import os
import pytoPDF
import string
import data_cleanning
from annualReportClassifier import AnnualReportClassifier
import ESGbertClassifier

def find_subfolder(root_folder, target_folder_name):
    # Create a list of subfolder names
    subfolders = [f.name for f in os.scandir(root_folder) if f.is_dir()]

    # Check if the target folder name is in the list of subfolders
    if target_folder_name in subfolders:
        return os.path.join(root_folder, target_folder_name)
    else:
        return None  # Return None if the folder is not found
    
def list_files_in_folder(folder_path):
    # Create a list to store file paths
    file_paths = []
    
    # Walk through the directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_paths.append(file_path)
    
    return file_paths

def pdf_to_text(file_path):
    report_text = pytoPDF.extract_text_from_pdf(file_path=file_path)
    sents = pytoPDF.tokenize_sentences(report_text)
    # cleaned_sentences = [sentence.replace("\n", " ") for sentence in sents]
    cleaned_sentences = pytoPDF.remove_table_of_contents(sents)
    return cleaned_sentences

def cleaning_text(sent):
    sent = [s.translate(str.maketrans('', '', string.punctuation)) for s in sent]   #remove punctuation
    sent = [data_cleanning.remove_URL(s) for s in sent] #remove URL
    sent = [''.join([char for char in s if not char.isdigit()]) for s in sent]  #remove number
    sent = [data_cleanning.remove_special_characters(s) for s in sent]  #remove special character
    sent = [data_cleanning.lemmatization(s) for s in sent]  #lemmatization
    sent = [data_cleanning.stop_word(s) for s in sent]  #remove stop_word
    sent = [s for s in sent if s.strip()]
    sent = [data_cleanning.remove_extra_whitespace(s) for s in sent]
    sent = [data_cleanning.remove_person_names(s) for s in sent]
    return sent


def process_file(file_path):
    file = file_path.split('\\')[2].split('.')[0]
    sentences = []
    sentences = pdf_to_text(file_path)
    if(len(sentences) == 0):
        print("Cannot extract text from file ",file_path)
    else:
        sentences = cleaning_text(sentences)
        #classify by Finbert (E,S,G,N)
        classifier = AnnualReportClassifier(file_path)
        sentences = classifier.process_report(sentences)
        ESGbertClassifier.get_report_score(sentences=sentences,file=file)


def find_and_list_files(root_folder, target_folder_name):
    # Find the subfolder with the specified name
    subfolder_path = find_subfolder(root_folder, target_folder_name)

    if subfolder_path:
        print(f"Current subfolder '{target_folder_name}': {subfolder_path}")
        # List all files in the subfolder
        files_in_subfolder = list_files_in_folder(subfolder_path)
        for file_path in files_in_subfolder:
            print(f"Current File: {file_path}")
            process_file(file_path)
    else:
        print(f"Subfolder '{target_folder_name}' not found.")


def main():
    root_folder = 'input'
    target_folder_file = 'company.txt'

    # Read the target folder name from company.txt
    with open(target_folder_file, 'r') as file:
        target_folder_name = file.read().splitlines()

    # Find the subfolder with the specified name
    for company in target_folder_name:
         find_and_list_files(root_folder, company)

if __name__ == "__main__":
    main()