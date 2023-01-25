# Python code to scrape specific news websites Welt, Sueddeutsche and FAZ

# Note: Timeout is not set, so it will retry the request until it establishes an connection. Timeout can be set as a variable in the request. Furthermore the expect is kept generel which is bad practice, but should work
# here since most errors will be based on connection issues. Should be specified in the future though. An estimate can be implemented, since it will take around 4 seconds per url to make sure that there are not to many requests
# to the websites in a short amount of time.
#
# Important: This script looks for an url in the 6th column of an excel file with headers.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import unicodedata
import re
from datetime import datetime
import locale

url_collection = pd.read_excel("") # input URL

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Cookie': None
}

# Filter URL

# create a boolean mask to filter the DataFrame
sued = url_collection[url_collection.columns[5]].str.contains("sueddeutsche.de", flags=re.IGNORECASE)
welt = url_collection[url_collection.columns[5]].str.contains("welt.de", flags=re.IGNORECASE)
faz = url_collection[url_collection.columns[5]].str.contains("faz.net", flags=re.IGNORECASE)

# use the boolean mask to filter the DataFrame
url_collection_sued = url_collection[sued]
url_collection_welt = url_collection[welt]
url_collection_faz = url_collection[faz]

length_all = len(url_collection)

data_list = []

link_base_sued = "https://www.sueddeutsche.de"


print(f"Total links in collection: {length_all}")
print(f"Total links after applied filter for FAZ.de, welt.de and sueddeutsche.de: {len(url_collection_sued) + len(url_collection_faz) + len(url_collection_welt)}")

