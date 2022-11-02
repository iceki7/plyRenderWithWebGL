import operator

import numpy as np
import pandas as pd

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from plyfile import PlyData, PlyElement

import os

# python manage.py runserver 0.0.0.0:8000
# 表单
import json

from plyRender.settings import BASE_DIR


def search_form(request):
    return render(request, 'search_form.html')


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'

    if 'q' in request.GET and request.GET['q']:

        # message = '数据为: ' + readPlyToNp() + request.GET['q']
        dic = readPly()
    else:
        message = '你提交了空表单'
        # return HttpResponse('hello')
    return JsonResponse(dic)


def readPly():  # 读取顶点和面，返回一个dict。
    plydata = PlyData.read(os.path.join(BASE_DIR, r'plyRender\tet.ply'))

    # print(plydata.elements[0].name)
    # print(plydata.elements[0].data[0])
    # print(plydata.elements[0].data['z'])
    # print(plydata['face'][0]['red'])
    # print(plydata['face'][0]['vertex_indices'])

    # for x in plydata.elements:
    #     print(x.name)

    vertex_np = []
    face_np = []
    print('————↓vertex↓————')
    # 传递点
    for x in plydata['vertex']:  # vertex
        print(x)
        vertex_np.append(x)

    print('————↓face↓————')
    # 传递面
    for x in plydata['face']:  # face
        print(x['vertex_indices'])
        face_np.append(x['vertex_indices'])

    # return plydata['vertex']
    print('————↓face np↓————')
    print(face_np)

    dic = {}
    for kind in (vertex_np, face_np):
        arr = []
        for x in kind:
            arr.append(list(x.tolist()))  # 类型转换 numpy obj -> tuple ->list
        arr = sum(arr, [])  # 多维转一维
        if kind is vertex_np:
            dic['vertex'] = arr
        else:
            dic['facet'] = arr

    return dic


def readPlyToNp():
    plydata = PlyData.read(os.path.join(BASE_DIR, r'plyRender\tet.ply'))
    data = plydata.elements[0].data  # 读取vertex
    print('----1↓-------')
    print(data)
    data_pd = pd.DataFrame(data)  # 转换成DataFrame, 因为DataFrame可以解析结构化的数据
    data_np = np.zeros(data_pd.shape, dtype=np.float)  # 初始化储存数据的array
    property_names = data[0].dtype.names  # 读取property的名字
    for i, name in enumerate(property_names):  # 按property读取数据，这样可以保证读出的数据是同样的数据类型。
        data_np[:, i] = data_pd[name]
    print('----numpy version↓-------')
    print(data_np)
    return data_np
