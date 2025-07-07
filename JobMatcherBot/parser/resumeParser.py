from pdfminer.high_level import extract_text
from openai import OpenAI
from collections import defaultdict

client = OpenAI(
    api_key="",
    base_url="https://api.groq.com/openai/v1"
)  

conversations = defaultdict(list)

def extractdata(chat_id,text):
    prompt = f"""
You are an intelligent resume parser AI.

Given the following raw resume text, extract and return the following fields:

1. Full Name
2. Preferred Job Role (if mentioned or can be inferred)
3. Skills (as a comma-separated list)
4. Total Experience (in years, or approximate if not exact, need integer value)
5. dont add any extra information, just return the JSON object with the fields mentioned above.
6. if this is not a resume, return False.

Respond only in valid JSON format, like this:

{{
  "name": "...",
  "preferred_job_role": "...",
  "skills": ["...", "..."],
  "total_experience": "..."
}}

Resume Text:
\"\"\"
{text}
\"\"\"
"""


    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    parsed_result = response.choices[0].message.content.strip()

    resume_prefix = "User's resume profile:"
    found = False
    for msg in conversations[chat_id]:
        if msg["role"] == "system" and msg["content"].startswith(resume_prefix):
            msg["content"] = f"{resume_prefix}\n{parsed_result}"
            found = True
            break
    if not found:
        conversations[chat_id].insert(0, {
            "role": "system",
            "content": f"{resume_prefix}\n{parsed_result}"
        })

    return parsed_result



def extract_pdf_text(file_path):
    try:
        return extract_text(file_path)
    except Exception as e:
        print("Error reading PDF:", e)
        return ""


def parse_resume(chat_id,file_path):
    raw_text = extractdata(chat_id,extract_pdf_text(file_path))
    return raw_text


def response(chat_id, user_input):
    conversations[chat_id].append({"role": "user", "content": user_input})
    if len(conversations[chat_id]) > 6:
        conversations[chat_id] = conversations[chat_id][-6:]

    system_message = {
        "role": "system",
        "content": "you are a webscraping bot that takes in resume and scans through job portal, a user will as question and you have to help him, word limit of 30 and dont give job opening details, be friendly and talk like a girl and use emojis"
    }

    messages = [system_message] + conversations[chat_id]
    print(messages)


    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.7,
    )

    reply = completion.choices[0].message.content.strip()


    conversations[chat_id].append({"role": "assistant", "content": reply})

    return reply


#add resume data to the chat ai 

def generate_cover_letter(resume_data, job_description):
    prompt = f"""You are an expert cover letter writer. Given the user's resume data and the job description, generate a personalized cover letter. resume data: {resume_data} job description: {job_description}"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
    )
    cover_letter = response.choices[0].message.content.strip()
    return cover_letter