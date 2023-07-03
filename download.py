
import requests
import json
from os import path, makedirs


def getSize(length):
    utils = ['b', 'kb', 'Mb', 'Gb']
    idx = 0
    while length > 1024:
        idx += 1
        length = length/1024
    length = int(length*100)/100
    if (idx >= len(utils)):
        idx = len(utils) - 1
    return str(length) + utils[idx]

# print(getSize(10000))
m = path.join(path.curdir, '..', 'stable-diffusion-webui', 'models')
f = open('./models.json', encoding='utf-8')
content = f.read()
modelsConfig = json.loads(content)
for info in modelsConfig:
    name = info['name']
    type = info['type']
    p = path.join(m, type, name)
    makedirs(path.dirname(p), exist_ok=True)
    res = requests.get(info['url'], stream=True)
    fileLength = int(res.headers['Content-Length'])
    if path.exists(p):
        if fileLength == path.getsize(p):
            print(p+" is exists")
            continue
    contentLength = 0
    with open(r''+p, 'wb') as pyFile:
        for chunk in res.iter_content(chunk_size=1024*8*10):
            if chunk:
                contentLength += len(chunk)
                pyFile.write(chunk)
                print('\r当前下载: '+name+" 进度:%s/%s     "%(getSize(contentLength), getSize(fileLength)), flush=True, end='')
    print()