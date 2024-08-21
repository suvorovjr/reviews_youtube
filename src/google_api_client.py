from typing import Optional
from config import settings
from googleapiclient.discovery import build
from common.exceprions import ValidationError
from common.schemas import ChanelIDResponseModel, VideosListModel, ReviewsResponseModel


class GoogleAPIClient:
    """
    Класс для работы с youtube по API
    Для работы класса необходимо добавить в файл .env ключ для работы с сервисом
    """
    api_key = settings.YOUTUBE_API_KEY
    logger = settings.logger

    def __init__(self, chanel_link: str) -> None:
        """Union
        Инициализатор класса
        :param chanel_link: ссылка на канал
        """

        self._api_client = build('youtube', 'v3', developerKey=self.api_key)
        self._chanel_link = chanel_link
        self._chanel_id = self._get_chanel_id()

    def _execute_request(self, method: str, id_or_name: Optional[str] = None, page_token: Optional[str] = None) -> dict:
        match method:
            case 'GET_CHANEL_ID':
                request = self._api_client.search().list(
                    part='snippet',
                    q=id_or_name,
                    type='channel'
                )
                response = request.execute()
                return response
            case 'GET_VIDEOS':
                request = self._api_client.search().list(
                    part='snippet',
                    channelId=self._chanel_id,
                    maxResults=50,
                    order='date',
                    pageToken=page_token
                )
                response = request.execute()
                return response
            case 'GET_REVIEWS':
                request = self._api_client.commentThreads().list(
                    part='snippet',
                    videoId=id_or_name,
                    textFormat='plainText',
                    maxResults=100,
                    pageToken=page_token
                )
                response = request.execute()
                return response

    def _get_chanel_id(self) -> str:
        """
        Метод для получения ID каналов по ссылке на них
        :return: ID канала, полученный по ссылке на канал в self._chanel_link
        """

        chanel_name = self._chanel_link.split('/')[-1]
        method = 'GET_CHANEL_ID'
        response = self._execute_request(method=method, id_or_name=chanel_name)
        validate_response = ChanelIDResponseModel(**response)
        if validate_response.items and len(validate_response.items) > 0:
            chanel_id = validate_response.items[0].id.channel_id
            self.logger.info(f'Получен ID {chanel_id} к каналу {self._chanel_link}')
            return chanel_id
        msg = (f'ID канала не удалось получить. Название канала: {chanel_name} по ссылке /'
               f'{self._chanel_link}. Ответ от youtube {response}')
        self.logger.error(msg)
        raise ValidationError()

    def _get_all_videos(self) -> list[dict]:
        """
        Метод для получения всех видео с канала
        :return: Список словарей с названием видео и его ID
        """

        method = 'GET_VIDEOS'
        videos = []
        next_page_token = None
        page_count = 1
        while True:
            response = self._execute_request(method=method, page_token=next_page_token)
            validate_response = VideosListModel(**response)
            self.logger.info(f'Получил страницу с видео № {page_count}')
            if validate_response.videos and len(validate_response.videos) > 0:
                video = [{'title': video.snippet.title, 'id': video.id.video_id} for video in validate_response.videos
                         if video.id.video_id is not None]
                self.logger.info(f'Получено {len(video)} ID видео.')
                videos.extend(video)
            else:
                self.logger.warning('Видео не найдены')
            if validate_response.next_page_token is None:
                self.logger.info(f'Все видео с канала {self._chanel_link} собраны. Всего видео: {len(videos)}')
                return videos
            next_page_token = validate_response.next_page_token
            page_count += 1

    def _get_reviews(self, video: dict):
        """
        Метод для получения комментариев со всех видео
        :return:
        """

        all_reviews = []
        method = 'GET_REVIEWS'
        next_page_token = None
        page_count = 1
        while True:
            response = self._execute_request(method=method, id_or_name=video['id'], page_token=next_page_token)
            validate_response = ReviewsResponseModel(**response)
            self.logger.info(f'Получил страницу с комментариями № {page_count}. По видео {video["title"]}')
            if validate_response.reviews and len(validate_response.reviews) > 0:
                all_reviews.extend(validate_response.reviews)
                self.logger.info(f'Получено {len(validate_response.reviews)} комментариев.')
            else:
                self.logger.warning('Комментарии не найдены')
            if validate_response.next_page_token is None:
                self.logger.info(
                    f'Все комментарии для видео {video["title"]} собраны. Всего комментариев: {len(all_reviews)}')
                return all_reviews
            next_page_token = validate_response.next_page_token
            page_count += 1

    def run(self):
        videos = self._get_all_videos()
        all_reviews = []
        for video in videos:
            reviews = self._get_reviews(video=video)
            all_reviews.extend(reviews)
        return all_reviews


chanel_link = 'https://www.youtube.com/@user-zu4xh6vb4p'
client = GoogleAPIClient(chanel_link=chanel_link)
client.run()
