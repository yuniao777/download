
import requests
import json
from os import path, makedirs, system, getcwd
import shutil


sd = path.join(path.dirname(getcwd()), 'stable-diffusion-webui')

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

def downloadModels():
    m = path.join(path.dirname(getcwd()), 'stable-diffusion-webui', 'models')
    f = open('./models.json', encoding='utf-8')
    content = f.read()
    f.close()
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

def ignoreStyleFile(path, files):
    if files.count('style.css') > 0:
        return ['style.css']
    return []

def donwloadPlugin():
    f = open('./plugin.json', encoding='utf-8')
    content = f.read()
    f.close()
    plugins = json.loads(content)
    for plugin in plugins:
        url = plugin['url']
        p = plugin['path']
        if url[0:8] == 'https://':
            pdir = path.dirname(p)
            if not pdir == '' and not path.exists(pdir):
                makedirs(pdir, exist_ok=True)
            system('git clone ' + url + ' ' + p)
        if path.dirname(p) == '':
            dst = sd
        else :
            dst = path.join(path.dirname(getcwd()), p)
        shutil.copytree(p, dst, dirs_exist_ok=True, ignore=ignoreStyleFile)

def applyConfig():
    # 将默认语言改成中文
    f = open('./ui_setting.json', encoding='utf-8', mode='r')
    content = f.read()
    f.close()
    f = open(path.join(sd, 'config.json'), encoding='utf-8', mode='w+')
    f.write(content)
    f.close()

def applyAutoTag():
    t = path.join(sd, 'extensions', 'tag-autocomplete', 'tags')
    if path.exists(t):
        shutil.copy('zh_cn.csv', t)
    t = path.join(sd, 'extensions', 'sdweb-easy-prompt-selector', 'tags')
    if path.exists(t):
        shutil.copytree('sdweb-easy-prompt-selector-tags', t, dirs_exist_ok=True)

downloadModels()
donwloadPlugin()
applyAutoTag()
applyConfig()

# 常用插件列表
# https://gitee.com/akegarasu/sd-webui-extensions/raw/master/index.json