import os
import httplib2
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd
import pickle


SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = "/Users/gaurang.mac/Desktop/Pycharm/SMDM/Project/client_secret_"

def get_authenticated_service(idx):
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE+str(idx)+".json", SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs


def search_list_by_keyword(client, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.search().list(
    **kwargs
  ).execute()

  return response

def videos_list_by_id(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.videos().list(
    **kwargs
  ).execute()

  return(response)

#converts ISOTIME: e.g.:PT4M13S to seconds
def getSec(isoTime):
  isoTime = isoTime[2:]
  time_res = 0
  time_curr = ""

  for idx in isoTime:
    if not idx.isalpha():
      time_curr += idx
    else:
      if idx.lower() == 'h':
        time_res += int(time_curr)*3600
        time_curr = ""
      if idx.lower() == 'm':
        time_res += int(time_curr) * 60
        time_curr = ""
      if idx.lower() == 's':
        time_res += int(time_curr)
        time_curr = ""

  return time_res


# News, Comedy, Science, Technology , Black-hole, Gaming are the top trending queries for the mentioned genre
query = [
         ["live news","fox news","the news","news today","live fox news","news live stream",
         "fox news live stream","cnn news","cnn","latest news"],
         ["comedy stand up","stand up","movies comedy","comedy movie","comedy central","comedy full movies",
         "full movies","comedy scenes","comedy full movie","full movie"],
         ["science","the science","kids science","scientific","science experiments","science for kids",
         "the science of","science fair","science projects","spirit science"],
         ["technology","tech","new technology","best tech","technology 2018","tech 2018",
          "tecnologia","cool tech","future technology","5g"],
         ["5g technology","technology 2019","tech under 50","tech deals","information technology",
          "new tech","top tech","tech review","ancient technology","tech gadgets"],
         ["black hole sun","the black hole","supermassive black hole","black hole picture","soundgarden",
          "black hole sun soundgarden","black hole interstellar","interstellar","black hole muse","muse"],
         ["gaming with kev","gaming pc","gaming with jen","gaming beaver","fortnite gaming","gaming music",
          "gaming setup","neebs gaming","the gaming beaver","gaming laptop"],
         ["get good gaming","camodo gaming","gaming mouse","gaming monitor","gaming keyboard","gaming pc build",
          "gaming headset","gaming lemon","best gaming pc","youtube gaming"]]



for idx in range(len(query)):

  client = get_authenticated_service(idx)
  try:
    for qry in query[idx]:
      pt = ''
      #find the video id for above query
      for i in range(10):
        result = search_list_by_keyword(client,
            part='snippet',
            maxResults=50,
            q=qry,
            pageToken = pt,
            type='')

        ids_temp = []

        for item in result["items"]:
          if "videoId" in item["id"]:
            ids_temp.append(item["id"]["videoId"])


        if len(ids_temp) == 0:
          break

        # store in pickle
        f = open("search.pickle", "ab")
        pickle.dump(ids_temp, f)
        f.close()

        pt = result["nextPageToken"]
  except Exception as e: print(e)



client = get_authenticated_service(6)

video_len = []
video_like = []
video_view = []

#get video details
with open("search.pickle", "rb") as f:
  while True:
    try:

      video_name =[]
      video_len = []
      video_like = []
      video_view = []

      ids_temp = pickle.load(f)
      ids = ",".join(ids_temp)
      result_vid = videos_list_by_id(client,
                        part='snippet,contentDetails,statistics',
                        id=ids)


      for vid in result_vid["items"]:

        try:
          vid_name_temp = vid['snippet']['title']
          vid_len_temp = getSec(vid["contentDetails"]["duration"])
          vid_like_temp = int(vid["statistics"]["likeCount"])
          video_view_temp = int(vid["statistics"]["viewCount"])
          video_name.append(vid_name_temp)
          video_len.append(vid_len_temp)
          video_like.append(vid_like_temp)
          video_view.append(video_view_temp)
        except:
          print("miss")

      g = open("video_list.pickle", "ab")
      pickle.dump(video_name,g)
      pickle.dump(video_len, g)
      pickle.dump(video_like, g)
      pickle.dump(video_view, g)
      g.close()

    except Exception as e:
      break

video_name_draw = []
video_len_draw = []
video_like_draw = []
video_view_draw = []

#save it in csv
with open("video_list.pickle", "rb") as f:
  while True:
    try:
      video_name_draw.extend(pickle.load(f))
      video_len_draw.extend(pickle.load(f))
      video_like_draw.extend(pickle.load(f))
      video_view_draw.extend(pickle.load(f))
    except:
      break

video_len = [int(idx) for idx in video_len_draw]
video_like = [int(idx) for idx in video_like_draw]
video_view = [int(idx) for idx in video_view_draw]

s1 = pd.Series(video_name_draw,name="Name")
s2 = pd.Series(video_len,name="Length")
s3 = pd.Series(video_like,name="Like")
s4 = pd.Series(video_view,name="View")
temp_csv_1 = pd.concat([s1,s2,s3,s4],axis=1)

temp_csv_1.to_csv('video_data.csv', sep=",")




