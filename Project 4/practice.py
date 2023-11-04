from flask import Flask, render_template, request, redirect, url_for
import requests
from config import geoapify_key
import pandas as pd
import joblib

app = Flask(__name__, static_url_path='/static', static_folder='static')

#Load the diabetes predictor model
model = joblib.load("diabetes_model.joblib")
 

@app.route("/")
def home():
    return render_template("home_page.html")

@app.route("/Metrics", methods=["POST", "GET"])
def Metrics():
    if request.method == "POST":
        blood_pressure = int(request.form["Blood Pressure"])
        glucose = int(request.form["Glucose"])
        bmi = int(request.form["BMI"])

        def categorize_blood_pressure(value):
            if value < 60:
                return "Low"
            elif 60 <= value < 70:
                return "Normal"
            elif 70 <= value < 80:
                return "Elevated"
            elif 80 <= value < 90:
                return "High Stage 1"
            elif 90 <= value <= 120:
                return "High Stage 2"
            else:
                return "Invalid"

        def categorize_glucose(value):
            if value < 100:
                return "Normal"
            elif 100 <= value < 126:
                return "Prediabetic"
            else:
                return "Diabetic"

        def categorize_bmi(value):
            if value < 18.5:
                return "Underweight"
            elif 18.5 <= value < 24.9:
                return "Normal Weight"
            elif 25 <= value < 29.9:
                return "Overweight"
            elif 30 <= value < 34.9:
                return "Obesity Class I"
            elif 35 <= value < 39.9:
                return "Obesity Class II"
            else:
                return "Obesity Class III"

        # Categorize user inputs
        bp_category = categorize_blood_pressure(blood_pressure)
        glucose_category = categorize_glucose(glucose)
        bmi_category = categorize_bmi(bmi)

        return render_template("Metrics.html", bp_category=bp_category, glucose_category=glucose_category, bmi_category=bmi_category)
    else:
        return render_template("Metrics.html")



    

@app.route("/Predictor", methods=["POST", "GET"])
def Predictor():
    if request.method == "POST":
        blood_pressure = float(request.form["Blood Pressure"])
        glucose = float(request.form["Glucose"])
        bmi = float(request.form["BMI"])
        age = float(request.form["Age"])
        
        
        # Create a DataFrame from the user inputs and median data 
        data = pd.DataFrame({
            "Glucose": [glucose],
            "BloodPressure": [blood_pressure],
            "SkinThickness": 29,
            "Insulin": 125,
            "BMI": [bmi],
            "DiabetesPedigreeFunction": 0.378,
            "Age": [age],
        })

        # Use your machine learning model to make predictions
        prediction = model.predict(data)

        # Define the response message based on the prediction
        if prediction[0] == 0:
            response = "No diabetes risk detected"
        else:
            response = "Potential diabetes risk detected"
        
        # Return the response message to the user
        return f"Diabetes Prediction: {response}"
    else:
        return render_template("Predictor.html")
        
@app.route("/Nearest_Doc", methods=["POST", "GET"])
def Nearest_Doc():
    print("Entered Nearest_Doc function") 
    if request.method == "POST":
        Postcode = request.form["Postcode"]
         

        return render_template("Nearest_Doc.html")
 



@app.route("/Information")
def Information():
    return render_template("Information.html")

if __name__ == "__main__":
    app.run(debug=True)
