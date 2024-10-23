<h1 align="center">Polibite</h1><p align="center">
<h3 align="center">A bite of Capitol Hill, just for you!</h3><p align="center">
<p align="center">
  <div style="display: flex; justify-content: center; align-items: center;">
    <img src="https://cdn.discordapp.com/attachments/777961961576071169/1298437204497928243/logo.png?ex=67198f61&is=67183de1&hm=9bb31f6d1320f8e06bd5f7292ac8fccbd2f1af4509b297eaff513ab91cffca89&" width="232" height="238" alt="Polibite Logo"/>
  </div>
</p>

It's important to stay up-to-date on politics, but the government can get confusing. Polibite is here to help! Using [officially-sourced](https://github.com/LibraryOfCongress/api.congress.gov/) Congressional Records from the last 10 days, Polibite uses Google's [Gemini](https://github.com/google-gemini) generative AI to cut through the jargon and help you understand the latest developments in politics.

### Dependencies
```
polibite@1.0.0
├── @google/generative-ai@0.21.0
├── crawler-request@1.2.2
└── dotenv@16.4.5
```

### Setup and installation
* Run `npm install` to install all dependencies from `package.json`
* Set up a `.env` file with `CKEY` and `GKEY` environment variables corresponding to your Congress and Gemini API keys, respectively.
* **FRONTEND STEPS TO BE ADDED**

### Developers
* [Atri Dey](https://github.com/atride) - AI integration, API interfacing, and repository maintenance
* [Joshua Ko](https://github.com/Joshua-Ko7) - Web development and graphic design   

### Acknowledgements
* Anthony Egan - Initial brainstorming assistance
* Congressional App Challenge Volunteers - Making this competition possible!
