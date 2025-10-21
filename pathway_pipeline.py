import warnings
import os
import pathway as pw
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


warnings.filterwarnings("ignore", message=".*pkg_resources.*")
warnings.filterwarnings("ignore", message=".*PEP 484 type hint.*")


os.makedirs("./data", exist_ok=True)

df = pd.read_csv("./data/input_data.csv")
X = df[['feature1', 'feature2']]
y = df['label']

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)
print("Model trained")


class MySchema(pw.Schema):
    feature1: float
    feature2: float
    label: int


input_table = pw.io.csv.read(
    "./data/input_data.csv",
    schema=MySchema,
    mode="static"   # change to "streaming" for live updates
)


def predict_row(feature1, feature2):
    try:
        return int(model.predict([[feature1, feature2]])[0])
    except Exception:
        return -1  # fallback if prediction fails


predicted = input_table.with_columns(
    prediction=pw.apply(predict_row, input_table.feature1, input_table.feature2)
)

pw.io.csv.write(predicted, "./data/output_predictions.csv")

pw.run()
print("Pipeline completed")
