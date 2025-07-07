from utils.DownloadData import *
from parser.resumeParser import *
from scraper.scrape_timesjobs import *
from utils.sendMessages import send_all_jobs
import json
import requests
import time
import os
import time
import uuid

BOT_TOKEN = ''
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

last_update_id = None
job_data = {}
resume = {}



def main():
    global last_update_id
    print("🤖 Bot is running... Waiting for messages.")

    while True:
        updates = get_updates(offset=last_update_id)
        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    user = msg["chat"].get("first_name", "Unknown")
                    if "text" in msg:
                        print(msg["text"])
                        if msg["text"] == "/start":
                            message = f"Hey {user}, Welcome to job finder bot, send your resume so we could search the jobs which matches your resume"
                        elif msg["text"] == "/send_posts":
                            print(f"[DEBUG] Extracting PDF text for chat_id: {chat_id}")
                            extract_pdf_text(f"data/resumes/{chat_id}.pdf")
                            print(f"[DEBUG] Parsing resume for chat_id: {chat_id}")
                            preferred_job_role = parse_resume(chat_id, f"data/resumes/{chat_id}.pdf")
                            print(f"[DEBUG] Parsed resume: {preferred_job_role}")
                            parsed = json.loads(preferred_job_role)
                            print(f"[DEBUG] Preferred job role: {parsed['preferred_job_role']}")
                            print(f"[DEBUG] Scraping jobs for role: {parsed['preferred_job_role']}")
                            jobs = scrape_timesjobs(parsed["preferred_job_role"])
                            job_data[chat_id] = {}
                            for job in jobs:
                                job_id = str(uuid.uuid4())
                                job["id"] = job_id
                                job_data[chat_id][job_id] = job
                            print(job_data)
                            send_all_jobs(chat_id, job_data)
                            print(f"[DEBUG] Jobs found: {len(jobs)} for chat_id: {chat_id}")
                            message = None
                        elif msg["text"] == "/quit":
                            break
                        else:
                            message = response(chat_id, msg["text"])
                        if message:
                            send_to_telegram( message,chat_id)
                    elif "document" in msg:
                        file_id = msg["document"]["file_id"]
                        file_name = msg["document"]["file_name"]
                        resume_path = f"data/resumes/{chat_id}.pdf"
                        print(f"Received file: {file_name} from {user}")
                        resume_path = f"data/resumes/{chat_id}.pdf"
                        if os.path.exists(resume_path):
                            message = f"Thanks {user}, Your resume is updated."
                        else:
                            message = f"Thanks {user}, your resume has been received and processed."

                        download_resume(file_id, chat_id)
                        print(parse_resume(chat_id,resume_path))
                        send_to_telegram(
                            message ,
                            chat_id
                        )
                elif "callback_query" in update:
                    callback = update["callback_query"]
                    chat_id = callback["from"]["id"]
                    message_text = callback["message"]["text"]  # 🔥 This is what you want
                    data = callback["data"]

                    if data.startswith("generate_cover_"):
                # Example: extract job_id if needed
                        job_id = data.replace("generate_cover_", "")

                
                        # resume = get_user_resume(chat_id)
                        cover_letter = generate_cover_letter(resume.get(chat_id, {}),get_job_discription(job_data[chat_id][job_id]["link"]))

                        send_job_with_button(f"📄 Here's your cover letter:\n\n{cover_letter}", chat_id,job_data[chat_id][job_id]["link"])

                        requests.post(f"{API_URL}/answerCallbackQuery", json={
                    "callback_query_id": callback["id"],
                    "text": "✍️ Generating cover letter...",
                    "show_alert": False
                })
        time.sleep(1)

if __name__ == "__main__":
    main()
