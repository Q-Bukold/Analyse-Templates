import os
import googleapiclient
from googleapiclient.discovery import build
import pandas as pd

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAYvRpVKJUS5MUnw6NVcIQB484ao6CdutE"
video_id = "XFkzRNyygfk" #creep
youtube_api = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

def get_comment(api, video, page_token):
    #create list of lists
    page_list = []

    #get page
    page = api.commentThreads().list(
        part="snippet",
        maxResults=5, #CHANGE
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

    print(data_df.shape)
    lenght_df = data_df.shape[0]
    data_df.to_csv(filename, sep="\t")
    
    return lenght_df




data = []
next_page_token = ''
is_first_page = True
lenght_df = 0

max_lenght_df = 20

while is_first_page or next_page_token and lenght_df <= max_lenght_df:
    is_first_page = False
    page_data, next_page_token = get_comment(youtube_api, video_id, next_page_token)
    data += page_data

    lenght_df = post_processing_and_saving(data, '/Users/qbukold/Desktop/Schnulzen/gonewiththewind_comments2.tsv')



lenght_df = post_processing_and_saving(data, '/Users/qbukold/Desktop/Schnulzen/gonewiththewind_comments2.tsv')
print(lenght_df)