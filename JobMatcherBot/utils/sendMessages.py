import requests
import os
from utils.DownloadData import send_to_telegram

BOT_TOKEN = ''
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


def send_all_jobs(chat_id,job_data):
    if chat_id not in job_data or not job_data[chat_id]:
        send_to_telegram("No jobs found for you at the moment.", chat_id)
        return

    for job_id, job in job_data[chat_id].items():
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        location = job.get("location", "Not specified")
        experience = job.get("experience", "Not specified")
        skills = ", ".join(job.get("skills", [])) or "Not specified"
        link = job.get("link", "#")

        message = f"""📌 *{title}*
🏢 *Company:* {company}
📍 *Location:* {location}
🕓 *Experience:* {experience}
🛠️ *Skills:* {skills}
"""

        # Send message with buttons
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "📄 Generate Cover Letter", "callback_data": f"generate_cover_{job_id}"},
                        {"text": "🔗 Open Job", "url": link}
                    ]
                ]
            }
        }
        requests.post(f"{API_URL}/sendMessage", json=payload)


    

