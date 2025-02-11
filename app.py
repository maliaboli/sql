from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate SQL query from question
def get_sql_query(question):
    prompt = f"""
    You are an AI assistant that converts natural language questions into SQL queries.

    ### Database Schema:
    - **STUDENT(NAME, CLASS, SECTION, MARKS)**
    - **TEACHER(NAME, SUBJECT, EXPERIENCE)**
    - **COURSES(COURSE_NAME, DURATION, FEES)**

    ### Instructions:
    1. Identify the **correct table** based on the question.
    2. Generate an **accurate SQL query**.
    3. **Do NOT include** explanations, formatting (no "```sql"), or extra words.

    ### Examples:
    - **Q:** "Who is Abhi?"  
      ✅ **Output:** SELECT NAME, CLASS, MARKS FROM STUDENT WHERE NAME = 'Abhi';

    - **Q:** "List all students."  
      ✅ **Output:** SELECT NAME FROM STUDENT;

    - **Q:** "What subject does Dr. Smith teach?"  
      ✅ **Output:** SELECT SUBJECT FROM TEACHER WHERE NAME = 'Dr. Smith';

    Now, generate the SQL query for: "{question}"
    """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    sql_query = response.text.strip()

    # Remove unwanted formatting
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query

# Function to execute SQL query and return clean results
# Function to execute SQL query and return unique results
def execute_sql_query(sql_query):
    conn = sqlite3.connect("student.db")
    cur = conn.cursor()
    try:
        cur.execute(sql_query)
        rows = cur.fetchall()

        # Convert results into a clean, unique output (removes duplicates)
        unique_results = list(set([", ".join(map(str, row)) for row in rows]))

    except sqlite3.Error as e:
        unique_results = [f"SQL Error: {str(e)}"]

    conn.close()
    return unique_results

# Function to generate natural response
def generate_natural_response(question, sql_query, query_result):
    prompt = f"""
    You are an AI assistant that transforms SQL query results into a **natural, human-readable response**.

    ### SQL Query:
    {sql_query}

    ### Query Result:
    {query_result}

    ### Instructions:
    - **Convert the query result** into a clear, concise response.
    - **DO NOT show SQL syntax or special characters.**
    - **DO NOT include unnecessary explanations.**
    - If the query is about a person, provide an introduction.
    - If the query returns a list, just list the names.
    - If no results are found, return "No matching records found."

    Now, generate a response:
    """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    return response.text.strip()

# Streamlit App
st.set_page_config(page_title="SQL Query & Response Generator")
st.header("SQL-Powered AI Chatbot")

question = st.text_input("Enter your question: ")

if st.button("Get Answer"):
    sql_query = get_sql_query(question)
    st.subheader("Generated SQL Query")
    st.code(sql_query, language="sql")

    query_result = execute_sql_query(sql_query)
    st.subheader("SQL Query Result")
    
    # Display clean SQL results
    for row in query_result:
        st.write(row)

    natural_response = generate_natural_response(question, sql_query, query_result)
    st.subheader("Text Response")
    st.write(natural_response)
