import os
import googleapiclient
from googleapiclient.discovery import build
import pandas as pd

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = ""
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
    print(page_list)

    return page_list, next_page_token



data = []
next_page_token = ''
is_first_page = True
i = 1
i_max = 5 # N of comments = i_max * maxResults

while is_first_page or next_page_token and i <= i_max:
    i += 1
    is_first_page = False
    page_data, next_page_token = get_comment(youtube_api, video_id, next_page_token)
    data += page_data



data_df = pd.DataFrame(data, columns=['author', 'comment'])

#post processing
data_df['comment'] = data_df['comment'].replace(r'\s+|\\n', ' ', regex=True) 
data_df['comment'] = data_df['comment'].str.strip()



print(data_df)
print(data_df.shape)

data_df.to_csv('/Users/qbukold/Desktop/Schnulzen/gonewiththewind_comments2.tsv', sep="\t")
