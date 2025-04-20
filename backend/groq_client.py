import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_medical_report(caption: str) -> str:
    prompt = f"""
You are an expert radiologist. Based on the following image caption:

"{caption}"

Generate a medical report in this format:
Write a structured radiology report in this format:

Patient Name: John Doe
Age: 42

1. Findings
(Summarize in 3 bullet points max)

2. Diagnosis or Impression
(One-line)

3. Recommendation
(One-line)

4. Disclaimer

Just display the plain text, don't use any markdown or formatting symbols. Keep in mind that in the final report, nothting should be in bold. Do not write anything other 'Here is the report' etc. in the generated report, just display whatever is asked. 
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
