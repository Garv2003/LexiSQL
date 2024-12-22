import google.generativeai as genai
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path
import mysql.connector
from tabulate import tabulate
import re
import os
from dotenv import load_dotenv

load_dotenv()

# genai.configure(api_key =os.getenv("GOOGLE_API_KEY"))
     
# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Garv",
  database="stepout_db"
)

from sqlalchemy import create_engine

def get_engine_for_mysql_db():
    """Create a MySQL engine."""
    # Replace these parameters with your actual MySQL database credentials
    username = 'root'
    password = 'Garv'
    host = 'localhost'  # or your MySQL server address
    database = 'stepout_db'

    # Create the engine using MySQL connector
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{database}')
    return engine

engine = get_engine_for_mysql_db()

db = SQLDatabase(engine)

generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(model_name = "gemini-pro",
                              generation_config = generation_config,
                              safety_settings = safety_settings)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY"),  
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

print(toolkit.get_tools())


# def read_sql_query(sql, db):
#     mycursor = mydb.cursor()
#     cleaned_text = cleaned_sql = sql.replace("```sql", "").replace("```", "").strip()
#     print(cleaned_text,"cleaned text")
#     mycursor.execute(cleaned_text)
#     myresult = mycursor.fetchall()
    
#     # Create a list of column names
#     headers = [x[0] for x in mycursor.description]
    
#     # Print the table using tabulate
#     print(tabulate(myresult, headers=headers, tablefmt="grid"))

# prompt_parts_1 = [
#     "You are an expert in converting English questions to SQL code! Write SQL code to answer the following question;",
# ]
     
# question = "how many tables in db?"

# def generate_gemini_response(question, input_prompt):
#     prompt_parts = [input_prompt, question]
#     response = model.generate_content(prompt_parts)
#     print(response.text)
#     read_sql_query(response.text, mydb)

# generate_gemini_response(question,
#                          prompt_parts_1[0])