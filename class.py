import os
import json
import requests
from tqdm import tqdm


class Yandex_user:
    def __init__(self, name_folder):
        self.name_folder = name_folder

    def upload(self, download_photo, file_name):
        self.download_photo = download_photo
        self.file_name = file_name

        HEADERS = {"Authorization": f'OAuth token_yandex'}  # укажите яндекс-токен
        FILES = {"file": self.download_photo}

        params = {"path": f'{self.name_folder}/{self.file_name}.jpg'}

        response_url = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload",
                                    params=params, headers=HEADERS)

        url = response_url.json().get('href')

        response_upload = requests.put(url, files=FILES, headers={})

        if response_upload.status_code == 201:
            return 'Файл успешно загружен на Я.Диск'

    def create_folder_on_YandexDisk(self):
        HEADERS = {"Authorization": f'OAuth token_yandex'}  # укажите яндекс-токен
        folder_param = {
            'path': self.name_folder
        }

        url_folder = requests.put('https://cloud-api.yandex.net/v1/disk/resources', params=folder_param, headers=HEADERS).json()
        return url_folder['href']

class Vk_user:
    url = 'https://api.vk.com/method/'

    def __init__(self, token_vk, version):
        self.token_vk = token_vk
        self.params = {
            'access_token': token_vk,
            'v': version
        }

    def photos_get_id(self, id):
        photos_get_url = self.url + f'photos.get?access_token={self.token_vk}'
        photos_param = {
            'album_id': 'profile',
            'v': '5.131',
            'extended': 1,
            'count': 5,
            'owner_id': id
        }

        req = requests.get(photos_get_url, params=photos_param).json()['response']['items']

        # Создаю папку с помощью метода - mkdir у модуля OS, называю ее фото
        os.mkdir("foto")

        json_params = []
        name_folder = 'new_folder2'
        f = Yandex_user(name_folder)
        f.create_folder_on_YandexDisk()

        # Цикл, в котором итерируем все фото
        for item in tqdm(req):
            getMaxUrlFoto = max(item['sizes'], key=lambda x: x['height'] * x['width'])

            # Далее я загружаю (скачиваю) это фото и кладу в переменную
            download_photo = requests.get(getMaxUrlFoto['url']).content

            file_name = str(item["likes"]["count"]) + f'({item["id"]})'

            json_params.append({'file_name': file_name, 'size': getMaxUrlFoto['type']})

            # # создаю фаил  расширением jpg и называю его как колличество лайков и записываю в него данные из download_photo
            with open(f'foto/{file_name}.jpg', 'wb') as file:
                file.write(download_photo)

            f.upload(download_photo, file_name)

        with open('aaa.json', 'w') as f:
            json.dump(json_params, f)

if __name__ == '__main__':
    # Введите токен Вк
    token = 'vk'
    client_vk = Vk_user(token, '5.131')
    # Введите id
    client_vk.photos_get_id('id')



