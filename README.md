# Solvro ML - USOS scraper for PromoCHATor project
Description TBA

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
   .\venv\Scripts\activate
   ```

5. Install the required modules:

   ```
   python -m pip install -r requirements.txt
   ```

#### Run usos-teachers-scraper

1. Sign up for an API key:

   ```
   https://apps.usos.pwr.edu.pl/developers/`
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
   http://localhost:5000/start_oauth
   ```

6. Fetch teachers data by visiting page:
   ```
   http://localhost:5000/fetch_staff`
   ```
