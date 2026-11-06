# Dockerized Dividend Web Scraper

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.27-43B02A?style=flat-square&logo=selenium&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)

A containerised **Selenium** scraper that collects the **full dividend history** of a list of listed companies from Yahoo Finance and exports it to CSV. It runs anywhere Docker runs: the browser lives in its own container (`selenium/standalone-chrome`) and the scraper drives it through a **Remote WebDriver**.

## How it works

```
┌────────────────────────┐   Remote WebDriver   ┌──────────────────────────────┐
│ dockerized-webscraper  │ ───────────────────▶ │ selenium/standalone-chrome   │
│ Python · Selenium ·    │      :4444/wd/hub    │ headless Chrome              │
│ pandas                 │                      └──────────────┬───────────────┘
└──────────┬─────────────┘                                     │
           │ actions_dividends.csv                             ▼
           ▼                                          finance.yahoo.com
   shared_data volume
```

For each ticker, the scraper:
1. opens the dividend history page in headless Chrome and accepts the cookie banner,
2. waits for the table to load, then extracts the date, dividend amount and company name,
3. concatenates every company into a single pandas DataFrame and writes `actions_dividends.csv`.

Default tickers: `ZURN.SW`, `SCMN.SW`, `RMS.PA`, `V`, `BLK`, `SLHN.SW` (edit the list in `webscraping/yahoo_finance_scrape.py`).

## Getting started

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/).

```bash
# 1. Pull the browser image and build the scraper image
docker pull --platform linux/x86_64 selenium/standalone-chrome
docker build -t dockerized-webscraper .

# 2. Create a volume to keep the results
docker volume create shared_data

# 3. Start the browser (shares the host's /dev/shm so Chrome has enough memory)
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome

# 4. Run the scraper interactively
docker run -v shared_data:/data -it dockerized-webscraper
python webscraping/yahoo_finance_scrape.py
cat actions_dividends.csv
```

> The scraper reaches the browser at `http://172.17.0.2:4444/wd/hub`, the default IP of the first container on Docker's bridge network. Update it in `yahoo_finance_scrape.py` if your Selenium container gets a different address.

### Local development

Dependencies are managed with [Poetry](https://python-poetry.org/) (`poetry install`); `requirements.txt` is used for the Docker image.

### Clean up

```bash
docker ps                      # find the container IDs
docker stop <container_id>
docker rm <container_id>
docker rmi selenium/standalone-chrome dockerized-webscraper
```

## Notes

- Yahoo Finance changes its CSS class names from time to time; if the company name is no longer found, update the selector in `yahoo_finance_scrape.py`.
- The pipelined, multi-container version of this project lives in [Multi-stage-dividend-pipeline](https://github.com/rbgt/Multi-stage-dividend-pipeline).
