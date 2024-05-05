import streamlit as st
import pandas as pd
import nltk
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
import joblib
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from imblearn.pipeline import Pipeline as ImbPipeline

def cleantext(text):
  # Remove URLs
  text = re.sub(r'https?://\S+|http://\S+|www\.\S+',' ', text)
  # Remove non-printable characters
  text = re.sub(r'[\x00-\x1F\x7F-\x9F]',' ', text)
  # Remove text starting with "URL"
  text = re.sub(r'\bURL\S*',' ', text)
  # Expand contractions
  text = contractions.fix(text)
  text = re.sub(r'<[^.>]+>', '', text)
  text = re.sub(r',', '', text)
  text = re.sub(r'\.', ' ', text)
  # Remove special characters and unknown symbols
  text = re.sub(r'[^a-zA-Z0-9\s]',' ', text)
  # Remove occurrences of '\xa0'
  text = text.replace('\xa0',' ')
  return text

def get_simple_pos(tag):
  if tag.startswith('J'):
      return wordnet.ADJ
  elif tag.startswith('V'):
      return wordnet.VERB
  elif tag.startswith('N'):
      return wordnet.NOUN
  elif tag.startswith('R'):
      return wordnet.ADV
  else:
      return wordnet.NOUN

def tokenize_text(text):
  # Tokenize text
  tokens = word_tokenize(text)
  # Remove stopwords and punctuation
  stop = set(stopwords.words('english')) | set(string.punctuation)
  tokens = [token for token in tokens if token.lower() not in stop]
  # POS tagging
  tagged_tokens = pos_tag(tokens)
  # Initialize lemmatizer
  lemmatizer = WordNetLemmatizer()
  # Lemmatization
  lemmatized_tokens = [lemmatizer.lemmatize(token, get_simple_pos(tag)).lower() for token, tag in tagged_tokens]
  # Rejoin tokens into a string
  return ' '.join(lemmatized_tokens)

st.set_page_config(page_title="Fraudulent Job Posting Prediction")

if 'key' not in st.session_state:
  st.session_state['key'] = 'value'
  nltk.download('stopwords')
  nltk.download('punkt')
  nltk.download('averaged_perceptron_tagger')
  nltk.download('wordnet')
  
pipeline=joblib.load('pipeline.pkl')
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
#salary=st.text_input("Salary Range")
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
    text = title + ' ' + country  + ', ' + city + ' ' + dept + ' ' + profile + ' ' + desc + ' ' + req + ' ' + benefit + ' ' + emp_type + ' ' + req_exp + ' ' + req_edu + ' ' + industry + ' ' + function
    df2=pd.DataFrame({"telecommuting":telecom,"has_company_logo":logo,"has_questions":questions,"text":text},index=[0])
    fraud=pipeline.predict(df2)[0]
    if not fraud:
      st.success("The job is less likely a fraud.")
    else:
      st.error("The job is likely a fraud!")