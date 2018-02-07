# -*- coding: utf-8 -*-
"""
    http client
"""
import requests
from utils.logger import LOGGER

DEFAULT_HEADER = {
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

COOKIES = {}


def get_response(req_type="POST", url=None, data=None, headers=DEFAULT_HEADER, cookies=COOKIES):
    """ http请求 """
    LOGGER.info(url + " " + str(data) + " " + str(COOKIES))
    try:
        if req_type.upper() == "POST":

            r = requests.post(url=url, data=data, headers=headers, allow_redirects=True, cookies=cookies)

        elif req_type.upper() == "GET":
            param_list = []
            for key, value in data.items():
                param_list.append(key + "=" + value)
            r = requests.get(url=url + "?" + "&".join(param_list), data={}, headers=headers, allow_redirects=True,
                             cookies=cookies)
        else:
            raise TypeError("http method error")
    except (requests.exceptions.ConnectionError, TypeError) as e:
        LOGGER.error("send request fail " + str(e))
        return None

    if r.status_code == requests.codes.ok:
        # LOGGER.info(r.text)
        # 更新cookies
        if len(r.cookies) != 0:
            COOKIES.update(r.cookies)
        for res in r.history:
            if len(res.cookies) != 0:
                COOKIES.update(res.cookies)

        return r.text
    else:
        LOGGER.error("status code " + str(r.status_code))
        return None


if __name__ == '__main__':

    pass
    # data = {"loginId": "xuser11111", "password": "Zc123456"}
    # get_response(req_type="POST", url="http://admintest03.10101111.com/ucaradmin/system/login.login", data=data)
