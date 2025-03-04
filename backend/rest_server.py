#################### OUTSIDE API HANDLING #########################

import os
import requests
from io import BytesIO
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

CKEY = os.getenv('CKEY')
GKEY = os.getenv('GKEY')
genai.configure(api_key=GKEY)
model = genai.GenerativeModel("gemini-1.5-flash-8b")

summary_cache = {}

def get_recent_records():
    return requests.get(f'https://api.congress.gov/v3/daily-congressional-record?format=json&limit=10&api_key={CKEY}').json()['dailyCongressionalRecord']

def get_dates():
    global recent_records
    recent_records = get_recent_records()
    dates = []
    for record in recent_records:
        dates.append(record['issueDate'][:10])
    return dates

def update_cache(dates):
    # Remove outdated summaries
    for cached_date in list(summary_cache.keys()):
        if cached_date not in dates:
            del summary_cache[cached_date]
    # Add missing summaries
    for date in dates:
        if date not in summary_cache:
            summary_cache[date] = get_summary(date)

Q_PT1 = 'Within the triple curly braces is an entire day issue for a congressional session:\n{{{'
Q_PT2 = '}}}\nConsidering a reader with political knowledge equal to or slightly less than the average American, summarize the issue in a concise, informative, impartial, and engaging way. Structure the response in a way that is appropriate for one single paragraph of text without line breaks. Do not use Markdown, and use formatting tools such as Unicode bullets (do not add bullets to headings), and Unicode bold characters instead. Prioritize proceedings related to law with policy implications, such as bills and resolutions, and specifically list and name the most significant ones with bill numbers. Any non-legal things can be included if space remains. Limit the response to approximately 250-300 words. Begin your response with "Here\'s a Politibite for you!\"'
def get_summary(date):
    global recent_records
    for record in recent_records:
        if record['issueDate'][:10] == date:
            url = record['url'] + f'&api_key={CKEY}'
            all_issues = requests.get(url).json()['issue']['fullIssue']['entireIssue']
    if len(all_issues) > 1:
        if all_issues[0]['type'] == 'PDF':
            issue_url = all_issues[0]['url']
        else:
            issue_url = all_issues[1]['url']
    else:
        issue_url = all_issues[0]['url']
    
    r = requests.get(issue_url)
    reader = PdfReader(BytesIO(r.content))
    full_text = ''
    for page in reader.pages:
        full_text += page.extract_text()

    return model.generate_content(Q_PT1 + full_text + Q_PT2).text


recent_records = get_recent_records()
update_cache(get_dates())

#################### BACKEND REST API #########################

from typing import Union
from fastapi import FastAPI, APIRouter, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(redoc_url=None)
router = APIRouter(prefix='/api')

@router.get('/get_dates/')
def return_dates(background_tasks: BackgroundTasks):
    dates = get_dates()  #Fetch and return dates immediately
    background_tasks.add_task(update_cache, dates)  #Run cache update in the background
    return {'date_list': dates}

@router.get('/get_summary/{ISOSTRING}')
def return_summary(ISOSTRING: str):
    if ISOSTRING in summary_cache:
        summary = summary_cache[ISOSTRING]
    else:
        summary = get_summary(ISOSTRING)
        summary_cache[ISOSTRING] = summary  # Cache it for future use
    return {'summary': summary.split('\n')}

app.include_router(router)
