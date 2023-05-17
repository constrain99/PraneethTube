from googleapiclient.discovery import build
import csv
import pandas as pd
import random
import numpy as np
import time
api_key='AIzaSyDwqdLReFcAWNMvJKu5GlMaSvJEZGyHo40'
api_key='AIzaSyBjitT48BKFtUm-Lit4e4SnWJ9gh8vSLas'
with open('watched_videos.csv', 'r') as f:
        reader = csv.reader(f)
        a=[]
        i=-1
        for row in reader:
            a.append(i+1)
            i=i+1

        new_video_ids = []
        for j in range(0,9): 
            time.sleep(1)
            print("hoo\n")
            temp=random.choice(a)
            a.remove(temp)

            df=pd.read_csv('watched_videos.csv',header=None)
            temp2=df.iloc[temp]
            data=temp2.values
            data2=str(data)
            
            data2=data2[2:-2]
            print(data2)
            youtube = build('youtube', 'v3', developerKey=api_key)
            request = youtube.search().list(
                part="snippet",
                maxResults=1,
                type="video",
                fields="items(id(videoId),snippet(thumbnails, title))",
                relatedToVideoId='SEeQgNdJ6AQ'
            )
            
            response = request.execute()

            print(response['items'])
            # for item in response['items']:
            #     if 'videoId' in item['id']:
            #         video_id = item['id']['videoId']
            #         thumbnail = item['snippet']['thumbnails']['default']['url']
            #         title = item['snippet']['title']
            #         new_video_ids.append((video_id, thumbnail, title))
            #     else:
            #         print(f"Skipping item {item['id']} because it does not have a videoId")
            
            # print(new_video_ids)
