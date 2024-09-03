import numpy as np
import json
import random
from tensorflow.keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer
import pickle

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# 데이터 로드
with open('C:/my_chatbot/data/intents.json') as file:
    intents_json = json.load(file)

with open('C:/my_chatbot/chatbot/words.pkl', 'rb') as file:
    words = pickle.load(file)

with open('C:/my_chatbot/chatbot/classes.pkl', 'rb') as file:
    classes = pickle.load(file)

# 모델 로드
model = load_model('C:/my_chatbot/chatbot/chatbot_model.keras')

def clean_up_sentence(sentence):
    # 문장 토큰화 및 정제
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # Bag of Words 벡터 생성
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return(np.array(bag))

def predict_class(sentence, model):
    # 클래스 예측
    bow_vector = bow(sentence, words, show_details=False)
    prediction = model.predict(np.array([bow_vector]))[0]
    return prediction

def get_response(prediction):
    # 응답 생성
    intent_index = np.argmax(prediction)
    tag = classes[intent_index]
    
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response

    return "Sorry, I didn't understand that."
