import requests

from collage_diffusion.utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '740ebedcdd864159'
# 您的应用密钥
APP_SECRET = 'lrEwNGzjgEIuNRIJNPWijYQq0YKCAtRr'


def createRequest(text):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    q = text
    lang_from = 'zh-CHS'
    lang_to = 'en'
    vocab_id = '1'

    data = {'q': q, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post').json()
    return res["translation"][0]
    # print(res.text)
    # print(str(res.content, 'utf-8'))


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == '__main__':
    createRequest('【背景】')
