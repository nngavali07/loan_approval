from flask import Flask, request, jsonify, render_template
from src.utils import LoanApprovalClassification

app = Flask(__name__)
Obj = LoanApprovalClassification()  # ✅ load model + encoders ONCE


@app.route("/")
def home():
    return render_template("predict.html")


@app.route("/education_options")
def education_options():
    return jsonify(list(Obj.encoded_data[" education"].keys()))


@app.route("/self_employed_options")
def self_employed_options():
    return jsonify(list(Obj.encoded_data[" self_employed"].keys()))


@app.route("/prediction", methods=["POST"])
def prediction():
    result = Obj.predict_loan_approval(request.form)
    return jsonify({"Result": result})
