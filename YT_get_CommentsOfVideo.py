import os
import googleapiclient
from googleapiclient.discovery import build
import pandas as pd


def load_comments(match):
    for item in match["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textOriginal"]
        list_all_comments.append(text)
        authors.append(author)

        print("Comment by {}: {}".format(author, text))
        if 'replies' in item.keys():
            for reply in item['replies']['comments']:
                rauthor = reply['snippet']['authorDisplayName']
                rtext = reply["snippet"]["textOriginal"]
            print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")


def get_comment_threads(youtube, video_id, nextPageToken):
    results = youtube.commentThreads().list(
        part="snippet",
        maxResults=100, #CHANGE
        videoId=video_id,
        textFormat="plainText",
        pageToken=nextPageToken
    ).execute()
    return results


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAYvRpVKJUS5MUnw6NVcIQB484ao6CdutE"
video_id = "hEMm7gxBYSc"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)
list_all_comments = []
authors = []

match = get_comment_threads(youtube, video_id, '')
next_page_token = match["nextPageToken"]
load_comments(match)

try:
    while next_page_token:
        match = get_comment_threads(youtube, video_id, next_page_token)
        next_page_token = match["nextPageToken"]
        load_comments(match)
except:
    data = pd.DataFrame(list_all_comments, index=authors, columns=["Comments"])
    print(data)


data.to_csv('data.csv')