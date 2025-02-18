import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Load Data
data = pd.read_csv("/app/orders.csv").sample(5000, random_state=42)

# Preprocessing
data["Customer Status"] = data["Customer Status"].str.lower()
data["Customer Status"] = LabelEncoder().fit_transform(data["Customer Status"])
data["Date Order was placed"] = pd.to_datetime(data["Date Order was placed"])
data["Delivery Date"] = pd.to_datetime(data["Delivery Date"])
data["Delivery Days"] = (data["Delivery Date"] - data["Date Order was placed"]).dt.days

# Features and Target
X = data[["Customer Status", "Quantity Ordered", "Total Retail Price for This Order", "Cost Price Per Unit"]]
y = data["Delivery Days"]  # Example target variable

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save Model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as model.pkl")
# curl -X POST http://localhost:5001/predict \
# -H "Content-Type: application/json" \
# -d '{
#   "Customer Status": 1,
#   "Quantity Ordered": 10,
#   "Total Retail Price for This Order": 500,
#   "Cost Price Per Unit": 45
# }'
