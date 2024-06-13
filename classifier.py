import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

# For building and deploying the model
# import joblib 

df = pd.read_csv('heart_disease.csv')
y = df['target']
X = df.drop('target', axis=1)

X_train, X_test, y_train, y_test  = train_test_split(X,y,test_size=0.10,random_state=101)
scaler = StandardScaler()
scaler.fit(X_train)
scaled_X_train = scaler.transform(X_train)
scaled_X_test = scaler.transform(X_test)

# Cs=10 (default)
classifier = LogisticRegressionCV()
classifier.fit(scaled_X_train, y_train)

chosen_C = classifier.C_
Cs_values = classifier.Cs_
beta_coefs = classifier.coef_

y_pred = classifier.predict(scaled_X_test)

a_score = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
rec_score = recall_score(y_test, y_pred)
prec_score = precision_score(y_test, y_pred)
hmean_rec_prec = f1_score(y_test, y_pred)
cnf_matrix = confusion_matrix(y_test, y_pred)

# final classifying model
final_classifier = LogisticRegression(C=chosen_C[0])
final_classifier.fit(X,y)

# Use this function to build and deploy the model
# joblib.dump(final_classifier, 'heart_classifier.joblib')
if __name__ == "__main__":


    print("Error metrics of the classifier...")
    print(f'Accuracy  score: {a_score}')
    print(f'Classification report: \n{report}')
    print(f'Recall  score: {rec_score}')
    print(f'Precision  score: {prec_score}')
    print(f"f1_score: {hmean_rec_prec}")
    print(f'Confusiion matrix:\n{cnf_matrix}')

