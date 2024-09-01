<p align="center">
    <img src="./assets/solvro.png">
</p>

# Solvro ML - USOS scraper for PromoCHATor project
<p align="justify">
This repository contains scripts scraping data from USOS for PromoCHATor project in Solvro ML section. These scripts allow to collect data about university teachers, their scientific achievements, abstracts of students' scientific papers. The project will be developed as necessary.
</p>

## Table of contents

1. **[Description](#description)**
2. **[Technologies](#technologies)**
3. **[Development](#development)**
   1. [Quick start](#quick-start)
      - [Setup project locally](#setup-project-locally)
      - [Run usos-teachers-scraper](#run-usos-teachers-scraper)
      - [Run usos-abstracts-scraper](#run-usos-abstracts-scraper)
   2. [Github workflow](#github-workflow)
4. **[Current team](#current-team)**

## Description
<p align="justify"> 
This repository contains scripts scraping data from USOS. These scripts allow to collect data about university teachers, their scientific achievements, abstracts of students' scientific papers.
</p>

## Technologies
Project uses following languages and technologies
* Python 3.9.13

## Development
### Quick start
#### Setup project locally

1. Clone the repository:

   ```
   git clone https://github.com/Solvro/script-promochator-usos-scraper.git
   ```

2. Change directory:

   ```
   cd script-promochator-usos-scraper
   ```

3. Create new virtual environment:

   ```
   python -m venv <your_env_name>
   ```

4. Activate environment:

   ```
   ./venv/Scripts/activate
   ```

5. Install the required modules:

   ```
   python -m pip install -r requirements.txt
   ```

#### Run usos-teachers-scraper

1. Sign up for an API key:

   ```
   https://apps.usos.pwr.edu.pl/developers/
   ```

2. Change directory:

   ```
   cd usos-teachers-scraper
   ```

3. Create a `config.json` file. Then come up with a secret key. Finally, paste your Consumer Key and Consumer Secret:

   ```
   {
    "secret_key": "<your-secret-key>",
    "consumer_key": "<generated-consumer-key>",
    "consumer_secret": "<generated-consumer-secret>"
   }
   ```

4. Run the script:

   ```
   python ./usos-teachers-scraper.py
   ```

5. Visit the USOS authorization page:
   
   ```
   http://127.0.0.1:5000/start_oauth
   ```

6. Fetch teachers data by visiting page:
   ```
   http://127.0.0.1:5000/fetch_staff
   ```

#### Run usos-abstracts-scraper

1. Change directory:

   ```
   cd usos-abstracts-scraper
   ```

2. Optionally, run a text editor, such as vim, and uncomment a few code snippets to enable the HTTP proxy. Remember that it is not recommended due to the security of public proxy data processing.

3. Run the script:

   ```
   python ./usos-abstracts-scraper.py
   ```

4. Input initial thesis id and final thesis id.

### Github workflow

When you had assigned yourself to new task, you should stick to these steps
1. `git checkout main` Check out main branch
2. `git pull origin main` Pull current changes from main branch
3. `git fetch` Be up to date with remote branches
4. `git checkout -b type/task` Create new task branch
5. `git add .` Add all changes we have made
6. `git commit -m "My changes description"` Commit changes with proper description
7. `git push origin type/task` Pushing our changes to remote branch
8. On Github we are going to make Pull Request (PR) from our remote branch
 
> [!WARNING]
> Do not push changes directly to main branch

For further information read Solvro handbook

**Github Solvro Handbook 🔥** - https://docs.google.com/document/d/1Sb5lYqYLnYuecS1Essn3YwietsbuLPCTsTuW0EMpG5o/edit?usp

## Current team
This is our current team
- [@LukiLenkiewicz](https://github.com/LukiLenkiewicz) - Tech Lead
- [@Micz26](https://github.com/Micz26) - ML Engineer
- [@farqlia](https://github.com/farqlia) - ML Engineer
- [@AgataGro](https://github.com/AgataGro) - ML Engineer
- [@dekompot](https://github.com/dekompot) - ML Engineer
- [@b4rt4s](https://github.com/b4rt4s) - ML Engineer
- [@Woleek](https://github.com/Woleek) - ML Engineer
- [@WiktoriaFrost](https://github.com/WiktoriaFrost) - ML Engineer
- [@Barionetta](https://github.com/Barionetta) - Project Manager
