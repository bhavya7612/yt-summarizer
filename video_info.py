import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from dotenv import load_dotenv
load_dotenv()

yt_api_key=os.getenv("YT_API_KEY")
youtube = build('youtube', 'v3', developerKey=yt_api_key)

# get video title through api_key
def get_video_title(video_id):
    try:
        request=youtube.videos().list(part="snippet", id=video_id)
        response=request.execute()
        video_title=response['items'][0]['snippet']['title']
        return video_title
    except Exception as e:
        print(f"error is {e}")
        return "Cannot find title"

def get_video_transcript(video_id):                                              
    proxies={
        "https":f'{os.getenv("proxy2")}',
    }

    try:
        session = requests.Session()
        session.proxies.update(proxies)
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages = ['en','en-IN','en-US','en-UK','es','hi','de','fr','ru','ja','ar'],
            # proxies = session.proxies
        )
        transcript_text=""
        for d in transcript_list:
            transcript_text += " " + d['text']
        return transcript_text
    except Exception as e:
        print(f"Error is {e}")
        return "No Transcript Found"
