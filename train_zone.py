import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import random
import os

# Generate sample data
n = 200
df = pd.DataFrame({
    "Distance": [random.uniform(10, 150) for _ in range(n)],
    "Available_Slots": [random.randint(0, 5) for _ in range(n)],
    "Avg_Wait": [random.randint(5, 40) for _ in range(n)],
    "Battery_Type": random.choices(["Lithium-ion 48V", "Nickel-MH", "Lead-Acid"], k=n),
    "Status": random.choices(["online", "offline", "maintenance"], k=n)
})

# Assign target zone
def assign_zone(row):
    if row["Distance"] > 100 or row["Available_Slots"] == 0 or row["Status"] != "online" or row["Avg_Wait"] > 30:
        return "Red"
    elif row["Distance"] <= 80:
        return "Green"
    elif row["Distance"] <= 100:
        return "Yellow"
    return "Red"

df["Zone"] = df.apply(assign_zone, axis=1)

# Encode categorical features
battery_encoder = LabelEncoder()
status_encoder = LabelEncoder()

df["Battery_Type_enc"] = battery_encoder.fit_transform(df["Battery_Type"])
df["Status_enc"] = status_encoder.fit_transform(df["Status"])

X = df[["Distance", "Available_Slots", "Avg_Wait", "Battery_Type_enc", "Status_enc"]]
y = df["Zone"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Create model folder if needed
os.makedirs("model", exist_ok=True)

# Save model & encoders
with open("model/zone_predictor.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model/battery_encoder.pkl", "wb") as f:
    pickle.dump(battery_encoder, f)

with open("model/status_encoder.pkl", "wb") as f:
    pickle.dump(status_encoder, f)

print("✅ Model and encoders saved in /model folder")
