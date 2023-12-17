# HQporner and Eporner Bulk Video Downloader

### Introduction
The python script in `main.py` downloads multiple videos concurrently from [hqporner.com](https://hqporner.com) and [eporner.com](https://www.eporner.com).
The program is built using asyncio, aiohttp and selenium with Firefox webdriver. If you wish to change the browser, update configurations from `line 84` to `line 92` in `main.py`.
If you change the webdriver variable name, make sure to change in other places throughout the code.

### Usage
1. Install python 3.12 or whichever version works.  
2. Update config values in `settings.py` file.  
3. Install all the required packages in `requirements.txt` file by running:  
   ```
   pip3 install -r requirements.txt
   ```
5. List all the video links you want to download from in `urls.txt` file.
6. Run `python3 main.py` to start the download process.

---
Coded by [taraglo](https://www.github.com/taraglo) on GitHub
