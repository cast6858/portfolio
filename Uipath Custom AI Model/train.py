import pandas as pd
import re
import string
import os
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

nltk.download('wordnet')

class Main:
    def __init__(self):
        self.model = MultinomialNB()
        self.lemmatizer = WordNetLemmatizer()
        self.tfidf = TfidfVectorizer()

    def cleaning(self, text):
        # removing the word subject, checking for spam inside the subject line all emails contain the word subject
        text = text.replace("Subject", "")
        # making all text lower case
        text_m = text.lower()
        # removing spaces
        text = re.sub('\s+', ' ', text)

        # removing hyper links
        text = text.replace("http://", " ").replace("https://", " ")

        # taking alll punctiation like : !
        text = text.translate(str.maketrans("", "", string.punctuation))

        # removing numbers
        text = re.sub(r"\d+", "", text)

        return text

    def stop_words_removal(self, text):
        txt = ' '.join([word for word in text.split() if word not in stopwords.words("english")])

        return txt

    def lemm_sentence(self, text):
        word_list = nltk.word_tokenize(text)
        lem_out = ' '.join([self.lemmatizer.lemmatize(w) for w in word_list])
        return lem_out

    def save_vector_model(self, vectorize_model):
        with open('vector.pkl', 'wb') as f:
            pickle.dump(vectorize_model, f)

    def train(self, training_data_directory):
        # Load the training data into a Pandas DataFrame
        # Getting Data
        training_data_path = training_data_directory
        df = pd.read_csv(training_data_path)
        # Perp Data
        df['label'] = df['label'].replace(['ham'], 'not-spam')
        df['cleaned_txt'] = df['text'].apply(lambda x: self.cleaning(x))
        df['cleaned_txt'] = df['cleaned_txt'].apply(lambda x: self.stop_words_removal(x))
        df['cleaned_txt'] = df['cleaned_txt'].apply(lambda x: self.lemm_sentence(x))
        df = df.drop(['text'], axis=1)
        # Bring meaning to the words
        x = self.tfidf.fit_transform(df['cleaned_txt'])
        self.save_vector_model(self.tfidf)
        y = df['label']
        # Train
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

        # Fit model
        self.model.fit(x_train, y_train)

    def save(self):
        # Save the model to file
        with open('model.pkl', 'wb') as f:
            pickle.dump(self.model, f)

main = Main()
main.train(r"C:\DataScience_DSC_680\project1\spam_ham_dataset.csv")
main.save()