import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

df = pd.read_csv("employee_activity.csv")

model = IsolationForest(
    n_estimators=150,
    contamination=0.05,
    random_state=42
)

model.fit(df)

joblib.dump(model, "insider_model.pkl")

print("Model trained and saved as insider_model.pkl")
