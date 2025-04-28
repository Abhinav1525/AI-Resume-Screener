from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Sample training data (Skills, Experience, Similarity Score)
X_train = [
    [5, 2, 0.85], [3, 0, 0.60], [7, 5, 0.90], 
    [4, 1, 0.70], [6, 3, 0.80], [2, 0, 0.50], 
    [8, 4, 0.95], [1, 0, 0.40], [10, 7, 0.99]
]
y_train = [1, 0, 1, 1, 1, 0, 1, 0, 1]  # More diverse examples

# Retrain model
model = RandomForestClassifier()
model.fit(X_train, y_train)


# Predict ATS Score
def predict_resume_score(skills_count, experience, similarity):
    return round(model.predict_proba([[skills_count, experience, similarity]])[0][1] * 100, 2)
