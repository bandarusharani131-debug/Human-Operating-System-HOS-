import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("datasets/diabetes.csv")

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(n_estimators=100)

model.fit(X_train, y_train)

print("Diabetes Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "models/diabetes_model.pkl")