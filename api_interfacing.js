require('dotenv').config()
const crawler = require('crawler-request');
const CKey = process.env['CKey']
const { GoogleGenerativeAI } = require('@google/generative-ai')
const GKey = process.env['GKey']
const genAI = new GoogleGenerativeAI(GKey)
const model = genAI.getGenerativeModel({model: 'gemini-1.5-flash'})

const recentRecords = ( await ( await fetch(`https://api.congress.gov/v3/daily-congressional-record?format=json&limit=10&api_key=${CKey}`) ).json() ).dailyCongressionalRecord

async function getDates() {
  let dates = []
  for (let i = 0; i < recentRecords.length; i++) {
    dates.push(recentRecords[i].issueDate)
  }
  return dates
}

async function createSummary(isoDate) {
  const questionPt1 = 'Within the triple curly braces is an entire day issue for a congressional session:\n{{{'
  const questionPt2 = '}}}\nConsidering a reader with political knowledge equal to or slightly less than the average American, summarize the issue in a concise, informative, impartial, and engaging way, structured with headings. Do not use Markdown, and use formatting tools such as Unicode bullets (do not add bullets to headings), and Unicode bold characters instead. Prioritize proceedings related to law with policy implications, such as bills and resolutions, and specifically list and name the most significant ones with bill numbers. Any non-legal things can be included if space remains. Limit the response to approximately 200 words. Begin your response with "Here\'s a Politibyte for you!\"'
  
  for (let i = 0; i < recentRecords.length; i++) {
    if (recentRecords[i].issueDate == isoDate) {
      url = recentRecords[i].url + `&api_key=${CKey}`
    }
  }
  const r = await fetch(url)
  const session = await r.json()
  const issues = session.issue.fullIssue.entireIssue
  if (issues.length > 1) {
    if (issues[0].type == 'PDF') {
      issue_url = issues[0].url
    } else {
      issue_url = issues[1].url
    }
  } else {
    issue_url = issues[0].url
  }

  pdfText = (await crawler(issue_url)).text
  return (await model.generateContent(questionPt1 + pdfText + questionPt2) ).response.text()
}

module.exports = { getDates, createSummary }