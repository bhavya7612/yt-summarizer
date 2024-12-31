from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("YT_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_title(video_id):
    request=youtube.videos().list(part="snippet", id=video_id)
    response=request.execute()
    video_title=response['items'][0]['snippet']['title']
    return video_title