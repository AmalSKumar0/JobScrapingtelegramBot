import requests
import os

BOT_TOKEN = ''
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
FILE_API_URL = f'https://api.telegram.org/file/bot{BOT_TOKEN}'


def send_job_with_button(job_text, chat_id, link):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": job_text,
        "reply_markup": {
            "inline_keyboard": [[
                {
                    "text": "🔗 Apply to this job",
                    "url": link
                }
            ]]
        },
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)



def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    response = requests.get(f"{API_URL}/getUpdates", params=params)
    return response.json()

def get_file_info(updates, target_user_id):
    try:
        messages = updates["result"]
        for msg in reversed(messages):
            if "document" in msg["message"] and msg["message"]["from"]["id"] == target_user_id:
                file_id = msg["message"]["document"]["file_id"]
                return file_id
        print("No document found for this user.")
    except Exception as e:
        print(f"Error extracting file_id: {e}")
    return None

def get_file_path(file_id):
    res = requests.get(f"{API_URL}/getFile?file_id={file_id}")
    return res.json().get("result", {}).get("file_path", None)


def download_file(file_path, user_id):
    if not file_path:
        print("No file path available.")
        return
    file_url = f"{FILE_API_URL}/{file_path}"

    os.makedirs("data/resumes", exist_ok=True)
    save_path = f"data/resumes/{user_id}.pdf"

    res = requests.get(file_url)
    with open(save_path, "wb") as f:
        f.write(res.content)

    print(f"File saved as {save_path}")


def download_resume(file_id, user_id):
    path = get_file_path(file_id)
    if path:
        download_file(path, user_id)
        return True
    return False


def send_to_telegram(message,id):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200




