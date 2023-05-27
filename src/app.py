from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
api = Api(app)

def log_transform(X):
    X_df = pd.DataFrame(X, columns=num_features)
    X_df['LoanAmount'] = np.log(X_df['LoanAmount'])
    X_df['log_total_income'] = np.log(X_df['ApplicantIncome'] + X_df['CoapplicantIncome'])
    X_df.drop(columns=['ApplicantIncome', 'CoapplicantIncome'], inplace=True)
    return X_df

# log_transform_obj = FunctionTransformer(log_transform)

cat_features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Credit_History', 'Property_Area']
num_features = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']

model = pickle.load(open('model.sav', 'rb'))



class Predict(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        df.replace('NaN', np.nan, inplace=True)
        # getting predictions from our model
        res = model.predict(df)
        # need to convert results because they come out as a numpy array
        return res.tolist()
    
api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)