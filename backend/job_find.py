import requests
from bs4 import BeautifulSoup
import math
import os
from dotenv import load_dotenv


load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")
adzuna_country = "in"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


def get_jobs_from_adzuna(job_title):
    url = f"https://api.adzuna.com/v1/api/jobs/{adzuna_country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": job_title,
        "where": "India",
        "results_per_page": 5,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)
    data = response.json()
    jobs = []

    for job in data.get("results", [])[:5]:
        jobs.append({
            "company": job.get("company", {}).get("display_name"),
            "job_title": job.get("title"),
            "job_link": job.get("redirect_url")
        })

    return jobs


def get_jobs_from_linkedin(job_title):
    job_title_encoded = job_title.replace(" ", "%20")
    location_encoded = "India".replace(" ", "%20")
    search_url = (
        f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        f"?keywords={job_title_encoded}&location={location_encoded}"
    )

    job_ids = []
    for i in range(0, math.ceil(50 / 25)):
        res = requests.get(f"{search_url}&start={i * 25}", headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        all_jobs = soup.find_all("li")
        for job in all_jobs:
            if len(job_ids) >= 5:
                break
            try:
                job_id = job.find("div", {"class": "base-card"}).get("data-entity-urn").split(":")[3]
                job_ids.append(job_id)
            except:
                continue
        if len(job_ids) >= 5:
            break

    jobs = []
    for job_id in job_ids:
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        resp = requests.get(job_url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            company = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get("alt")
        except:
            company = None

        try:
            title = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
        except:
            title = None

        job_data = {
            "company": company,
            "job_title": title,
            "job_link": f"https://www.linkedin.com/jobs/view/{job_id}/"
        }
        jobs.append(job_data)

    return jobs


def search_jobs(job_title):
    print(f"🔍 Searching for '{job_title}' jobs in India from Adzuna and LinkedIn...\n")
    adzuna_jobs = get_jobs_from_adzuna(job_title)
    linkedin_jobs = get_jobs_from_linkedin(job_title)

    all_jobs = adzuna_jobs + linkedin_jobs
    return all_jobs
