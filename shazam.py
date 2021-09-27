import config
import requests
import json


def shazam_voice(file):
    """
    По ссылке определяет название и много другой информации
    :param file: Путь к файлу
    :return: возвращает json формат
    """
    data = {
        'api_token': config.API,
        'url': f'https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file}',
        'return': 'musicbrainz,lyrics,apple_music,spotify,deezer,napster,youtube',
    }
    file = requests.post('https://api.audd.io/', data=data)  # recognizeWithOffset/
    music = file.json()
    print(music)
    return music


def download_youtube(url):
    file = "..."
    return file

