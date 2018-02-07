# -*- coding: utf-8 -*-
"""

    公共配置项

"""
import os

#todo 1.提取公共配置 2.页面增加信息提示
# 获取工作目录（main）的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志目录
LOG_DIR = BASE_DIR
