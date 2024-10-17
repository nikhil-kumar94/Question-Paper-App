import streamlit as st
import requests

# Define the FastAPI backend URL
API_URL = "http://localhost:8000/papers"

st.title("Comprehensive Sample Paper Creator")

# Paper details form
title = st.text_input("Paper Title")
paper_type = st.selectbox("Paper Type", ["Previous Year", "Model Paper"])
time = st.number_input("Time (in minutes)", min_value=0)
marks = st.number_input("Total Marks", min_value=0)
board = st.text_input("Board", "CBSE")
grade = st.number_input("Grade", min_value=1, max_value=12)
subject = st.text_input("Subject", "Maths")
tags = st.text_input("Tags (comma-separated)", "algebra,geometry")
chapters = st.text_input("Chapters (comma-separated)", "Quadratic Equations,Triangles")

# Sections and questions
st.write("Add Sections and Questions")
sections = []
if "sections" not in st.session_state:
    st.session_state.sections = []

if st.button("Add Section"):
    st.session_state.sections.append({"section_id": f"s{len(st.session_state.sections)+1}", "title": "", "questions": []})

for i, section in enumerate(st.session_state.sections):
    st.session_state.sections[i]["title"] = st.text_input(f"Section {i+1} Title", key=f"section_title{i}")
    
    if st.button(f"Add Question to Section {i+1}"):
        st.session_state.sections[i]["questions"].append({
            "question_id": f"q{len(st.session_state.sections[i]['questions'])+1}",
            "text": "",
            "answer": ""
        })
    
    for j, question in enumerate(st.session_state.sections[i]["questions"]):
        st.session_state.sections[i]["questions"][j]["text"] = st.text_input(f"Question {i+1}.{j+1}", key=f"q{i}{j}")
        st.session_state.sections[i]["questions"][j]["answer"] = st.text_input(f"Answer {i+1}.{j+1}", key=f"a{i}{j}")

# Submit the form
if st.button("Create Sample Paper"):
    paper_data = {
        "paper_id": f"paper_{title.replace(' ', '_')}",
        "title": title,
        "sections": st.session_state.sections
    }
    
    # Send the data to FastAPI backend
    response = requests.post(API_URL, json=paper_data)

    if response.status_code == 200:
        st.success("Sample Paper Created Successfully!")
    else:
        st.error("Failed to create paper. Please check your input and try again.")
