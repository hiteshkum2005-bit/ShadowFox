import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# =========================
# 1. Load Dataset
# =========================
data = pd.read_csv("dataset.csv")

# =========================
# 2. Preprocessing
# =========================
data = data.drop(['Car_Name'], axis=1)
data['Car_Age'] = 2024 - data['Year']
data = data.drop(['Year'], axis=1)

# =========================
# 3. Encoding
# =========================
data = pd.get_dummies(data, drop_first=True)

# =========================
# 4. Split Data
# =========================
X = data.drop('Selling_Price', axis=1)
y = data['Selling_Price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 5. Train Model
# =========================
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# =========================
# 6. USER INPUT SECTION 🔥
# =========================
print("\nEnter Car Details:")

present_price = float(input("Showroom Price (in lakhs): "))
kms_driven = int(input("Kilometers Driven: "))
owner = int(input("Number of previous owners (0/1/2): "))
car_age = int(input("Car Age (years): "))

fuel_type = input("Fuel Type (Petrol/Diesel): ").strip().capitalize()
seller_type = input("Seller Type (Dealer/Individual): ").strip().capitalize()
transmission = input("Transmission (Manual/Automatic): ").strip().capitalize()

# =========================
# 7. Create Input Data
# =========================
input_data = {
    'Present_Price': present_price,
    'Kms_Driven': kms_driven,
    'Owner': owner,
    'Car_Age': car_age,
    'Fuel_Type_Diesel': 1 if fuel_type == "Diesel" else 0,
    'Fuel_Type_Petrol': 1 if fuel_type == "Petrol" else 0,
    'Seller_Type_Individual': 1 if seller_type == "Individual" else 0,
    'Transmission_Manual': 1 if transmission == "Manual" else 0
}

input_df = pd.DataFrame([input_data])

# =========================
# 8. Prediction
# =========================
predicted_price = model.predict(input_df)

print(f"\nPredicted Selling Price: ₹{round(predicted_price[0], 2)} Lakhs")