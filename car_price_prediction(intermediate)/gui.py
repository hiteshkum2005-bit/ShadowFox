import tkinter as tk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# =========================
# 1. Load & Train Model
# =========================
data = pd.read_csv("dataset.csv")

data = data.drop(['Car_Name'], axis=1)
data['Car_Age'] = 2024 - data['Year']
data = data.drop(['Year'], axis=1)

data = pd.get_dummies(data, drop_first=True)

X = data.drop('Selling_Price', axis=1)
y = data['Selling_Price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# =========================
# 2. Functions
# =========================
def predict_price():
    try:
        present_price = float(entry_price.get())
        kms_driven = int(entry_km.get())
        owner = int(entry_owner.get())
        car_age = int(entry_age.get())

        fuel_type = fuel_var.get()
        seller_type = seller_var.get()
        transmission = trans_var.get()

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

        # 🔥 IMPORTANT FIX (ensures correct columns)
        input_df = input_df.reindex(columns=X.columns, fill_value=0)

        prediction = model.predict(input_df)

        result_label.config(
            text=f"Predicted Price: ₹{round(prediction[0], 2)} Lakhs",
            fg="green"
        )

    except Exception as e:
        print("ERROR:", e)
        result_label.config(text="⚠ Please enter valid inputs", fg="red")


def clear_fields():
    entry_price.delete(0, tk.END)
    entry_km.delete(0, tk.END)
    entry_owner.delete(0, tk.END)
    entry_age.delete(0, tk.END)

    fuel_var.set("Petrol")
    seller_var.set("Dealer")
    trans_var.set("Manual")

    result_label.config(text="")

# =========================
# 3. GUI Design
# =========================
root = tk.Tk()
root.title("Car Price Prediction")
root.geometry("420x550")
root.configure(bg="#f2f2f2")

# Title
title = tk.Label(root, text="🚗 Car Price Predictor",
                 font=("Arial", 18, "bold"),
                 bg="#f2f2f2")
title.pack(pady=10)

# Frame
frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

def create_label_entry(text):
    tk.Label(frame, text=text, bg="#f2f2f2").pack()
    entry = tk.Entry(frame, width=25)
    entry.pack(pady=5)
    return entry

entry_price = create_label_entry("Showroom Price (in lakhs)")
entry_km = create_label_entry("Kilometers Driven")
entry_owner = create_label_entry("Owner (0/1/2)")
entry_age = create_label_entry("Car Age")

# Dropdowns
fuel_var = tk.StringVar(value="Petrol")
tk.Label(frame, text="Fuel Type", bg="#f2f2f2").pack()
tk.OptionMenu(frame, fuel_var, "Petrol", "Diesel").pack(pady=5)

seller_var = tk.StringVar(value="Dealer")
tk.Label(frame, text="Seller Type", bg="#f2f2f2").pack()
tk.OptionMenu(frame, seller_var, "Dealer", "Individual").pack(pady=5)

trans_var = tk.StringVar(value="Manual")
tk.Label(frame, text="Transmission", bg="#f2f2f2").pack()
tk.OptionMenu(frame, trans_var, "Manual", "Automatic").pack(pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Predict", width=12,
          bg="#4CAF50", fg="white",
          command=predict_price).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Clear", width=12,
          bg="#f44336", fg="white",
          command=clear_fields).grid(row=0, column=1, padx=10)

# Result
result_label = tk.Label(root, text="",
                        font=("Arial", 12, "bold"),
                        bg="#f2f2f2")
result_label.pack(pady=20)

# Run
root.mainloop()