# 爬取控制工程全体学生的期末成绩

import requests
from requests import RequestException
import os
from hashlib import md5
from pyquery import PyQuery as pq
import tesserocr
from PIL import Image



def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = save_image(response.content)
            return image
        else:
            return None
    except RequestException:
        return None


def get_image_url(html):
    doc = pq(html)
    image_url = 'http://yjsgl.ccu.edu.cn/education/' + doc('img').attr('src')
    return image_url


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    with open(file_path, 'wb') as f:
        f.write(content)
        f.close()
    return file_path




def get_code(html):
    image_url = get_image_url(html)
    image_file_path = download_image(image_url)
    image = Image.open(image_file_path)
    image = image.convert('L')
    result = tesserocr.image_to_text(image)
    return result





