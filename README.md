# Fraud Job Prediction
A model to predict fraudulent jobs deployed via Streamlit. Can be run using containers or locally.

## Installation
```
docker build -t streamlit .
```

## How to Run (Docker)
```
docker run -p 8080:8080 streamlit
```

## How to Run (Local)
```
pip install -r requirements.txt
streamlit run app.py --server.port=8080 --server.address=0.0.0.0
```

Navigate to localhost:8080 (or the specified server.port) to access the website.