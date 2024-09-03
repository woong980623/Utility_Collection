import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import random
import json
import pickle

# NLTK 리소스 다운로드
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# JSON 파일을 읽어옴
with open('C:/my_chatbot/data/intents.json') as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

# 데이터 저장
with open('C:/my_chatbot/chatbot/words.pkl', 'wb') as f:
    pickle.dump(words, f)
    
with open('C:/my_chatbot/chatbot/classes.pkl', 'wb') as f:
    pickle.dump(classes, f)

# 훈련 데이터 생성
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in doc[0]]
    
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])

# NumPy 배열로 변환
training = np.array(training, dtype=object)

# 훈련 데이터와 레이블 분리
train_x = np.array([elem[0] for elem in training])
train_y = np.array([elem[1] for elem in training])

# 모델 생성
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# 모델 컴파일
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# 모델 훈련
model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# 모델 저장
model.save('chatbot_model.keras')
