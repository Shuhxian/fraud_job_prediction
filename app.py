import streamlit as st
import pandas as pd
import nltk
st.set_page_config(page_title="Fraudulent Job Posting Prediction")

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

df=pd.read_csv("fake_job_postings.csv")
df = df.drop(columns=['job_id'])
location_split = df['location'].str.split(', ', expand=True)
df['Country'] = location_split[0]
df['City'] = location_split[1]
df.fillna("",inplace=True)

#st.write('Hello, *World!* :sunglasses:')
st.image("image.png")
st.header("Fraudulent Job Posting Prediction")
st.write("Developed by G1 Group 8")

title=st.text_input("Job Title")
desc=st.text_area("Job Description")
profile=st.text_area("Company Profile")
req=st.text_area("Requirements")
benefit=st.text_area("Benefits")
salary=st.text_input("Salary Range")
industry=st.selectbox("Industry",sorted(df.industry.unique()))
dept=st.text_input("Department")#too many values,sorted(df.department.unique()))
function=st.selectbox("Function",sorted(df.function.unique()))
emp_type=st.selectbox("Employment Type",sorted(df.employment_type.unique()))
req_exp=st.selectbox("Required Experience",sorted(df.required_experience.unique()))
req_edu=st.selectbox("Required Education",sorted(df.required_education.unique()))
country=st.selectbox("Country",sorted(df.Country.unique()))
city=st.selectbox("City",sorted(df[df.Country==country].City.unique()))
logo = st.checkbox("Has Company Logo")
telecom = st.checkbox("Telecommuting")
questions = st.checkbox("Has Questions")

submitted = st.button("Submit")
#deploy model
fraud = True
if submitted:
  if not fraud:
    st.success("The job is less likely a fraud.")
  else:
    st.error("The job is likely a fraud!")