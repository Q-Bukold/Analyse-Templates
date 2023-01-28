import os
import googleapiclient
from googleapiclient.discovery import build
import pandas as pd
import time

def get_comment(api, video, page_token):
    #create list of lists
    page_list = []

    #get page
    page = api.commentThreads().list(
        part="snippet",
        maxResults=100, #CHANGE
        videoId=video_id,
        textFormat="plainText",
        #is there a netxt page? If yes, get token:
        pageToken=page_token,
        order="time" # "time" or "relevance" (not the same as TOP-Comments on YT, but similar)
    ).execute()

    for item in page["items"]:
        item_list = []
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textOriginal"]
        #print("Comment by {}: {}".format(author, text))
        item_list.append(author)
        item_list.append(text)
        page_list.append(item_list)

        '''
        if 'replies' in item.keys():
            for reply in item['replies']['comments']:
                rauthor = reply['snippet']['authorDisplayName']
                rtext = reply["snippet"]["textOriginal"]
            #print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")
        '''

    next_page_token = page["nextPageToken"]
    return page_list, next_page_token

def post_processing_and_saving(list, filename):
    #convert to df
    data_df = pd.DataFrame(list, columns=['author', 'comment'])

    #delete newlines in comments
    data_df['comment'] = data_df['comment'].replace(r'\s+|\\n', ' ', regex=True) 
    #strip excess white spaces
    data_df['comment'] = data_df['comment'].str.strip()

    #print(data_df.shape)
    lenght_df = data_df.shape[0]
    data_df.to_csv(filename, sep="\t")
    
    return lenght_df

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAYvRpVKJUS5MUnw6NVcIQB484ao6CdutE"
youtube_api = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)
video_id = "PgF-rcHcPqE" #gwtw
set_filename = "/Users/qbukold/Desktop/Schnulzen/1000_gwtw.tsv"
data = []
next_page_token = ''
is_first_page = True
lenght_df = 0
waiting_time = 30 #seconds


max_lenght_df = 1000 #CHANGE


while is_first_page or next_page_token and lenght_df <= max_lenght_df:

    is_first_page = False
    page_data, next_page_token = get_comment(youtube_api, video_id, next_page_token)
    data += page_data
    lenght_df = post_processing_and_saving(data, set_filename)
    print(lenght_df)


lenght_df = post_processing_and_saving(data, set_filename)
print("final len:", lenght_df)