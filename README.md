<h1 align="center">Polibite</h1><p align="center">
<h3 align="center">A bite of Capitol Hill, just for you!</h3><p align="center">
<p align="center">
  <div style="display: flex; justify-content: center; align-items: center;">
    <img src="https://repository-images.githubusercontent.com/876954395/e868085c-e19b-428d-9004-35c7014efd01" width="232" height="238" alt="Polibite Logo"/>
  </div>
</p>

It's important to stay up-to-date on politics, but the government can get confusing. Polibite is here to help! Using [officially-sourced](https://github.com/LibraryOfCongress/api.congress.gov/) Congressional Records from the last 10 days, Polibite uses Google's [Gemini](https://github.com/google-gemini) generative AI to cut through the jargon and help you understand the latest developments in politics.

### Server setup
* `cd server_side`
* (Recommended) Run `py -m venv .venv` to set up a virtual environment
  * Windows: Start the virtual environment with `.venv\Scripts\activate`
  * Mac/Unix: `./venv/bin/activate`
* Run `pip install -r requirements.txt` to install all dependencies from `requirements.txt`
* Set up a `.env` file with `CKEY` and `GKEY` environment variables corresponding to your Congress and Gemini API keys, respectively.
* Start the server! Run `fastapi run rest_server.py`

### Developers
* [Atri Dey](https://github.com/atride) - AI integration, API interfacing, backend, and repository maintenance
* [Joshua Ko](https://github.com/Joshua-Ko7) - Web development, graphic design  
* Anthony Egan - Backend integration

Thank you to Congressional App Challenge Volunteers for making this competition possible!
