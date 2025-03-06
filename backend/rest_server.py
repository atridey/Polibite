#################### OUTSIDE API HANDLING #########################

import os
import requests
from io import BytesIO
from pypdf import PdfReader
CKEY = os.getenv('CKEY')

import google.generativeai as genai
GKEY = os.getenv('GKEY')
genai.configure(api_key=GKEY)
model = genai.GenerativeModel("gemini-1.5-flash-8b")

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(json.loads(FIREBASE_CREDENTIALS))
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_recent_records():
    return requests.get(f'https://api.congress.gov/v3/daily-congressional-record?format=json&limit=10&api_key={CKEY}').json()['dailyCongressionalRecord']

def get_dates():
    recent_records = get_recent_records()
    dates = []
    for record in recent_records:
        dates.append(record['issueDate'][:10])
    #purge_cache(dates)
    return dates

#Not currently in use
def purge_cache(dates):
    cache = db.collection("summary_cache")
    for entry in cache.stream():
        date = list(entry.to_dict().keys())[0]
        if date not in dates:
            cache.document(date).delete()

Q_PT1 = 'Within the triple curly braces is an entire day issue for a congressional session:\n{{{'
Q_PT2 = '}}}\nConsidering a reader with political knowledge equal to or slightly less than the average American, summarize the issue in a concise, informative, impartial, and engaging way. Structure the response in a way that is appropriate for one single paragraph of text. Do not use Markdown, and use formatting tools such as Unicode bullets (do not add bullets to headings) or Unicode bold characters instead. Use paragraph breaks when necessary (with a blank space in between), and ensure that any and all line breaks are represented with HTML <br> tags (NOT \'\\n\') and not actual line breaks in the outputted string. Prioritize proceedings related to law with policy implications, such as bills and resolutions, and specifically list and name the most significant ones with bill numbers. Any non-legal things can be included if space remains. Limit the response to approximately 250-300 words. Begin your response with \"Here\'s a Polibite for you!\"'
def get_summary(date):
    cached = db.collection("summary_cache").document(date)
    if cached.get().exists:
        return cached.get().to_dict()['summary']
    else:
        recent_records = get_recent_records()
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

        summary = model.generate_content(Q_PT1 + full_text + Q_PT2).text
        cached.set({'summary': summary})
        return summary

#################### BACKEND REST API #########################

from typing import Union
from fastapi import FastAPI, APIRouter, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(redoc_url=None)
router = APIRouter(prefix='/api')

@router.get('/get_dates/')
def return_dates():
    dates = get_dates()
    return {'date_list': dates}

@router.get('/get_summary/{ISOSTRING}')
def return_summary(ISOSTRING: str):
    summary = get_summary(ISOSTRING)
    return {'summary': summary}

app.include_router(router)
