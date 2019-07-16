# encoding=utf-8

import requests
from selenium import webdriver
import time
from PIL import Image
import urllib2
from bs4 import BeautifulSoup
import re
import urllib
import json
import base64

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# 多点账号防止被和谐
myAccount = [
    {'no': 'konhay@sina.com', 'psw': 'Hanbing123'}#,
    #{'no': 'XXXXXXXX', 'psw': 'XXXXXXX'},
    #{'no': 'XXXXXX', 'psw': 'XXXXXXX'}
]

headers = {
    #"Host": "login.weibo.cn",
    "Host": "login.sina.com.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}


# 获取验证码等相关登录信息
def get_captchainfo(loginURL):
    html = requests.get(loginURL).content
    bs = BeautifulSoup(html)
    # print bs
    # 注意通过bs.select元素寻找对象，返回的是列表对象
    password_name = (bs.select('input[type="password"]'))[0].get('name')
    vk = (bs.select('input[name="vk"]'))[0].get('value')
    capId = (bs.select('input[name="capId"]'))[0].get('value')
    print password_name, vk, capId
    try:
        captcha_img = bs.find("img", src=re.compile('http://weibo.cn/interface/f/ttt/captcha/')).get('src')
        print captcha_img
        # captchaid可以从验证码图片地址中直接截取获得
        urllib.urlretrieve(captcha_img, 'captcha.jpg')
        print "captcha download success!"
        captcha_input = input("please input the captcha\n>")
    except:
        return None

    return (captcha_input, password_name, vk, capId)


def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    #loginURL = 'http://login.weibo.cn/login/'
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        #captcha = get_captchainfo(loginURL)
        # if captcha[0] is None:
        #     # 不需要验证码时的表单,微博移动网页版都要验证码，此处可以忽略
        #     postData = {
        #         "source": "None",
        #         "redir": "http://weibo.cn/",
        #         "mobile": account,
        #         "password": password,
        #         "login": "登录",
        #     }
        # else:
        #     # 需要验证码时的表单
        #     print "提交表单数据"
        #     postData = {
        #         "mobile": account,
        #         captcha[1]: password,
        #         "code": captcha[0],
        #         "remember": "on",
        #         "backurl": "http://weibo.cn/",
        #         "backtitle": u'微博',
        #         "tryCount": "",
        #         "vk": captcha[2],
        #         "capId": captcha[3],
        #         "submit": u'登录',
        #
        #
        #     }
        postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": base64.b64encode(account.encode(encoding="utf-8")),
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        print postData
        session = requests.Session()
        r = session.post(loginURL, data=postData)#, headers=headers)
        # 判断post过后是否跳转页面
        # time.sleep(2)
        print r.url
        # if r.url == 'http://weibo.cn/?PHPSESSID=&vt=1' or r.url == 'http://weibo.cn/?PHPSESSID=&vt=4':

        jsonStr = r.content.decode('gbk')
        info = json.loads(jsonStr)
        print info
        #{u'reason': u'\u8bf7\u8f93\u5165\u6b63\u786e\u7684\u767b\u5f55\u540d', u'retcode': u'20'}
        #请输入正确的登录名

        if info["retcode"] == "0":
            ceshihtml = requests.get(r.url).content
            print ceshihtml
            print 'Login successfully!!!'
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
        else:
            print "login failed!"

    return cookies


#通过selenium driver方式获取cookie
def getcookieByDriver(weibo):
    driver = webdriver.Firefox()
    driver.maximize_window()
    cookies = []
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        driver.get('https://weibo.cn')
        elem_user = driver.find_element_by_name("mobile")
        elem_user.send_keys(account)  # 用户名
        #微博的password有加后缀,
        elem_pwd = driver.find_element_by_name("password_XXXX")
        elem_pwd.send_keys(password)  # 密码
        time.sleep(10)
        #手动输验证码时间
        elem_sub = driver.find_element_by_name("submit")
        elem_sub.click()  # 点击登陆
        time.sleep(2)
        weibo_cookies = driver.get_cookies()
        #cookie = [item["name"] + "=" + item["value"] for item in douban_cookies]
        #cookiestr = '; '.join(item for item in cookie)
        cookies.append(weibo_cookies)
    return cookies


def get_cookie_from_weibo(weibo):
    #driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    cookies = []
    driver.get('https://weibo.cn')
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        #assert "微博" in driver.title
        login_link = driver.find_element_by_link_text('登录')
        ActionChains(driver).move_to_element(login_link).click().perform()
        login_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "loginName"))
        )
        login_name = driver.find_element_by_id("loginName")
        login_password = driver.find_element_by_id("loginPassword")
        login_name.send_keys(account)
        login_password.send_keys(password)
        login_button = driver.find_element_by_id("loginAction")
        login_button.click()
        time.sleep(10)
        cookie = driver.get_cookies()
        cookies.append(cookie)
    driver.close()
    return cookies


#cookies = getCookies(myAccount)
#cookies = getcookieByDriver(myAccount)
cookies = get_cookie_from_weibo(myAccount)
print "Get Cookies Finish!( Num:%d)" % len(cookies)