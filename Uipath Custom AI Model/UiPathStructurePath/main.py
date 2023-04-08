
import pickle
import json
import re
import string
import os
import pandas as pd
# nlp
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk.data.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nltk_data'))


class Main:
    def __init__(self):
        self.model = None
        self.tfidf = pickle.load(open('vector.pkl', 'rb'))
        self.lemmatizer = WordNetLemmatizer()


        with open('model.pkl', 'rb') as f:
            self.model = pickle.load(f)



    def cleaning(self, text):
        try:
            mod_text = text
            # removing the word subject, checking for spam inside the subject line all emails contain the word subject
            if 'Subject' in mod_text:
                mod_text = text.replace("Subject", "")

            # making all text lower case
            mod_text = mod_text.lower()

            res = bool(re.search(r"\s", mod_text))
            if res:
                # removing spaces
                mod_text = re.sub('\s+', ' ', mod_text)

            if 'http://' or 'https://' in mod_text:
                # removing hyper links
                mod_text = mod_text.replace("http://", " ").replace("https://", " ")

            # taking all punctuation like : !
            mod_text = mod_text.translate(str.maketrans("", "", string.punctuation))

            hasNumVal = bool(re.search(r'\d', mod_text))
            if hasNumVal:
                # removing numbers
                mod_text = re.sub(r"\d+", "", mod_text)

            return mod_text
        except:
            return text


    def stop_words_removal(self, text):
        txt = ' '.join([word for word in text.split() if word not in stopwords.words("english")])

        return txt

    def lemm_sentence(self, text):
        word_list = nltk.word_tokenize(text)
        lem_out = ' '.join([self.lemmatizer.lemmatize(w) for w in word_list])
        return lem_out

    def preprocess(self, text):
        # Preprocess the input string
        text = self.cleaning(text)
        text = self.stop_words_removal(text)
        text = self.lemm_sentence(text)
        return text



    def predict(self, text):
        # Preprocess the input string
        text = self.preprocess(text)

        # Vectorize the preprocessed text
        x = self.tfidf.transform([text])

        # Make a prediction
        y_pred = self.model.predict(x)

        confidence = self.model.predict_proba(x)[0][0]

        #Making a threshold

        if confidence >= .75:
            result = {'prediction': 'spam', 'confidence': str(confidence)}
        else:
            result = {'prediction': 'not spam', 'confidence': str(confidence)}

        json_result = json.dumps(result)
        return json_result




'''main = Main()

spam_ham_df = pd.read_csv("C:\DataScience_DSC_680\project1\spam_ham_dataset.csv" , nrows=10)

for text in spam_ham_df['text']:
    result = main.predict(text)
    print(result)

Test Out Sucessful 100 percent correct : 
0.999863652135829
not-spam
0.999812161694688
not-spam
0.9908645857646956
not-spam
0.2545463858753426
spam
0.9977972289447704
not-spam
0.947918128380438
not-spam
0.9204215291465883
not-spam
0.061929380050151785
spam
0.9999991802187885
not-spam
0.9998242406509068
not-spam'''