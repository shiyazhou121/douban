#coding=utf-8
import urllib2,urllib
import cookielib
import requests
import re
import time
from lxml import etree

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
    url = 'https://accounts.douban.com/login'
    html = requests.get(url).content
    req1 = etree.HTML(html)
    iscon = req1.xpath('//div[@class="item item-captcha"]/label/text()')


    #判断是否需要输入验证码
    if len(iscon)==0:
        #无验证码post包
        print u'无验证码'
        data = {
            'source':'music',
            'redir':'http://www.douban.com',
            'form_email':'xxxxxx',
            'form_password':'xxxxxx',
            'login':'登录'}
    else:
        print u'有验证码'
        con = req1.xpath('//img[@id="captcha_image"]/@src')
        con1 = req1.xpath('//input[@name="captcha-id"]/@value')
        captcha_id = str(con1[0])
        print con[0].strip()
        yanzhengma = raw_input(u'输入验证码：')
        #有验证码post包
        data = {
            'source':'music',
            'redir':'http://www.douban.com',
            'form_email':'xxxxxx',
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
    if test_con[0].strip() == 'springxin':
        print u'登录成功!'
        print '==========================================='
    else:
        print u'登录失败!8秒后重试'
        print '==========================================='
        time.sleep(8)
        print u'重试!'
        login()
        print '==========================================='

def crawler(url):
    time.sleep(1)
    con1 = opener.open(url).read()
    con = etree.HTML(con1)
    return con
 
def get_address(url):
    con = crawler(url)
    content = con.xpath('//div[@class="user-info"]/a/text()')
    if len(content) ==0:
        return ''
    else:
        return content[0].strip().encode('utf-8')
    
def get_donething(url):
    doneurl = 'http://www.douban.com/thing/people/'+url[29:]+'done'
    con = crawler(doneurl)
    content = con.xpath('//li[@class="exp-name"]/a/text()')
    if len(content)==1:
        return content[0].strip().encode('utf-8')
    else:
        ucontent = ' '.join(content)
        return ucontent.encode('utf-8')
    
def get_wishthing(url):
    doneurl = 'http://thing.douban.com/thing/people/'+url[29:]+'wish'
    con = crawler(doneurl)
    content = con.xpath('//li[@class="exp-name"]/a/text()')
    if len(content)==1:
        return content[0].strip().encode('utf-8')
    else:
        ucontent = ' '.join(content)
        return ucontent.encode('utf-8')
    
def get_moviemark(url):
    markurl = 'http://movie.douban.com/people/'+url[29:]+'collect'
    con = crawler(markurl)
    content = con.xpath('//li[@class=" clearfix"]/a/text()|//li[@class=" clearfix"]/span/text()')
    if content =='':
        return ''
    elif len(content)<40:
        strli = ' '.join(content)
    else:
        content1 = content[:40]
        strli = ' '.join(content1)
    return strli.encode('utf-8')

def get_wishmoviemark(url):
    markurl = 'http://movie.douban.com/people/'+url[29:]+'wish'
    con = crawler(markurl)
    content = con.xpath('//li[@class=" clearfix"]/a/text()|//li[@class=" clearfix"]/span/text()')
    if content =='':
        return ''
    elif len(content)<40:
        strli = ' '.join(content)
    else:
        content1 = content[:40]
        strli = ' '.join(content1)
    return strli.encode('utf-8')

if __name__ =='__main__':

    count = 6692
    files = open('people_url.txt','r').readlines()
    for line in files[6692:]:
        try:
            url = line.strip()
            address = get_address(url)
            donething = get_donething(url)
            wishthing = get_wishthing(url)
            moviemark = get_moviemark(url)
            wishmoviemark = get_wishmoviemark(url)
            f = open('person.txt','a+')
            f.write(url+'|'+address.replace('|',' ')+'|'+donething.replace('|',' ')+'|'+wishthing.replace('|',' ')+'|'+moviemark.replace('|',' ')+'|'+wishmoviemark.replace('|',' ')+'\n')
            f.close()
        except Exception:
            f1 = open('person_error.txt','a+')
            f1.write(url+' : '+str(count)+'\n')
            f1.close()
        print 'this is end!: %d' %count
        count = count +1
        time.sleep(3)
    print 'all is end!'

        
