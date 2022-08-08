import os
import json
import requests
from tqdm import tqdm

def photos_get_id(token_vk, id):
    photos_get_url = f'https://api.vk.com/method/photos.get?access_token={token_vk}'
    photos_param = {
        'album_id':  'profile',
        'v': '5.131',
        'extended': 1,
        'count': 5,
        'owner_id': id
    }

    req = requests.get(photos_get_url, params=photos_param).json()['response']['items']

    # Создаю папку с помощью метода - mkdir у модуля OS, называю ее фото
    os.mkdir("foto")

    json_params = []

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

        def upload():
            HEADERS = {"Authorization": f'OAuth token_yandex'}  #укажите яндекс-токен
            FILES = {"file": download_photo}
            params = {"path": f'{file_name}.jpg'}

            response_url = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload", params=params, headers=HEADERS)

            url = response_url.json().get('href')

            response_upload = requests.put(url, files=FILES, headers={})

            if response_upload.status_code == 201:
                return 'Файл успешно загружен на Я.Диск'

        upload()

    with open('aaa.json', 'w') as f:
        json.dump(json_params, f)

# Введите токен Вк
token = 'vk'

photos_get_id(token, '3238110')
