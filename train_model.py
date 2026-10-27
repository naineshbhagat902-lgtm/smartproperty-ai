import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# Load property data
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "properties.csv"
MODEL_FILE = BASE_DIR / "property_model.pkl"

df = pd.read_csv(DATA_FILE)

# Features used to predict property price
features = [
    "location",
    "property_type",
    "area_sqft",
    "building_age"
]
target = "price_lakh"

# Keep rows with all required information
df = df[features + [target]].dropna()
df = df[df["area_sqft"] > 0]

if len(df) < 5:
    raise ValueError(
        "Add at least 5 valid property listings before training."
    )

X = df[features]
y = df[target]

# Convert text categories into numbers
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categories",
            OneHotEncoder(handle_unknown="ignore"),
            ["location", "property_type"]
        ),
        (
            "numbers",
            "passthrough",
            ["area_sqft", "building_age"]
        )
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ))
])

# Evaluate on a held-out sample when enough data is available
if len(df) >= 10:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Test mean absolute error: ₹{mae:.2f} lakh")

# Train the final model using all available rows
model.fit(X, y)
joblib.dump(model, MODEL_FILE)

print(f"Model trained on {len(df)} property listings.")
print(f"Model saved to: {MODEL_FILE}")
print("Note: predictions are experimental with a small dataset.")
