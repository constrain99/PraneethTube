from flask import Flask, render_template, request
from googleapiclient.discovery import build
import csv
import pandas as pd
import random
import numpy as np
import time
app = Flask(__name__)

# Your YouTube API key
api_key = 'AIzaSyBjitT48BKFtUm-Lit4e4SnWJ9gh8vSLas'

# Define the YouTube search function
def youtube_search(query):

    print(query)
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        maxResults=10,
        fields="items(id(videoId),snippet(thumbnails, title))", 
        q=query
    )
    response = request.execute()
    video_ids = []
    for item in response['items']:
        if 'videoId' in item['id']:
            video_id = item['id']['videoId']
            thumbnail = item['snippet']['thumbnails']['default']['url']
            title = item['snippet']['title']
            video_ids.append((video_id, thumbnail, title))
        else:
            print(f"Skipping item {item['id']} because it does not have a videoId")

    return video_ids

#home page recomendation api
def rec_search():
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
            temp=random.choice(a)
            a.remove(temp)

            df=pd.read_csv('watched_videos.csv',header=None)
            temp2=df.iloc[temp]
            data=temp2.values
            data2=str(data)

            data2=data2[2:-2]
            
            youtube = build('youtube', 'v3', developerKey=api_key)
            request = youtube.search().list(
                part="snippet",
                maxResults=1,
                type="video",
                fields="items(id(videoId),snippet(thumbnails, title))",
                relatedToVideoId=data2
            )
            response = request.execute()
            for item in response['items']:
                if 'videoId' in item['id']:
                    video_id = item['id']['videoId']
                    thumbnail = item['snippet']['thumbnails']['default']['url']
                    title = item['snippet']['title']
                    new_video_ids.append((video_id, thumbnail, title))
                else:
                    print(f"Skipping item {item['id']} because it does not have a videoId")

        return new_video_ids

    

# Define the home route
@app.route('/')
def home():
    new_video_ids=rec_search()
    return render_template('index.html',new_video_ids=new_video_ids)

# Define the search route
@app.route('/search', methods=['POST'])
def search():
    # Get the search query from the form data
    search_query = request.form['query']
    # Call the YouTube search function
    video_ids = youtube_search(search_query)

    # Pass the video IDs to the template
    return render_template('result.html', video_ids=video_ids)


watched_ids=[]
# Define the watch route
@app.route('/watch/<video_id>')
def watch(video_id):
    with open('watched_videos.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                watched_ids.append(row[0])
    if video_id in watched_ids:
        return render_template('watch.html', video_id=video_id)


    else:
        with open('watched_videos.csv', mode='a', newline='') as watched_videos_file:
            watched_videos_writer = csv.writer(watched_videos_file)
            watched_videos_writer.writerow([video_id])
        return render_template('watch.html', video_id=video_id)


if __name__ == '__main__':
    app.run(debug=True)
