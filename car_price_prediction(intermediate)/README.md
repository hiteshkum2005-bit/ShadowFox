#  Car Price Prediction System

##  Description
This project predicts the selling price of a car using Machine Learning. The model takes various inputs such as showroom price, kilometers driven, fuel type, number of owners, seller type, transmission, and car age to estimate the selling price.

##  Features
- Predicts car selling price based on user input
- Uses Random Forest Regressor for accurate predictions
- Data preprocessing and feature engineering (Car Age)
- One-hot encoding for categorical variables
- User-friendly GUI using tkinter
- Clear button to reset inputs

##  Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Tkinter

##  How to Run

1. Install dependencies:
   pip install -r requirements.txt


##  Example Input
- Showroom Price: 5.5  
- Kilometers Driven: 30000  
- Owner: 0  
- Car Age: 5  
- Fuel Type: Petrol  
- Seller Type: Dealer  
- Transmission: Manual  

##  Output
Predicted Selling Price: ₹3.7 Lakhs (approx)

##  Project Structure
- gui.py → GUI application
- dataset.csv → dataset used
- requirements.txt → dependencies
- README.md → documentation

##  Conclusion
This project demonstrates a complete machine learning pipeline from data preprocessing to model deployment using a GUI for real-world usability.