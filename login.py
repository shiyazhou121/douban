#coding=utf-8
import urllib2,urllib
import cookielib
import requests
from lxml import etree

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
    #记录cookies
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    #post包
    data = {
        'source':'music',
        'redir':'http://www.douban.com',
        'form_email':'xxxx',
        'form_password':'xxxx',
        'login':'登录'}
    url = 'https://www.douban.com'
    #登录
    post_data = urllib.urlencode(data)
    req = urllib2.Request(url,post_data,headers)
    content = opener.open(req)
    #测试
    test = 'http://www.douban.com/people/136418637/'
    text = opener.open(test).read()
    text1 = etree.HTML(text)
    test_con = text1.xpath('//head/title/text()')
    #登录成功或失败
    print '==========================================='
    if test_con[0].strip() == 'springxin':
        print u'没有验证码登录成功!'
        print '==========================================='
    else:
        print u'没有验证码登录失败!'
        print '==========================================='
        print u'重试!'
        account_login()


def account_login():
    #头文件
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'accounts.douban.com',
        'Origin':'http://www.douban.com',
        'Referer':'http://www.douban.com/login',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.3'}
    #记录cookies
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    #验证码
    url = 'http://www.douban.com/login'
    html = requests.get(url).content
    req1 = etree.HTML(html)
    con = req1.xpath('//img[@id="captcha_image"]/@src')
    con1 = req1.xpath('//input[@name="captcha-id"]/@value')
    captcha_id = str(con1[0])
    print con[0].strip()
    yanzhengma = raw_input(u'输入验证码：')
    #post包
    data = {
        'source':'index_nax',
        'redir':'http://www.douban.com',
        'form_email':'xxxxx',
        'form_password':'xxxxx',
        'captcha-solution':yanzhengma,
        'captcha-id':captcha_id,}
    url = 'https://www.douban.com'
    #登录
    post_data = urllib.urlencode(data)
    req = urllib2.Request(url,post_data,headers)
    content = opener.open(req)
    #测试
    test = 'http://www.douban.com/people/136418637/'
    text = opener.open(test).read()
    text1 = etree.HTML(text)
    test_con = text1.xpath('//head/title/text()')
    #登录成功或失败
    print '==========================================='
    if test_con[0].strip() == 'springxin':
        print u'有验证码登录成功!'
        print '==========================================='
    else:
        print u'有验证码登录失败!'
        print '==========================================='
        print u'重试!'
        account_login()

    
if __name__ =='__main__':
    account_login()
