#

__author__ = 'Sergey Kievskiy <knhel7@mail.ru>'
__date__ = '08.01.23'
__version__ = '0.1.0'

import argparse
import datetime
import json

from tqdm import tqdm
from pprint import pprint
import math

from ya_disk import YandexDisk
from tokens import Token
from vk_photo_crawler import VkUserPhotoCrawler


def get_user_ids(ids='', splitter=',') -> list:
    def get_id(id_: str = '0'):
        id_ = id_.strip()
        try:
            vk_id = int(id_)
        except ValueError as err:
            print(err)
            vk_id = 0
        return id_ if vk_id else ''

    while True:
        if ids:
            vk_user_ids = ids
            ids = ''
        else:
            vk_user_ids = input("\nСкачать фотографии пользователя VK, введите список id через запятую: ")
        vk_ids = (get_id(vk_id) for vk_id in vk_user_ids.split(splitter))
        vk_ids = list(vk_id for vk_id in vk_ids if vk_id)
        if len(vk_ids):
            return vk_ids


def get_args() -> argparse.Namespace:
    yandex_dir = 'Test'

    parser = argparse.ArgumentParser(description='This is а VK photo grabber sample Py program', )
    parser.add_argument('-vk', '--vkIds', action='store',
                        dest='vk_user_ids_string',
                        default='',
                        help='VK user id collection')
    parser.add_argument('-ya', '--yandex', action='store',
                        dest='yandex_dir',
                        default=yandex_dir,
                        help='Yandex disk path to store photos')
    parser.add_argument('-m', '--max', action='store', type=int,
                        dest='max_count_photos',
                        default=0,
                        help='The maximum needed count of photos from each album of the VK user')
    parser.add_argument('-a', '--albums', action='store',
                        dest='albums_string',
                        default='',
                        help='VK user id collection')
    parser.add_argument('-ver', '--version', action='version',
                        version='%(prog)s 0.1.0' + __version__)

    args_ = parser.parse_args()
    args_.yandex_dir = args_.yandex_dir if args_.yandex_dir.isalnum() else yandex_dir
    args_.max_count_photos = abs(args_.max_count_photos)
    # print(f'{type(args_)}:\t{args}')  # -----------------------------------------
    return args_


def get_tokens() -> Token:
    tokens_ = Token()
    while not tokens_.VK:
        tokens_.VK = input('\nОтсутствует токен api VKontakte! Введите сервис-токен VK: ')
    while not tokens_.YA:
        tokens_.YA = input('\nОтсутствует токен api Yandex! Введите свой токен Yandex: ')
    return tokens_


def read_json_file(file, dict_: dict = None):
    try:
        with open(file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as ex:
        print(f'File "{file}" not found...\n\t{ex}\n')
    except OSError as other:
        print(f'При открытии файла "{file}" возникли проблемы: \n\t{other}\n')
    print('Не получилось скачать запрашиваемые данные: недостаточно информации! ')
    return dict_


if __name__ == '__main__':

    def print_user_operation_title(user_: dict, user_dir_: str):
        print(f'\n{"." * 50}\nЗагрузка на Я.диск фото из {user_["count"]} альбомов'
              f' пользователя "{user_["user_title"]}"'
              f'\nв папку {user_dir_}:')


    def print_album_operation_title(album_):
        print(f'\n\tЗагрузка на Я.диск фото из альбома "{album_["album_title"]}" ({album_["album_id"]})')


    def print_finally_msg(count: int):
        print(f'\nЗагрузка на Я.диск {count} фото из альбомов VK пользователей завершена!')


    args = get_args()
    tokens = get_tokens()
    vk_crawler = VkUserPhotoCrawler(token=tokens.VK)
    ya = YandexDisk(token=tokens.YA)
    ya.makedir(args.yandex_dir)

    # vk_photos_filename = vk_crawler.start(vk_ids=get_user_ids(), max_count_photos=3, albums_string='profile')
    # vk_photos_filename = vk_crawler.start(vk_ids=get_user_ids('11,14,17'), max_count_photos=2)
    vk_photos_filename = vk_crawler.start(vk_ids=get_user_ids(args.vk_user_ids_string),
                                          max_count_photos=abs(args.max_count_photos),
                                          albums_string=args.albums_string.replace(' ', ''))
    photos: dict = read_json_file(vk_photos_filename) if vk_photos_filename else {}

    photo_counter: int = 0
    start_time = str(datetime.datetime.now()).split('.')[0]
    for char in '- :':
        start_time = start_time.replace(char, '')

    for user in photos:
        user_name = f'{user["user_title"][:30]}'
        user_dir = f'{args.yandex_dir}/{user_name}_{start_time}'
        ya.makedir(user_dir)
        print_user_operation_title(user, user_dir)

        for album in user['albums']:
            album_name = f'{album["album_id"]}_{album["album_title"][:30]}'
            print_album_operation_title(album)

            for vk_photo in tqdm(album['photos']):
                photo_name: str = vk_photo['url'].split('/')[-1].split('?')[0]
                ya_path = f"{user_dir}/{user_name}_{album_name}_{start_time}_likes{vk_photo['likes']}_{photo_name}"
                # print(ya_path)  # ----------------------------------------
                ya.upload_file_to_disk(upload_path=ya_path, saved_file_name=vk_photo['url'])
                photo_counter += 1

    print_finally_msg(photo_counter)
