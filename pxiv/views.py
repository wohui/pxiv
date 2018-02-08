from django.shortcuts import render

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from utils.logger import LOGGER
from django.http import JsonResponse
import requests
import json
import base64


# Create your views here.
# 处理部分
class restful(APIView):
    def index(request):
        return render(request, "pxiv/index.html")

    # 获取图片url
    @api_view(['POST'])
    @permission_classes([permissions.AllowAny, ])
    def get_img_data(request):
        if request.method == 'POST':
            # 获取10个img_url
            pxiv_url = "https://api.imjad.cn/pixiv/v1/"
            pxiv_data = {
                "type": "search",
                "per_page": 10,
                "word": "香風智乃 1000users入り",
                "page": 1,
            }
            pxiv_res = requests.get(pxiv_url, pxiv_data, verify=False)
            json_obj = json.loads(pxiv_res.text)
            data = []
            for i in range(0, 1):
                pxiv_img_url = json_obj['response'][i]['image_urls']['px_480mw']
                pxiv_img_base64_data = "data:image/jpeg;base64," + get_img_base64_data(pxiv_img_url)
                data.append(pxiv_img_base64_data)
            res = {}
            if data:
                res['msg'] = "获取图片成功"
                res['status'] = True
                LOGGER.info("获取图片成功")
            else:
                res['msg'] = "获取图片失败"
                res['status'] = False
                LOGGER.error("获取图片失败")
            response_data = {"msg": res['msg'], "status": res['status'], "data": data}
            return JsonResponse(response_data)

    @api_view(['POST'])
    @permission_classes([permissions.AllowAny, ])
    def get_hito_data(request):
        if request.method == 'POST':
            # 获取一言
            hitoko_url = "https://sslapi.hitokoto.cn/"
            hitoko_data = {
                "c": "c"
            }
            data = []
            for i in range(0, 1):
                hitoko_res = requests.get(hitoko_url, hitoko_data, verify=False)
                json_obj = json.loads(hitoko_res.text)
                if json_obj:
                    hito_text = json_obj['hitokoto']
                    LOGGER.info(hito_text)
                    data.append(hito_text)
            res = {}
            if data:
                res['msg'] = "获取一言完成"
                res['status'] = True
                LOGGER.info("获取一言完成")
            else:
                res['msg'] = "获取一言失败"
                res['status'] = False
                LOGGER.error("获取一言失败")
            response_data = {"msg": res['msg'], "status": res['status'], "data": data}
            return JsonResponse(response_data)


# 通过imjad代理获取图片数据
def get_img_base64_data(pxiv_img_url):
    imjad_url = "https://api.imjad.cn/interface/img/PixivProxy.php"
    headers = {
        "authority": "api.imjad.cn",
        "method": "GET",
        "path": "/interface/img/PixivProxy.php?url=" + pxiv_img_url,
        "scheme": "https",
        "accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "https://api.imjad.cn/pixiv.md",
    }
    data = {
        "url": pxiv_img_url,
    }
    res_img = requests.get(imjad_url, data, headers=headers, verify=False)
    base64_res = base64.b64encode(res_img.content).decode('ascii')
    return base64_res
