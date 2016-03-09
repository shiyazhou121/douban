#coding=utf-8
import urllib2,urllib
import cookielib
import requests
import re
import time
import random
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#记录cookies
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
urllib2.install_opener(opener)

#登陆函数
def login():
    
    #头文件
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cookie':'bid="PCfWm4daTbM"; ll="108288"; ps=y; ct=y; ue="289761386@qq.com"; push_noty_num=0; push_doumail_num=0',
        'Host':'accounts.douban.com',
        'Origin':'http://www.douban.com',
        'Referer':'http://www.douban.com/login',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.3'}

    #得到是否需要输入验证码
    url = 'http://www.douban.com/login'
    html = requests.get(url).content
    req1 = etree.HTML(html)
    iscon = req1.xpath('//div1[@class="item item-captcha"]/label/text()')

    #判断是否需要输入验证码
    if len(iscon)==0:
        #无验证码post包
        data = {
            'source':'music',
            'redir':'http://www.douban.com',
            'form_email':'xxxxxx',
            'form_password':'xxxxxx',
            'login':'登录'}
    else:
        con = req1.xpath('//img[@id="captcha_image"]/@src')
        con1 = req1.xpath('//input[@name="captcha-id"]/@value')
        captcha_id = str(con1[0])
        print con[0].strip()
        yanzhengma = raw_input(u'输入验证码：')

        #有验证码post包
        data = {
            'source':'music',
            'redir':'http://www.douban.com',
            'form_email':'xxxxx',
            'form_password':'xxxxxx',
            'captcha-solution':yanzhengma,
            'captcha-id':captcha_id,
            'login':'登录'}

    #登录
    post_data = urllib.urlencode(data)
    req = urllib2.Request(url,post_data,headers)
    content = opener.open(req)

    #登录成功或失败
    test = 'http://www.douban.com/people/136418637/'
    text = opener.open(test).read()
    text1 = etree.HTML(text)
    test_con = text1.xpath('//head/title/text()')
    print text
    print '==========================================='
    if test_con[0].strip() == 'xxxxxx':
        print u'登录成功!'
        print '==========================================='
    else:
        print u'登录失败!'
        print '==========================================='
        time.sleep(5)
        print u'重试!'
        print '==========================================='


if __name__ =='__main__':
    login()     



    
