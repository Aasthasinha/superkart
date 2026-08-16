
# Import Libraries
import numpy as np
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify


class SuperKartAPI():

    def __init__(self, model_path="superkart_model.joblib"):

        if not os.path.exists(model_path) and os.path.exists(
            f"backend_files/{model_path}"
        ):
            model_path = f"backend_files/{model_path}"

        # Load the model
        self.model = joblib.load(model_path)

        # Create Flask application
        self.app = Flask(__name__)

        # Register routes
        self._register_routes()
    def _build_sample(self, data_source):
        """Helper method to construct a uniform sample dictionary from a dict or pandas Series/dict-like row."""
        return {
            'Product_Weight': data_source.get('Product_Weight'),
            'Product_Sugar_Content': data_source.get('Product_Sugar_Content'),
            'Product_Allocated_Area': data_source.get('Product_Allocated_Area'),
            'Product_MRP': data_source.get('Product_MRP'),
            'Store_Size': data_source.get('Store_Size'),
            'Store_Location_City_Type': data_source.get('Store_Location_City_Type'),
            'Store_Type': data_source.get('Store_Type'),
            'Product_Category_Code': data_source.get('Product_Category_Code', data_source.get('Product_Id_char')),
            'Store_Age_Years': data_source.get('Store_Age_Years'),
            'Product_Type_Category': data_source.get('Product_Type_Category')
        }


    def _register_routes(self):

        @self.app.route("/", methods=["GET"])
        def home():
            return jsonify({
                "status": "online",
                "message": "SuperKart API is up and running"
            })
        

        @self.app.route("/v1/predict", methods=["POST"])
        def predict():
            try:
                data = request.get_json(force=True)
                sample = self._build_sample(data)
                input_df = pd.DataFrame([sample])
                result = self.model.predict(input_df)
                return jsonify({
                    "status": "success",
                    "prediction": float(result[0])
                })

            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400

        @self.app.route("/v1/predictbatch", methods=["POST"])
        def predictbatch():
            try:
                file = request.files["file"]

                if not file:
                    return jsonify({
                        "status": "error",
                        "message": "No file found"
                    }), 400
                raw_df = pd.read_csv(file)
                processed_rows = [self._build_sample(row) for _, row in raw_df.iterrows()]
                input_df = pd.DataFrame(processed_rows)
                results = self.model.predict(input_df)

                predictions_dict = {
                    str(idx): float(result)
                    for idx, result in enumerate(results)
                }

                return jsonify({
                    "status": "success",
                    "predictions": predictions_dict
                })

            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400


# Create the Flask application
superkart_api = SuperKartAPI().app
