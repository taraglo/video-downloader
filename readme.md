# HQporner and Eporner Video Downloader

### Introduction
The python script in `main.py` downloads multiple videos concurrently from [hqporner.com](https://hqporner.com) and [eporner.com](https://www.eporner.com).
The program is built using asyncio, aiohttp and selenium with Firefox webdriver. If you wish to change the browser, update configurations from `line 75` to `line 84` in `main.py`.
If you change the webdriver variable name, make sure to change in other places throughout the code.

### Usage
1. Install python 3.10 or whichever version works.  
2. Update config values in `settings.py` file.  
3. Install all the required packages in `requirements.txt` file.  
4. List all the videos links you want to download from in `urls.txt` file.
5. Run `python3 main.py` to start the download process.

---
Coded by [taraglo](https://www.github.com/taraglo) on GitHub