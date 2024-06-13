import joblib

model = joblib.load('heart_classifier.joblib')

# [[43,1,0,115,303,0,1,181,0,1.2,1,0,2]] --> User input
output = model.predict([[43,1,0,115,303,0,1,181,0,1.2,1,0,2]])
probability = model.predict_proba([[43,1,0,115,303,0,1,181,0,1.2,1,0,2]])
    
probability[0][0] = round(probability[0][0],2)
probability[0][1] = round(probability[0][1],2)

if output[0] == 1:
    print("You have higher chance of having heart disease!")
    print(f"Probability of you having a heart disease is {probability[0][1] * 100}%")
    print(f"Probability of you not having a heart disease is {probability[0][0] * 100}%")
elif output[0] == 0:
    print("You have lower chance of having heart disease!")
    print(f"Probability of you having a heart disease is {probability[0][1] * 100}%")
    print(f"Probability of you not having a heart disease is {probability[0][0] * 100}%")