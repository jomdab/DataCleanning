import os
from rules import rule
import csv

def get_score_list(file):
    scores_dict = {label: None for label in rule}
    try:
        with open(file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_label = row.get('Label')
                row_score = float(row.get('Score')) if 'Score' in row else None
                if row_label in scores_dict:
                    scores_dict[row_label] = row_score

        # Ensure there are no missing scores
        if None in scores_dict.values():
            return []  # Return an empty list if there are missing scores

        ordered_scores = [scores_dict[label] for label in rule]
        return ordered_scores
    except FileNotFoundError:
        print(f"File not found: {file}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_data(folder_path):
    data_files = []
    for filename in os.listdir(folder_path):
        if not filename.startswith("valid"):
            data_files.append(filename)
    # print(data_files)
    return data_files

def get_company_score(file_name):
    n = file_name.split('.')[0]
    for i in range(len(n)):
        if n[i].isdigit():
            year_index = i
            break
    name = n[:year_index]
    year = n[year_index:]
    with open('scores.csv',mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['ABV'] == name and row['Year'] == year:
                return row['Score']
    print('cant find the score of ',name,year)
    return None
    
def main():
    with open('dataset.csv',mode='w',newline='') as file:
        writer = csv.writer(file)
        output_list = get_data("output")
        for output_file in output_list:
            ESG_score = get_score_list(os.path.join('output',output_file))
            target = get_company_score(output_file)
            ESG_score.append(target)
            writer.writerow(ESG_score)
    print(f"Data has been written.")
main()
    
