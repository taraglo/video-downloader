import requests
import ssl
import re
import time
import asyncio
import aiohttp
from settings import *
from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

time_1 = time.perf_counter()


@dataclass
class DownloadParams:
    url: str
    model: str
    title: str


ff_driver = None
browser_needed = False
failed_downloads = []
server_dnld_urls = []
urls = []
with open("urls.txt", encoding='utf-8') as file:
    for line in file:
        urls.append(line)
        if "hqporner" in line:
            browser_needed = True


def format_name(file_name: str) -> str:
    filter_chars = [',', '/', ';', '-']
    filter_expressions = ['\\', '?', '!', ':', '\'']
    file_types = {".mp4", ".jpg", ".png"}

    file_name = file_name.lower()

    # Replace filter characters with spaces
    table = str.maketrans({char: ' ' for char in filter_chars})
    file_name = file_name.translate(table)

    # Remove filter expressions
    table = str.maketrans({char: '' for char in filter_expressions})
    file_name = file_name.translate(table)

    words = file_name.split()
    formatted_name = words[0]

    for word in words[1:]:
        if word in file_types:
            formatted_name += f" {word}"
        else:
            formatted_name += f"-{word}"

    return formatted_name


def format_time(time_in_seconds: float) -> str:
    hours, remainder = divmod(time_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours >= 1:
        time_string = f"{int(hours):02} hrs {int(minutes):02} min {int(seconds):02} sec"
    elif minutes >= 1:
        time_string = f"{int(minutes)} min {int(seconds)} sec"
    else:
        time_string = f"{seconds:.2f} seconds"
    return time_string


if browser_needed:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    firefox_profile = Options()
    # firefox_profile.add_argument("--headless")
    # firefox_profile.add_argument("--window - size = 1920, 1080")
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    ff_driver = webdriver.Firefox(options=firefox_profile)
    # ff_driver.minimize_window()

for a in range(0, len(urls)):
    html = requests.get(urls[a])                  # go to website page
    bs = BeautifulSoup(html.text, 'html.parser')  # retrieve html source code

    if "eporner.com" in urls[a]:
        try:
            videos = bs.find_all('a', {'href': re.compile('1440p.mp4')})
            if len(videos) == 0:
                videos = bs.find_all('a', {'href': re.compile('1080p.mp4')})
            pornstars = bs.find_all('li', {'class': re.compile('vit-pornstar starw')})

            if len(pornstars) > 0:
                pornstar_names = pornstars[0].get_text()
            else:
                pornstar_names = "_"

            download_url = "https://eporner.com" + videos[0].attrs['href']
            video_info = bs.find_all('div', {'id': 'video-info'})[0]
            video_title_arr = video_info.find_all('h1')[0].get_text().split(" ")
            video_title = ""
            for x in range(0, len(video_title_arr) - 1):
                video_title += " " + video_title_arr[x]

            server_dnld_urls.append(DownloadParams(download_url, pornstar_names, video_title))

        except Exception as e:
            failed_downloads.append(urls[a].replace("\r\n", "").replace('\n', ''))
            print(str(a+1) + ". Error: " + str(e))

    elif "hqporner.com" in urls[a]:
        error = bs.find_all('section', {'class': 'box highlight'})

        if len(error) > 0:
            search_query = urls[a].replace("https://hqporner.com/hdporn/", "")
            search_query = search_query[6:-5].replace("_", "+").replace("-", "+")

            ff_driver.get("https://hqporner.com/?q=" + search_query)

            search_results = BeautifulSoup(ff_driver.page_source, 'html.parser').find_all('a', {'class': 'non-overlay'})
            if len(search_results) > 1:
                print(str(a+1) + ". Found multiple videos.")
                compare_words = search_query[6:-5].split("+")
                for video_index in range(0, len(search_results)):
                    matched_words = 0
                    for word in compare_words:
                        if word.lower() in search_results[video_index].attrs['href'].lower():
                            matched_words += 1
                    if matched_words > 0:
                        print("   " + str(video_index) + ". " + search_results[video_index].attrs['href'])
                vid_index = int(input("Select a video to continue, or enter 69 to ignore: "))

                if vid_index == 69:
                    failed_downloads.append(urls[a].replace("\r\n", "").replace('\n', ''))
                    continue
                else:
                    ff_driver.find_element(By.XPATH, "//a[@class='image featured non-overlay atfib' and @href='" + search_results[vid_index].attrs['href'] + "']").click()

            else:
                ff_driver.find_element(By.CLASS_NAME, "non-overlay").click()

            ff_driver.implicitly_wait(1)
            html_source = ff_driver.page_source

            try:
                iframe = BeautifulSoup(html_source, 'html.parser').find_all('iframe', {'src': re.compile("mydaddy.cc")})

                video_title = BeautifulSoup(html_source, 'html.parser').find_all('h1', {'class': 'main-h1'})
                video_title = video_title[0].get_text().replace("\r\n", "").replace("\n", "")
                pornstars = BeautifulSoup(html_source, 'html.parser').find_all('li', {'class': 'icon fa-star-o'})
                pornstar_names = pornstars[0].getText().replace("featuring ", "").replace(",", " and")

                source = iframe[0].attrs['src']
                source = "https:" + source           # iframe video url
                ff_driver.get(source)                # open iframe in browser
                ff_driver.implicitly_wait(2)         # wait
                html_source = ff_driver.page_source  # get page source
                videos = BeautifulSoup(html_source, 'html.parser').find_all("source", {'src': re.compile("1080.mp4")})
                download_url = "https:" + videos[len(videos) - 1]['src']

                server_dnld_urls.append(DownloadParams(download_url, pornstar_names, video_title))

            except Exception as e:
                failed_downloads.append(urls[a].replace("\r\n", "").replace('\n', ''))
                print(str(a+1) + ". Error: " + str(e))

        else:
            try:
                iframe = bs.find_all('iframe', {'src': re.compile("//mydaddy.cc/video/")})

                video_title = bs.find_all('h1', {'class': 'main-h1'})[0].get_text().replace("\r\n", "")
                pornstars = bs.find_all('li', {'class': 'icon fa-star-o'})
                pornstar_names = pornstars[0].getText().replace("featuring ", "").replace(",", " and")

                source = iframe[0].attrs['src']
                source = "https:" + source           # iframe video url
                ff_driver.get(source)                # open iframe in browser
                ff_driver.implicitly_wait(1)         # wait
                html_source = ff_driver.page_source  # get page source
                videos = BeautifulSoup(html_source, 'html.parser').find_all("source", {'src': re.compile("1080.mp4")})
                download_url = "https:" + videos[len(videos) - 1]['src']

                server_dnld_urls.append(DownloadParams(download_url, pornstar_names, video_title))

            except Exception as e:
                failed_downloads.append(urls[a].replace("\r\n", "").replace('\n', ''))
                print(str(a+1) + ". Error: " + str(e))

    else:
        print("Invalid URL: " + urls[a])

if ff_driver is not None:
    ff_driver.quit()


async def download(session: aiohttp.ClientSession, params: DownloadParams, index: int):
    if params.model in params.title:  # to-do: fix extra underscore at the beginning of name
        filename = format_name(params.model + "_" + params.title.replace(params.model, "") + ".mp4")
    else:
        filename = format_name(params.model + "_" + params.title + ".mp4")

    print(str(index + 1) + ". Downloading... " + filename)

    time_start = time.perf_counter()

    async with session.get(params.url, timeout=3600) as response:
        with open(save_directory + filename, 'wb') as f:
            while True:
                chunk = await response.content.read(1024*1024)
                if not chunk:
                    break
                f.write(chunk)

    time_end = time.perf_counter()
    time_passed = time_end - time_start
    display_string = "   Download completed (" + str(index + 1) + ") in " + str(format_time(time_passed))
    if index >= 9:
        display_string = "    Download completed (" + str(index + 1) + ") in " + str(format_time(time_passed))
    print(display_string)


async def download_from_queue(queue, session):
    while True:
        url, counter = await queue.get()
        await download(session, url, counter)
        queue.task_done()


async def download_all(url_list):
    async with aiohttp.ClientSession() as session:
        counter = 0
        tasks = []
        queue = asyncio.Queue()
        for url in url_list:
            queue.put_nowait((url, counter))
            counter += 1

        for i in range(max_concurrent_downloads):
            task = asyncio.create_task(download_from_queue(queue, session))
            tasks.append(task)

        await queue.join()
        for task in tasks:
            task.cancel()


if __name__ == '__main__':
    asyncio.run(download_all(server_dnld_urls))

    if len(failed_downloads) > 0:
        print('\nFailed video downloads:')
        for item in failed_downloads:
            print(item)
    else:
        print('\nAll videos downloaded successfully.')

    time_2 = time.perf_counter()
    time_3 = time_2 - time_1
    print("Process finished in " + format_time(time_3))
