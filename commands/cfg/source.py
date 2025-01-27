import aiohttp
import logging
from dotenv import load_dotenv
from os import getenv

load_dotenv()
YT_TOKEN = getenv('yt_token')


class YTDLSource:
    def __init__(self, data):
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_query(cls, query):
        api_key = YT_TOKEN
        search_url = "https://www.googleapis.com/youtube/v3/search"
        video_url = "https://www.googleapis.com/youtube/v3/videos"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(search_url, params={
                    'part': 'snippet',
                    'q': query,
                    'type': 'video',
                    'key': api_key,
                    'maxResults': 1
                }) as search_resp:
                    search_data = await search_resp.json()
                    video_id = search_data['items'][0]['id']['videoId']

                async with session.get(video_url, params={
                    'part': 'snippet,contentDetails',
                    'id': video_id,
                    'key': api_key
                }) as video_resp:
                    video_data = await video_resp.json()
                    video_info = video_data['items'][0]

                    return cls({
                        'title': video_info['snippet']['title'],
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    })

            except Exception as e:
                logging.error(f"Error retrieving video information: {e}")
                raise