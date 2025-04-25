'''
This is the flow of the application

1. Field to enter Job description
2. Upload resume pdf
3. convert pdf to image for processing - google gemini pro model based on prompts
4. Multiple Prompt Template
'''

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import base64
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model =genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App for UI
    
st.set_page_config(page_title="Resume Revise Insight HUb")
st.header("Resume Insight HUb")

input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


#Functionalities
    
submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Resume Match Score")

input_prompt1 = """
 You are an experienced Human Resource Manager with technical expertise in the field of data science, full stack web development, Big Data Engineering, DEVOPS, Data Analyst. Your task is to review the provided resume against the job description for these profiles. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 ="""
You are a Technical Human Resource Manager with expertise in  the field of data science, full stack web development, Big Data Engineering, DEVOPS, Data Analyst 
Your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective. 
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.


"""
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of in the field of data science, full stack web development, Big Data Engineering, DEVOPS, Data Analyst and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of resume match if the resume matches
the job description. First the output should come as resume match percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("Reponse ...")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("Reponse ...")
        st.write(response)        
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.subheader("Reponse ...")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

