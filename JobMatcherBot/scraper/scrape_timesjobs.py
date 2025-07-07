import requests
from bs4 import BeautifulSoup

def scrape_timesjobs(query="python"):
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={query}&txtLocation="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch job listings.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

    jobs = []

    for card in job_cards:
        try:
            title_tag = card.find("h2")
            job_title = title_tag.text.strip()
            job_link = title_tag.find("a")["href"]

            company = card.find("h3", class_="joblist-comp-name").text.strip().replace("(More Jobs)", "").strip()

            # Experience and location
            details = card.find("ul", class_="top-jd-dtl clearfix")
            spans = details.find_all("span") if details else []
            location = spans[0].text.strip() if len(spans) > 0 else "Not specified"
            experience = spans[1].text.strip() if len(spans) > 1 else "Not specified"

            # Skills
            skills_tag = card.find("span", class_="srp-skills")
            skills = [s.strip() for s in skills_tag.text.strip().split(",")] if skills_tag else []

            jobs.append({
                "title": job_title,
                "company": company,
                "link": job_link,
                "location": location,
                "experience": experience,
                "skills": skills,
                "description": "Visit link for details"
            })

        except Exception as e:
            print(f"⚠️ Error parsing job: {e}")
            continue

    return jobs

def get_job_discription(job_link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(job_link, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch job description.")
        return "No description available."

    soup = BeautifulSoup(response.text, "html.parser")
    description_tag = soup.find("div", class_="jd-desc job-description-main")
    return description_tag.text.strip() if description_tag else "No description available."


