import string
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

# data = pd.read_csv(r"sentences_output.csv" ,encoding='mac_roman') 

# # Remove newline characters '\n'
# data['Sentence'] = data['Sentence'].str.replace(r'\n', ' ')

# # Removing Punctuations
# data['Sentence'] = data['Sentence'].apply(lambda x: x.translate(str.maketrans('','', string.punctuation)))

# removing urls
def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'',text)
# data['Sentence']=data['Sentence'].apply(lambda x : remove_URL(x))

# # removing numbers
# data['Sentence']=data['Sentence'].apply(lambda x : ''.join([i for i in x if not i.isdigit()]))

# Removing Special Characters
def remove_special_characters(text):
    # Keep only alphanumeric characters and spaces
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned_text

# data['Sentence'] = data['Sentence'].apply(lambda x: remove_special_characters(x))

# lemmatization
def lemmatization(text):
    temp=[]
    for t in nlp(text):
        temp.append(t.lemma_)
    return " ".join(temp)
# data['Sentence']=data['Sentence'].apply(lambda x : lemmatization(x) )

# Stop word
def stop_word(text):
    temp=[]
    for t in nlp(text):
        if not nlp.vocab[t.text].is_stop :
            temp.append(t.text)
    return " ".join(temp)


def remove_extra_whitespace(sentence):
    # Removing extra spaces and tabs from the sentence
    return re.sub(r'\s+', ' ', sentence).strip()

def remove_person_names(sentence):

    # Process the sentence with the NLP pipeline
    doc = nlp(sentence)

    # Filter out person names and return the sentence without them
    filtered_sentence = ' '.join(token.text for token in doc if token.ent_type_ != 'PERSON')
    return filtered_sentence

# data['Sentence']=data['Sentence'].apply(lambda x : stop_word(x) )

# # Remove rows with empty or whitespace-only Sentence
# data = data[data['Sentence'].str.strip().astype(bool)]

# data['Sentence'] = data['Sentence'].apply(remove_extra_whitespace)
# data['Sentence'] = data['Sentence'].apply(remove_person_names)

# # create csv file.
# output_file_path = r"processed_sentences.csv"
# data.to_csv(output_file_path, index=False, encoding='utf-8')

# print("Processed data saved to:", output_file_path)