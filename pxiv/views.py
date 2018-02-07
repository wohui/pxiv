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

    @api_view(['POST'])
    @permission_classes([permissions.AllowAny, ])
    def get_data(request):
        if request.method == 'POST':
            json_str = (request.body)
            url = "https://api.imjad.cn/interface/img/PixivProxy.php"
            headers = {
                "authority": "api.imjad.cn",
                "method": "GET",
                "path": "/interface/img/PixivProxy.php?url=https://i.pximg.net/c/480x960/img-master/img/2017/12/28/20/21/14/66505036_p0_master1200.jpg",
                "scheme": "https",
                "accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "referer": "https://api.imjad.cn/pixiv.md",
            }
            data = {
                "url": "https://i.pximg.net/c/480x960/img-master/img/2017/12/28/20/21/14/66505036_p0_master1200.jpg",
            }
            res_img = requests.get(url, data, headers=headers, verify=False)
            base64_res = base64.b64encode(res_img.content).decode('ascii')
            # 获取一言
            hitoko_url = "https://sslapi.hitokoto.cn/"
            hitoko_data = {
                "c": "c"
            }
            hitoko_res = requests.get(hitoko_url, hitoko_data, verify=False)
            LOGGER.info(hitoko_res.text)
            res = {}
            data = {}
            data['imgData'] = base64_res
            data['hitoko'] = json.loads(hitoko_res.text)
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
