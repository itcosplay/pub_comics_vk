import os
import urllib
import requests
import random

from environs import Env


def main():
    env = Env()
    env.read_env()

    vk_token = env('VK_TOKEN')
    group_id = env('GROUP_ID')

    file_name, autor_comment = get_comics()

    upload_url = get_upload_server_data(vk_token, group_id)
    server, hash, photo = upload_image(upload_url, file_name)
    owner_id, image_id = save_wall_image(
        vk_token,
        group_id,
        server,
        hash,
        photo
    )
    post_image_on_the_wall(
        vk_token,
        group_id,
        owner_id,
        image_id,
        autor_comment
    )


def get_comics():
    last_comics_num = get_last_comics_num()
    random_comics_num = random.randint(1, last_comics_num)
    url = f'https://xkcd.com/{random_comics_num}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    comics_data = response.json()

    comics_img_url = comics_data['img']
    autor_comment = comics_data['alt']

    comics_img_name = get_filename_from_url(comics_img_url)
    comics_img = get_image_by_url(comics_img_url)

    save_image(comics_img, comics_img_name)

    return comics_img_name, autor_comment


def get_last_comics_num():
    url = f'https://xkcd.com/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    return response.json()['num']


def get_image_by_url(url):
    response = requests.get(url)
    response.raise_for_status()

    return response.content


def save_image(image, filename):
    with open(filename, 'wb') as file:
        file.write(image)


def get_filename_from_url(url: str):
    img_path = urllib.parse.urlsplit(url).path

    return os.path.split(img_path)[1]


def get_upload_server_data(token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': token,
        'group_id': group_id,
        'v': '5.131'
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    server_data = response.json()['response']

    upload_url = server_data['upload_url']

    return upload_url


def upload_image(url, filename):
    with open(f'{filename}', 'rb') as file:
        files = {
            'photo': file,
        }

        response = requests.post(url, files=files)
        response.raise_for_status()

    os.remove(filename)

    upload_data = response.json()

    server = upload_data['server']
    hash = upload_data['hash']
    photo = upload_data['photo']

    return server, hash, photo


def save_wall_image(token, group_id, server, hash, photo):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': token,
        'group_id': group_id,
        'server': server,
        'hash': hash,
        'photo': photo,
        'v': '5.131'
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    image_data = response.json()['response'][0]

    owner_id = image_data['owner_id']
    image_id = image_data['id']

    return owner_id, image_id


def post_image_on_the_wall(token, group_id, owner_id, image_id, comment):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'access_token': token,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{image_id}',
        'message': comment,
        'v': '5.131'
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()


if __name__ == '__main__':
    main()

    