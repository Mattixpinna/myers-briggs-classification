import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd

def get_class_proba(y):
    n = len(y)
    y_vals, y_counts = np.unique(y, return_counts=True)
    class_probs = {y_val: y_count/n for y_val, y_count in zip(y_vals, y_counts)}
    return class_probs
        

def get_att_proba(attribute, a_name,  y):
    y_vals, y_counts = np.unique(y, return_counts=True)

    probs_x_att = probs_x_att = {y_val: [0] * 7 for y_val in y_vals}
    value_to_index = { -3: 0, -2: 1, -1: 2, 0: 3, 1: 4, 2: 5, 3: 6 } # mappa valori del dataset a indici delle probabilità
    
    for i, y_val in enumerate(y_vals):
        a_vals, a_counts = np.unique(attribute, return_counts=True)
        for j, a_val in enumerate(a_vals):
            count = sum(np.array(y==y_val) & np.array(attribute==a_val))
            probs_x_att[y_val][value_to_index[a_val]] = count/y_counts[i]

    return probs_x_att

import numpy as np

def test_bayes(probs, class_probs, X_test):
    predictions = []
    values_to_index = { -3: 0, -2: 1, -1: 2, 0: 3, 1: 4, 2: 5, 3: 6 }
    attr_list = X_test.columns.tolist()
    for i in range(0, np.shape(X_test)[0]):
        max_prob = -1
        max_class = None
        for y_val in class_probs.keys():
            prob = class_probs[y_val]
            for j in range(0, np.shape(X_test)[1]):
                prob *= probs[attr_list[j]][y_val][values_to_index[X_test.iloc[i,j]]]
            if prob > max_prob:
                max_prob = prob
                max_class = y_val
        predictions.append(max_class)
    return predictions




df = pd.read_csv("16P.csv", encoding='cp1252')
# Separate features and target
X = df.drop(columns=['Personality'])  # Adjust if column name is different
X = X.drop(columns=['Response Id'])  # remove response id since it has 0 predictive power
y = df['Personality']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

class_probs = get_class_proba(y_train)
print(class_probs)
question_columns = df.columns[1:-1].tolist()  # Select all columns except the last one
entire_probability = {}
for col in range(0,np.shape(X_train)[1]):
    entire_probability.update({question_columns[col]: get_att_proba(X_train.iloc[:,col], question_columns[col], y_train)})

# test
print("Test")
y_pred = test_bayes(entire_probability, class_probs, X_test)
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy:.4f}")

# confront with sklearn
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy:.4f}")
