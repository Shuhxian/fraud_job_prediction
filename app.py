from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd
from sklearn import set_config
set_config(transform_output="pandas")
import joblib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('deploy.html')

@app.route('/predict', methods=(['POST']))
def predict():
    data=request.json
    print(data)
    res={}
    for key,val in data.items():
        if val: 
            res[key]=int(val)
        else:
            res[key]=None
    #df=pd.DataFrame(res)
    # print(df)
    # pipeline = joblib.load('pipeline.pkl')
    resp = "Real" #pipeline.predict(df)[0]
    response=jsonify({'resp': resp})
    resp=make_response(response,200)
    return resp