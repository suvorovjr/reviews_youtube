import json
from typing import Union, Optional
from config import settings
from googleapiclient.discovery import build
from common.schemas import ChanelIDResponseModel


class GoogleAPIClient:
    api_key = settings.YOUTUBE_API_KEY
    logger = settings.logger

    def __init__(self, chanel_link: str) -> None:
        self._api_client = build('youtube', 'v3', developerKey=self.api_key)
        self._chanel_link = chanel_link
        self._chanel_id = self._get_chanel_id()

    def _get_chanel_id(self) -> str:
        """
        Метод для получения ID каналов по ссылке на них
        :return: ID канала, полученный по ссылке на канал в self._chanel_link
        """

        chanel_name = self._chanel_link.split('/')[-1]
        method = 'GET_CHANEL_ID'
        response = ChanelIDResponseModel(**self._execute_request(method=method, chanel_name=chanel_name))
        if response.items and len(response.items) > 0:
            chanel_id = response.items[0].id.channelId
            self.logger.info(f'Получен ID {chanel_id} к каналу {self._chanel_link}')
            return chanel_id
        self.logger.error(f'ID канала не удалось получить. Название канала: {chanel_name} по ссылке /'
                          f'{self._chanel_link}. Ответ от youtube {response}')
        raise TypeError

    def _execute_request(self, method: str, chanel_name: Optional[str] = None) -> dict:
        match method:
            case 'GET_CHANEL_ID':
                request = self._api_client.search().list(
                    part='snippet',
                    q=chanel_name,
                    type='channel'
                )
                response = request.execute()
                return response
            case 'GET_VIDEOS':
                pass

    async def _get_all_videos(self):

        pass

    async def get_reviews(self):
        pass

    @staticmethod
    def get_chanel_id_from_response(response: dict) -> Union[str, None]:
        pass


chanel_links = 'https://www.youtube.com/@user-zu4xh6vb4p'
client = GoogleAPIClient(chanel_link=chanel_links)

# import json
# import os
#
# from dotenv import load_dotenv
# from googleapiclient.discovery import build
# from pathlib import Path
#
# BASE_DIR = Path(__file__).parent
# load_dotenv(BASE_DIR / '.env')
#
# API_KEY = os.getenv('YOUTUBE_API')
# CHANNEL_ID = 'myachshorts'
#
# youtube = build('youtube', 'v3', developerKey=API_KEY)
#
# request = youtube.search().list(
#     part='snippet',
#     q='@myachshorts',
#     type='channel'
# )
#
# response = request.execute()
#
# # Обработка результата
# if 'items' in response and len(response['items']) > 0:
#     channel_id = response['items'][0]['id']
#     print(f"Channel ID: {channel_id}")
# else:
#     print(response)
#     print("Канал не найден")
#
# request = youtube.search().list(
#     part='snippet',
#     channelId=channel_id['channelId'],
#     maxResults=50,
#     order='date'
#
# )
#
# response = request.execute()
#
# for item in response['items']:
#     if item['id']['kind'] == 'youtube#video':
#         print(f"Title: {item['snippet']['title']}, Video ID: {item['id']['videoId']}")
#
# with open('test.json', 'w', encoding='utf-8') as file:
#     json.dump(response, file, ensure_ascii=False, indent=4)
