# Script to mine comments from YouTube and store them in different files for each category 
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets

import httplib2
import sys
import csv
import re


from apiclient.discovery import build_from_document
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from importlib  import reload

reload(sys)

# Load necessary API token and configuration files
CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

# Authenticate the account and fetch the 
def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)
    with open("youtube-v3-discoverydocument.json", "r") as f:
        doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))

# Function to make YouTube API Calls for video details
def get_videos(youtube, channelId, maxResults, pageToken):
    result = youtube.search().list(
    part="snippet",
    channelId=channelId,
    pageToken=pageToken,
    order="viewCount",
    publishedAfter="2015-01-01T00:00:00Z",
    publishedBefore="2018-01-01T00:00:00Z",
    safeSearch="none",
    type="video",
    maxResults=maxResults
    ).execute()
    return result

# Function to make YouTube API Calls for comments details
def get_comments(youtube, videoId, maxResults, pageToken):
    result = youtube.commentThreads().list(
    part="snippet",
    videoId=videoId,
    pageToken=pageToken,
    order="relevance",
    textFormat="plainText",
    maxResults=maxResults
    ).execute()
    return result

def clean_str(string):
    string = string.encode("ascii", "ignore");
    string = string.decode('utf-8')
    return re.sub(r"\s+", " ", string).strip()

# function to make API calls to the comment thread API and fetch comments for 25 most watched videos
# 300 comments per video ; 7500 comments per channel ; 25 * 7500 = 30k comments per category
def mine_comments(youtube,channels, file_name):  
    
    for channel in channels:
        videos = []
        pageToken = None
        comments = []
        
        for _ in range(1):
            if pageToken != False:
                resultVideos = get_videos(youtube, channel["id"], 25, pageToken)  # 25 most watched videos
                videos.extend(resultVideos["items"])
                pageToken = resultVideos.get("nextPageToken", False)
        
        for i, vi in enumerate(videos):
            
            print ("%s: %d" % (channel["name"], i))
            videoId = vi["id"]["videoId"]
            pageToken = None
            
            for _ in range(3):
                if pageToken != False:
                    try:
                        resultComments = get_comments(youtube, videoId, 100, pageToken) # 300 comments per video 
                        comments.extend(resultComments.get("items", []))
                        pageToken = resultComments.get("nextPageToken", False)
                    except:
                        print("Locked comments")
                        continue      
                
        with open(file_name, "a+") as commentFile:
            commentWriter = csv.writer(commentFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            commentWriter.writerows([["channelId","videoId", "commentId", "author", "text", "replies", "likes", "publishedAt"]])
            for comment in comments:
                clc = comment["snippet"]["topLevelComment"]["snippet"]
                
                commentWriter.writerows([ [
                                          channel["id"],
                                          comment["snippet"]["videoId"],
                                          comment["snippet"]["topLevelComment"]["id"],
                                          clean_str(clc["authorDisplayName"]),
                                          clean_str(clc["textDisplay"]),
                                          comment["snippet"]["totalReplyCount"],
                                          clc["likeCount"],
                                          clc["publishedAt"].encode("ascii", "ignore")
          ]])
            
# Initiates mining procedure for each of the categories
# list of channels are selected based on popularity
def start_mining(youtube):
    comedy_channels = [
      {"category": "comedy", "id": "UCUsN5ZwHx2kILm84-jPDeXw", "name": "comedy central"},
      {"category": "comedy", "id": "UCPDXXXJj9nax0fr0Wfc048g", "name": "CollegeHumor"},
      {"category": "comedy", "id": "UC0ntBMtAa1ecIP3Yu5lktCg", "name": "Just for laugh gags"},
      {"category": "comedy", "id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw", "name": "PewDiePie"},
      {"category": "comedy", "id": "UCY30JRSgfhYXA6i6xX1erWg", "name": "SMOSH"}, 
    ]
    
    news_channels = [
      {"category": "news", "id": "UCupvZG-5ko_eiXAupbDfxWw", "name": "CNN"},
      {"category": "news", "id": "UCXIJgqnII2ZOINSWNOGFThA", "name": "Fox News"},
      {"category": "news", "id": "UCBi2mrWuNuyYy4gbM6fU18Q", "name": "ABC News"},
      {"category": "news", "id": "UCwqusr8YDwM-3mEYTDeJHzw", "name": "Vox News"},
    ]
    
    tech_channels = [
      {"category": "Tech", "id": "UCsTcErHg8oDvUnTzoqsYeNw", "name": "UnboxTherapy"},
      {"category": "Tech", "id": "UCXuqSBlHAE6Xw-yeJA0Tunw", "name": "LinusTechTips"},
      {"category": "Tech", "id": "UCddiUEpeqJcYeBxX1IVBKvQ", "name": "TheVerge"},
      {"category": "Tech", "id": "UCBJycsmduvYEL83R_U4JriQ", "name": "MarquesBrownlee"}, 
    ]
    
    tv_channels = [
      {"category": "TV_Show", "id": "UC4PooiX37Pld1T8J5SYT-SQ", "name": "Good Mythical Morning"},
      {"category": "TV_Show", "id": "UCzH3iADRIq1IJlIXjfNgTpA", "name": "Rooster Teeth"},
      {"category": "TV_Show", "id": "UCH6vXjt-BA7QHl0KnfL-7RQ", "name": "Simon's Cat"},
      {"category": "TV_Show", "id": "UC0v-tlzsn0QZwJnkiaUSJVQ", "name": "FBE"},
    ]
    
    mine_comments(youtube,comedy_channels,"comments_comedy.csv")
    mine_comments(youtube,news_channels,"comments_news.csv")
    mine_comments(youtube,tech_channels,"comments_tech.csv")
    mine_comments(youtube,tv_channels,"comments_TV.csv")
    
    
if __name__== '__main__':
    args = argparser.parse_args()
    youtube = get_authenticated_service(args)
    start_mining(youtube)