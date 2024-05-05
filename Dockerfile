FROM python:3.9-slim

# Expose port you want your app on
EXPOSE 8080

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

RUN mkdir app
WORKDIR /app
COPY app.py app.py
COPY image.png image.png
COPY fake_job_postings.csv fake_job_postings.csv
COPY pipeline.pkl pipeline.pkl

# Run
ENTRYPOINT ["streamlit","run","app.py","--server.port=8080","--server.address=0.0.0.0"]