# Dockerized Dividend Web Scraping with Selenium

This repository contains a Dockerized Python template for scraping data from websites using Selenium
The example website here is Yahoo Finance where we're looking for scraping the dividends of a list of companies

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Prerequisites

Requirements for the software and other tools to build, test and push 
- [Selenium](https://www.selenium.dev/)
- [pytest](https://docs.pytest.org/en/stable/)
- [Poetry](https://python-poetry.org/)
- [Github CLI](https://cli.github.com/)

## Insallation

* First we'll need to pull the selenium/standalone docker image in order to run the remote webdriver
`docker pull --platform linux/x86_64 selenium/standalone-chrome`

* Then build the project's container :
`docker build -t dockerized-webscraper .`

* Once the images are built, we can run the image containers :
    * Minimalistically : `docker run -v /dev/shm:/dev/shm selenium/standalone-chrome`
    * Detached mode : `docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome`

* To run the webscraper interactively : 
`docker run -it dockerized-webscraper`

* Launch the webscraper : 
`python webscraper/yahoo_finance_scrape.py`

* Get the scraped dividends : 
`cat actions_dividends.csv`

## Stop & cleaning

* To stop the containers :
`docker stop selenium/standalone-chrome`

* To remove any non-running container :
`docker rm -f (container id)`

* To check all running containers are removed :
`docker ps -a`

* To check the built Docker images :
`docker images`

## Versioning

We use [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/PurpleBooth/a-good-readme-template/tags).

## Acknowledgments

Feel free to use this template for your own projects and comment this repository if you have any suggestions.
