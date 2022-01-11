import execjs
import requests
import re


def GetCk():
    url = 'https://www.mafengwo.cn/u/nopa13.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    ck = re.findall('document.cookie=(.*?)location\.href', res.text)[0]
    js_join = '''
        function test(){
            var c = %s
            return c
        }
    ''' % ck
    ex = execjs.compile(js_join).call('test')
    res_ck = '__jsluid_s=' + res.cookies.items()[0][1]
    item = {
        '__jsluid_s': res_ck,
        '__jsl_clearance_s': ex
    }
    return item


def GetBth(ck):
    cks = ck['__jsl_clearance_s'].split(';')
    url = 'https://www.mafengwo.cn/u/nopa13.html'
    headers = {
        'Referer': 'https://www.mafengwo.cn/u/nopa13.html',
        'cookie': cks[0] + ';' + ck['__jsluid_s'],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res = res.text.replace('<script>', '').replace('</script>', '')
    cookies = '''
        window = this;
        navigator = {
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        }
        document = {
            cookie:'',   
        }
        location = {}
        setTimeout = function(x1, x2) {
            x1();
        };
        %s
        function test(){
            var aaa = document.cookie;
            return aaa
        }
    ''' % res
    ex = execjs.compile(cookies).call('test').split(';')[0]
    return ex


def GetHtml(jsluid_s, __jsl_clearance_s):
    url = 'https://www.mafengwo.cn/u/nopa13.html'
    headers = {
        'Referer': 'https://www.mafengwo.cn/u/nopa13.html',
        'cookie': __jsl_clearance_s + ';' + jsluid_s,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    print(headers)
    res = requests.get(url, headers=headers)
    print(res.text)


if __name__ == '__main__':
    ck = GetCk()
    bts = GetBth(ck)
    GetHtml(ck['__jsluid_s'], bts)
