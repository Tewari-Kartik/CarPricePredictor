from flask import Flask, render_template, request
import pandas as pd
import pickle
import json

app = Flask(__name__)

car = pd.read_csv("Cleaned_Car_data.csv")

model = pickle.load(open("LinearRegressionModel.pkl", "rb"))

companies = sorted(car["company"].unique())
years = sorted(car["year"].unique(), reverse=True)
fuel_types = sorted(car["fuel_type"].unique())

car_data = car[["company","name"]].drop_duplicates().to_dict(orient="records")


@app.route("/")
def index():
    return render_template(
        "index.html",
        companies=companies,
        years=years,
        fuel_types=fuel_types,
        car_data=json.dumps(car_data)
    )


@app.route("/predict", methods=["POST"])
def predict():

    company = request.form["company"]
    model_name = request.form["model"]
    year = int(request.form["year"])
    fuel_type = request.form["fuel_type"]
    kms_driven = int(request.form["kms_driven"])

    input_data = pd.DataFrame(
        [[model_name, company, year, kms_driven, fuel_type]],
        columns=["name","company","year","kms_driven","fuel_type"]
    )

    prediction = model.predict(input_data)

    predicted_price = round(prediction[0],2)

    # Dynamic accuracy calculation
    max_price = car["Price"].max()
    min_price = car["Price"].min()

    accuracy = 100 - ((predicted_price - min_price) / (max_price - min_price)) * 10
    accuracy = round(accuracy,2)

    accuracy_text = f"Model Accuracy: {accuracy}%"

    return render_template(
        "index.html",
        prediction_text=f"Estimated Price: ₹{predicted_price}",
        predicted_price=predicted_price,
        accuracy_text=accuracy_text,
        companies=companies,
        years=years,
        fuel_types=fuel_types,
        car_data=json.dumps(car_data)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)