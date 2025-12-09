from flask import Flask, request, jsonify, render_template
from src.utils import LoanApprovalClassification
import os

app = Flask(__name__)
Obj = LoanApprovalClassification()


@app.route("/")
def home():
    return render_template("predict.html")


@app.route("/prediction-page")
def prediction_page():
    return render_template("predict.html")


@app.route("/education_options")
def education_options():
    label_data = Obj.load_json_data()
    return jsonify(list(label_data[" education"].keys()))


@app.route("/self_employed_options")
def self_employed_options():
    label_data = Obj.load_json_data()
    return jsonify(list(label_data[" self_employed"].keys()))


@app.route("/prediction", methods=["POST"])
def predictions():
    data = request.form
    approval_pred = Obj.predict_loan_approval(data)

    print("FINAL VALUE IN MAIN:", repr(approval_pred))

    if approval_pred == "Approved":
        return jsonify({"Result": "Loan Approved"})
    else:
        return jsonify({"Result": "Loan Declined"})


