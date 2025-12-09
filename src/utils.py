import json
import pickle
import config
import pandas as pd


class LoanApprovalClassification:

    def load_model(self):
        with open(config.MODEL_FILE_PATH, "rb") as f:
            self.model = pickle.load(f)
        return self.model

    def load_json_data(self):
        with open(config.LABEL_DATA_PATH, "r") as f:
            self.encoded_data = json.load(f)
        return self.encoded_data

    def predict_loan_approval(self, input_user_data):
        # Load model and encoders
        self.load_model()
        self.load_json_data()

        d = input_user_data

        income = int(d[" income_annum"])
        loan_amount = int(d[" loan_amount"])

        # ✅ CRITICAL FIX:
        # Dataset loan_term is in YEARS
        # UI sends MONTHS → convert to YEARS
        loan_term_years = int(d[" loan_term"]) / 12

        # ✅ Build feature dictionary (MATCHES TRAINING EXACTLY)
        data_dict = {
            " no_of_dependents": int(d[" no_of_dependents"]),
            " education": self.encoded_data[" education"][d[" education"]],
            " self_employed": self.encoded_data[" self_employed"][d[" self_employed"]],
            " income_annum": income,
            " loan_amount": loan_amount,
            " loan_term": loan_term_years,   # ✅ FIXED
            " cibil_score": int(d[" cibil_score"]),
            " residential_assets_value": int(d[" residential_assets_value"]),
            " commercial_assets_value": int(d[" commercial_assets_value"]),
            " luxury_assets_value": int(d[" luxury_assets_value"]),
            " bank_asset_value": int(d[" bank_asset_value"]),
            "loan_to_income_ratio": loan_amount / income if income > 0 else 0
        }

        # ✅ Create DataFrame and align columns
        test_df = pd.DataFrame([data_dict])
        test_df = test_df.reindex(
            columns=self.model.feature_names_in_,
            fill_value=0
        )

        # ✅ Predict probability
        proba = self.model.predict_proba(test_df)[0]
        classes = self.model.named_steps["model"].classes_

        approved_index = list(classes).index("Approved")
        approved_prob = proba[approved_index]

        print("Approved probability:", approved_prob)

        # ✅ Decision threshold
        return "Approved" if approved_prob >= 0.30 else "Rejected"