if length_all == len(url_collection_sued) + len(url_collection_faz) + len(url_collection_welt):
    print(f"Scraping {length_all} links")
    count = 1
    length_sued = len(url_collection_sued)
    for URL in url_collection_sued[url_collection_sued.columns[5]]:
        print(f"Scraping sueddeutsche.de link {count} from {length_sued}")
        count = count + 1
        while True:
            try:
                r = requests.get(URL, headers=headers)
                if r.ok:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    link_page = soup.select(".css-h3if63")
                    if link_page:
                        print(f"Found second page for {URL}. Getting new URL!")
                        first_link = link_page[0]
                        href = first_link.find("a")["href"]
                        new_URL = link_base_sued + href
                        r = requests.get(new_URL, headers=headers)
                        if r.ok:
                            soup = BeautifulSoup(r.text, 'html.parser')
                            data_text = soup.select('.css-13wylk3')
                            data_abstract = soup.select('.css-1485smx')
                            data_header = soup.select(".css-1bhnxuf")
                            data_topic = soup.select(".css-1tm5due")
                            data_release = soup.select(".css-1r5gb7q")
                            data_author = soup.select(".css-viqvuv")
                            data = {}
                            if data_header:
                                header = [d.get_text() for d in data_header]
                                clean_header = unicodedata.normalize("NFKD", " ".join(header))
                                data['header'] = clean_header
                            else:
                                data['header'] = "NA"
                            if data_topic:
                                topic = [d.get_text() for d in data_topic]
                                clean_topic = unicodedata.normalize("NFKD", " ".join(topic))
                                data['topic'] = clean_topic
                            else:
                                data['topic'] = "NA"
                            if data_release:
                                release = [d.get_text() for d in data_release]
                                clean_release = unicodedata.normalize("NFKD", " ".join(release))
                                match = re.search(r'(\d{1,2}\.\s+[A-Za-zä]+\s+\d{4})', clean_release)
                                if match:
                                    date = match.group(1)
                                    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
                                    date = datetime.strptime(match.group(), '%d. %B %Y').date().strftime("%d-%m-%Y")
                                    data["release"] = date
                                elif match is None:
                                    data["release"] = clean_release
                            else:
                                data['release'] = "NA"
                            if data_author:
                                author = [d.get_text() for d in data_author]
                                clean_author = unicodedata.normalize("NFKD", " ".join(author))
                                data['author'] = clean_author
                            else:
                                data['author'] = "NA"
                            if data_text:
                                text = [d.get_text() for d in data_text]
                                clean_text = unicodedata.normalize("NFKD", " ".join(text))
                                data['text'] = clean_text
                            else:
                                data['text'] = "NA"
                            if data_abstract:
                                abstract = [d.get_text() for d in data_abstract]
                                clean_abstract = unicodedata.normalize("NFKD", " ".join(abstract))
                                data['abstract'] = clean_abstract
                            else:
                                data['abstract'] = "NA"
                            data['new_url'] = new_URL
                            data['url'] = URL
                            data_list.append(data)
                            time.sleep(4)
                            break
                        else:
                            print(r.status_code, new_URL)
                            data['abstract'] = "NA"
                            data['text'] = "NA"
                            data['author'] = "NA"
                            data['release'] = "NA"
                            data['header'] = "NA"
                            data['topic'] = "NA"
                            data['new_url'] = new_URL
                            data['url'] = URL
                            data_list.append(data)
                            time.sleep(4)
                            break
                    else:
                        data_text = soup.select('.css-13wylk3')
                        data_abstract = soup.select('.css-1485smx')
                        data_header = soup.select(".css-1bhnxuf")
                        data_topic = soup.select(".css-1tm5due")
                        data_release = soup.select(".css-1r5gb7q")
                        data_author = soup.select(".css-viqvuv")

                        data = {}
                        if data_header:
                            header = [d.get_text() for d in data_header]
                            clean_header = unicodedata.normalize("NFKD", " ".join(header))
                            data['header'] = clean_header
                        else:
                            data['header'] = "NA"
                        if data_topic:
                            topic = [d.get_text() for d in data_topic]
                            clean_topic = unicodedata.normalize("NFKD", " ".join(topic))
                            data['topic'] = clean_topic
                        else:
                            data['topic'] = "NA"
                        if data_release:
                            release = [d.get_text() for d in data_release]
                            clean_release = unicodedata.normalize("NFKD", " ".join(release))
                            match = re.search(r'(\d{1,2}\.\s+[A-Za-zä]+\s+\d{4})', clean_release)
                            if match:
                                date = match.group(1)
                                locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
                                date = datetime.strptime(match.group(), '%d. %B %Y').date().strftime("%d-%m-%Y")
                                data["release"] = date
                            elif match is None:
                                data["release"] = clean_release
                        else:
                            data['release'] = "NA"
                        if data_author:
                            author = [d.get_text() for d in data_author]
                            clean_author = unicodedata.normalize("NFKD", " ".join(author))
                            data['author'] = clean_author
                        else:
                            data['author'] = "NA"
                        if data_text:
                            text = [d.get_text() for d in data_text]
                            clean_text = unicodedata.normalize("NFKD", " ".join(text))
                            data['text'] = clean_text
                        else:
                            data['text'] = "NA"
                        if data_abstract:
                            abstract = [d.get_text() for d in data_abstract]
                            clean_abstract = unicodedata.normalize("NFKD", " ".join(abstract))
                            data['abstract'] = clean_abstract
                        else:
                            data['abstract'] = "NA"
                        data['url'] = URL
                        data_list.append(data)
                        time.sleep(4)
                        break
                else:
                    print(r.status_code, URL)
                    data['abstract'] = "NA"
                    data['text'] = "NA"
                    data['author'] = "NA"
                    data['release'] = "NA"
                    data['header'] = "NA"
                    data['topic'] = "NA"
                    data['url'] = URL
                    data_list.append(data)
                    time.sleep(4)
                    break
            except:
                print("Error occurred, retrying in 5 seconds...")
                time.sleep(5)

    df = pd.DataFrame(data_list)
    df.to_csv('scraped_news_url_new.csv')

    length_welt = len(url_collection_welt)
    count = 1

    print(f"Scraping remaining {length_all - len(url_collection_sued)} links")
    for URL in url_collection_welt[url_collection_welt.columns[5]]:
        print(f"Scraping welt.de link {count} from {length_welt}")
        count = count + 1
        while True:
            try:
                r = requests.get(URL, headers=headers)
                if r.ok:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    data_text = soup.select('.__margin-bottom--is-0 p')
                    data_abstract = soup.select('.c-summary__intro')
                    data_header = soup.select(".rf-o-headline")
                    data_topic = soup.select(".c-topic")
                    data_release = soup.select(".c-publish-date")
                    data_author = soup.select(".c-author__link")

                    data = {}
                    if data_header:
                        header = [d.get_text() for d in data_header]
                        clean_header = unicodedata.normalize("NFKD", " ".join(header))
                        data['header'] = clean_header
                    else:
                        data['header'] = "NA"
                    if data_topic:
                        topic = [d.get_text() for d in data_topic]
                        clean_topic = unicodedata.normalize("NFKD", " ".join(topic))
                        data['topic'] = clean_topic
                    else:
                        data['topic'] = "NA"
                    if data_release:
                        release = [d.get_text() for d in data_release]
                        clean_release = unicodedata.normalize("NFKD", " ".join(release))
                        match = re.search(r'\d{2}.\d{2}.\d{4}', clean_release)
                        date = datetime.strptime(match.group(), '%d.%m.%Y').date().strftime("%d-%m-%Y")
                        data['release'] = date
                    else:
                        data['release'] = "NA"
                    if data_author:
                        author = [d.get_text() for d in data_author]
                        clean_author = unicodedata.normalize("NFKD", " ".join(author))
                        data['author'] = clean_author
                    else:
                        data['author'] = "NA"
                    if data_text:
                        text = [d.get_text() for d in data_text]
                        clean_text = unicodedata.normalize("NFKD", " ".join(text))
                        data['text'] = clean_text
                    else:
                        data['text'] = "NA"
                    if data_abstract:
                        abstract = [d.get_text() for d in data_abstract]
                        clean_abstract = unicodedata.normalize("NFKD", " ".join(abstract))
                        data['abstract'] = clean_abstract
                    else:
                        data['abstract'] = "NA"
                    if data_text:
                        text = [d.get_text() for d in data_text]
                        clean_text = unicodedata.normalize("NFKD", " ".join(text))
                        data['text'] = clean_text
                    else:
                        data['text'] = "NA"
                    data['url'] = URL
                    data_list.append(data)
                    time.sleep(4)
                    break
                else:
                    print(r.status_code, URL)
                    data['abstract'] = "NA"
                    data['text'] = "NA"
                    data['author'] = "NA"
                    data['release'] = "NA"
                    data['header'] = "NA"
                    data['topic'] = "NA"
                    data['url'] = URL
                    data_list.append(data)
                    time.sleep(4)
                    break
            except:
                print("Timeout occurred, retrying in 5 seconds...")
                time.sleep(5)

    df = pd.DataFrame(data_list)
    df.to_csv('scraped_news_url_new.csv')

    # get faz.net

    count = 1
    length_faz = len(url_collection_faz)

    print(f"Scraping remaining {length_faz} links")
    for URL in url_collection_faz[url_collection_faz.columns[5]]:
        print(f"Scraping FAZ.net link {count} from {length_faz}")
        count = count + 1
        while True:
            try:
                r = requests.get(URL, headers=headers)
                if r.ok:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    link_page = soup.select(".btn-Link-is-in-article-container-functions .btn-Base_Link")
                    if link_page:
                        print(f"Found second page for {URL}. Getting new URL!")
                        link = link_page[0]
                        href = link['href']
                        new_URL = href
                        r = requests.get(new_URL, headers=headers)
                        if r.ok:
                            soup = BeautifulSoup(r.text, 'html.parser')
                            data_text = soup.select('.atc-TextParagraph')
                            data_abstract = soup.select('.atc-IntroText')
                            data_header = soup.select(".atc-HeadlineText")
                            data_topic = soup.select(".atc-HeadlineEmphasisText")
                            data_release = soup.select(".atc-MetaTime")
                            data_author = soup.select(".atc-MetaAuthorLink")

                            data = {}
                            if data_header:
                                header = [d.get_text() for d in data_header]
                                clean_header = unicodedata.normalize("NFKD", " ".join(header))
                                data['header'] = clean_header
                            else:
                                data['header'] = "NA"
                            if data_topic:
                                topic = [d.get_text() for d in data_topic]
                                clean_topic = unicodedata.normalize("NFKD", " ".join(topic))
                                data['topic'] = clean_topic
                            else:
                                data['topic'] = "NA"
                            if data_release:
                                release = [d.get_text() for d in data_release]
                                clean_release = unicodedata.normalize("NFKD", " ".join(release))
                                match = re.search(r'\d{2}.\d{2}.\d{4}', clean_release)
                                date = datetime.strptime(match.group(), '%d.%m.%Y').date().strftime("%d-%m-%Y")
                                data['release'] = date
                            else:
                                data['release'] = "NA"
                            if data_author:
                                author = [d.get_text() for d in data_author]
                                clean_author = unicodedata.normalize("NFKD", " ".join(author))
                                data['author'] = clean_author
                            else:
                                data['author'] = "NA"
                            if data_text:
                                text = [d.get_text() for d in data_text]
                                clean_text = unicodedata.normalize("NFKD", " ".join(text))
                                data['text'] = clean_text
                            else:
                                data['text'] = "NA"
                            if data_abstract:
                                abstract = [d.get_text() for d in data_abstract]
                                clean_abstract = unicodedata.normalize("NFKD", " ".join(abstract))
                                data['abstract'] = clean_abstract
                            else:
                                data['abstract'] = "NA"
                            data['new_url'] = new_URL
                            data['url'] = URL
                            data_list.append(data)
                            time.sleep(4)
                            break
                        else:
                            print(r.status_code, new_URL)
                            data['abstract'] = "NA"
                            data['text'] = "NA"
                            data['author'] = "NA"
                            data['release'] = "NA"
                            data['header'] = "NA"
                            data['topic'] = "NA"
                            data['new_url'] = new_URL
                            data['url'] = URL
                            data_list.append(data)
                            time.sleep(4)
                            break
                    else:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        data_text = soup.select('.atc-TextParagraph')
                        data_abstract = soup.select('.atc-IntroText')
                        data_header = soup.select(".atc-HeadlineText")
                        data_topic = soup.select(".atc-HeadlineEmphasisText")
                        data_release = soup.select(".atc-MetaTime")
                        data_author = soup.select(".atc-MetaAuthorLink")

                        data = {}
                        if data_header:
                            header = [d.get_text() for d in data_header]
                            clean_header = unicodedata.normalize("NFKD", " ".join(header))
                            data['header'] = clean_header
                        else:
                            data['header'] = "NA"
                        if data_topic:
                            topic = [d.get_text() for d in data_topic]
                            clean_topic = unicodedata.normalize("NFKD", " ".join(topic))
                            data['topic'] = clean_topic
                        else:
                            data['topic'] = "NA"
                        if data_release:
                            release = [d.get_text() for d in data_release]
                            clean_release = unicodedata.normalize("NFKD", " ".join(release))
                            match = re.search(r'\d{2}.\d{2}.\d{4}', clean_release)
                            date = datetime.strptime(match.group(), '%d.%m.%Y').date().strftime("%d-%m-%Y")
                            data['release'] = date
                        else:
                            data['release'] = "NA"
                        if data_author:
                            author = [d.get_text() for d in data_author]
                            clean_author = unicodedata.normalize("NFKD", " ".join(author))
                            data['author'] = clean_author
                        else:
                            data['author'] = "NA"
                        if data_text:
                            text = [d.get_text() for d in data_text]
                            clean_text = unicodedata.normalize("NFKD", " ".join(text))
                            data['text'] = clean_text
                        else:
                            data['text'] = "NA"
                        if data_abstract:
                            abstract = [d.get_text() for d in data_abstract]
                            clean_abstract = unicodedata.normalize("NFKD", " ".join(abstract))
                            data['abstract'] = clean_abstract
                        else:
                            data['abstract'] = "NA"
                        data['url'] = URL
                        data_list.append(data)
                        time.sleep(4)
                        break
                else:
                    print(r.status_code, URL)
                    data['abstract'] = "NA"
                    data['text'] = "NA"
                    data['author'] = "NA"
                    data['release'] = "NA"
                    data['header'] = "NA"
                    data['topic'] = "NA"
                    data['url'] = URL
                    data_list.append(data)
                    time.sleep(4)
                    break
            except:
                print("Timeout occurred, retrying in 5 seconds...")
                time.sleep(5)

    # create a dataframe from data_list
    df = pd.DataFrame(data_list)


    print(f"Scraped {len(df.url)} URL from {len(url_collection)}.")

    df.to_csv('scraped_news_url_new.csv', index=False)

else:
    print("There are unrecognized links in the collection!")