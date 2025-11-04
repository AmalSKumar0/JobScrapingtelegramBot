# 🤖 JobScrapingTelegramBot  
### AI-Powered Telegram Bot for Personalized Job Search & Auto Cover Letter Generation  

**Author:** [Amal S Kumar](https://github.com/AmalSKumar0)  
**Tech Stack:** Python · Telegram Bot API · BeautifulSoup · OpenAI API  

---

## 🧭 Overview

**JobScrapingTelegramBot** is an intelligent Telegram assistant that automates the most time-consuming parts of a job search.  

Upload your **resume (PDF)**, and the bot will:  
1. Analyze your skills and experience using AI.  
2. Scrape the web for **relevant job listings**.  
3. Send personalized job matches directly in Telegram.  
4. Allow you to:  
   - 🔗 **View job details** instantly.  
   - ✍️ **Generate a custom AI-powered cover letter** based on your resume and the job description.  

This project combines **AI reasoning**, **web automation**, and **Telegram UX** into one seamless experience.

---

## 🚀 Features

| Feature | Description |
|----------|--------------|
| 🧾 Resume Upload | Users send a PDF resume to the bot. |
| 🧠 AI Resume Analysis | AI extracts job titles, skills, and experience from the PDF. |
| 🔍 Smart Job Scraping | The bot scrapes live job listings from job sites (custom site integration). |
| 💬 Inline Buttons | Each job message includes interactive buttons: “View Job” & “Generate Cover Letter.” |
| ✉️ Cover Letter Generation | AI creates a tailored cover letter using extracted resume data. |
| 💾 Data Storage | Stores user resumes and parsed data locally for re-use. |
| ⚙️ Configurable | Environment variables for API keys, Telegram tokens, and scraper URLs. |

---

## 🏗️ Architecture

```text
       ┌────────────────────────────────────────────────────┐
       │                    Telegram User                   │
       │  (Uploads Resume / Requests Jobs / Generates CL)   │
       └────────────────────────┬───────────────────────────┘
                                │
                                ▼
                ┌────────────────────────────────┐
                │       Telegram Bot Server      │
                │ (python-telegram-bot library)  │
                └──────────────┬─────────────────┘
                               │
             ┌─────────────────┼──────────────────┐
             ▼                 ▼                  ▼
   ┌────────────────┐  ┌────────────────┐  ┌───────────────────────┐
   │  Resume Parser │  │   Job Scraper  │  │       AI Engine       │
   │ (PyMuPDF/PDFPlumber) │ (BeautifulSoup/Requests) │ (OpenAI API) │
   └────────────────┘  └────────────────┘  └───────────────────────┘
             │                 │                  │
             │                 ▼                  │
             └──────────► Local Storage ◄─────────┘
                          (JSON / Files)
````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AmalSKumar0/JobScrapingtelegramBot.git
cd JobScrapingtelegramBot
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` File

Add your credentials in a `.env` file in the project root:

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
JOB_SOURCE_URL=https://example.com/jobs
```

### 5️⃣ Run the Bot

```bash
python main.py
```

---

## 🧰 Example Usage

1. Open your Telegram app and start the bot using `/start`.
2. Upload your **PDF resume**.
3. The bot analyzes your skills and career field.
4. It fetches **live job postings** matching your profile.
5. You’ll receive messages like:

```
💼 Job: Python Developer - Bangalore
🏢 Company: TechNova Solutions
🔗 [View Job]

[Generate Cover Letter]
```

6. Tap **Generate Cover Letter** to receive a fully tailored letter instantly.

---

## 🧠 AI Logic

The AI pipeline uses OpenAI’s API to perform the following:

1. **Resume Understanding:**

   ```text
   "Analyze the following resume and extract skills, roles, and experience in JSON format."
   ```

2. **Job Relevance Ranking:**

   ```text
   "Compare this user's profile to the given job description and rate the match (0-100%)."
   ```

3. **Cover Letter Generation:**

   ```text
   "Write a professional, concise cover letter using this resume data for this job posting."
   ```

Each output is contextually generated using data from the uploaded resume and the specific job link.

---

## 🗂️ Project Structure

```
JobScrapingtelegramBot/
│
├── main.py                # Entry point for the Telegram bot
├── resume_parser.py       # Extracts text and structured data from resume PDFs
├── job_scraper.py         # Scrapes jobs from target job portal
├── ai_utils.py            # Interacts with OpenAI API for analysis & generation
├── data/                  # Stored user resumes and parsed data
├── requirements.txt
├── .env
└── README.md
```

---

## 🔐 Environment Variables

| Variable             | Description                    |
| -------------------- | ------------------------------ |
| `TELEGRAM_BOT_TOKEN` | Token from BotFather           |
| `OPENAI_API_KEY`     | API key for OpenAI GPT models  |
| `JOB_SOURCE_URL`     | Base URL of job site to scrape |

---

## 📈 Future Roadmap

| Milestone              | Description                        | Priority     |
| ---------------------- | ---------------------------------- | ------------ |
| ✅ MVP Bot              | Resume → Jobs → Cover Letter       | High         |
| 🧩 Add DB              | Replace local JSON with PostgreSQL | Medium       |
| 🌍 Multi-Site Scraping | Integrate more job APIs            | High         |
| 💌 Daily Job Digest    | Scheduled job alerts               | Medium       |
| 🧠 Resume Enhancer     | AI suggests improvements           | Medium       |
| 💼 Web Dashboard       | Django/React front-end             | Low          |
| ⚡ Auto Apply           | Smart job form autofill            | Experimental |

---

## 🧑‍💻 Contributing

Contributions are welcome!
If you’d like to add features, fix scraping logic, or improve AI prompts:

1. Fork the repository
2. Create a feature branch
3. Submit a PR with clear commit messages

---

## 🛡️ Disclaimer

* The project is for educational and personal use.
* Scraping job portals may violate their terms of service — ensure compliance with each site’s policy.
* Do not store or share user resumes without consent.

---

## 💬 Author

**👨‍💻 Amal S Kumar**
Full-Stack Developer | AI & Automation Enthusiast
🌐 [GitHub Profile](https://github.com/AmalSKumar0)

