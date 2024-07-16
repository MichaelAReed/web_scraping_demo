# Web Scraping Demo

This repo contains a setup to demonstrate web scraping in python using:
* beautifulsoup4
* Selenium

Web scraping is an automated extraction of information from a website that does not have accessible APIs to directly connect to the data you want. In this situation we must work with the interface designed for users on a website.

# Setup

This project uses a devcontainer with docker compose that sets up a docker for Selenium chrome and a hub to connect through to it. The devcontainer also contains some purely developer experience features such as a custom zsh config.

It is recommended that you first have docker installed and use vscode to open this project. If you install (or have installed) the devcontainer extension, you will receive a popup notification that you can open the project inside a container. Doing so will setup the Selenium server, install the necessary python libraries as well as the typing, formatting, linting and testing libraries the project uses. These will also be automatically connected to vscode to automatically provide highlighting of style 'problems' as well as auto-formatting etc.

# beautifulsoup4

beautifulsoup4 is a popular, open source and well understood python library for parsing and extracting data from html. It is very fast and lightweight so it is the ideal choice if the website you are trying to scrape returns raw html. However many websites now use Javascript to modify the html of the website after the initial page request. This makes it much more difficult to use an html parser like beautifulsoup4 - you must instead first run the javascript just like a browser, wait for changes and then try to extract your data.

# Selenium

Selenium is a popular, open source and well understood tool for automating browser tasks by using a target browser (eg. Chrome) to render and interact with a webpage just as a user would. The benefit of this is that it provides as close as possible parity to real user interaction. This allows you to automate processes that require lots of javascript and live loading but also allows you to test your own web projects to discover issues that real users would encounter.

You can use Selenium just as a python library that makes use of your machine's native browser. But because we wanted this project to be as portable and easy to setup as possible, we used a Selenium maintained Docker image for running the browser that Selenium uses for its automation. This is a very useful boilerplate for web project testing but is maybe less necessary for general web scraping projects where repeatability isn't as fundamental.