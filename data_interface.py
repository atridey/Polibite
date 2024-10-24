import os
import requests
from io import BytesIO
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
CKEY = os.getenv('CKEY')
GKEY = os.getenv('GKEY')
recent_records = requests.get(f'https://api.congress.gov/v3/daily-congressional-record?format=json&limit=25&api_key={CKEY}').json()['dailyCongressionalRecord']
def get_dates():
    dates = []
    for record in recent_records:
        dates.append(record['issueDate'][:10])
    return dates

Q_PT1 = 'Within the triple curly braces is an entire day issue for a congressional session:\n{{{'
Q_PT2 = '}}}\nConsidering a reader with political knowledge equal to or slightly less than the average American, summarize the issue in a concise, informative, impartial, and engaging way, structured with headings. Do not use Markdown, and use formatting tools such as Unicode bullets (do not add bullets to headings), and Unicode bold characters instead. Prioritize proceedings related to law with policy implications, such as bills and resolutions, and specifically list and name the most significant ones with bill numbers. Any non-legal things can be included if space remains. Limit the response to approximately 200 words. Begin your response with "Here\'s a Politibyte for you!\"'
def get_summary(date):
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

    genai.configure(api_key=GKEY)
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    return model.generate_content(Q_PT1 + full_text + Q_PT2).text

#dates = get_dates()
#print(get_summary(dates[0]))