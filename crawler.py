# -*- coding: utf-8 -*-  
__author__ = 'KentChum'

from selenium import webdriver
from bs4 import BeautifulSoup
import os, thread, time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def run():
    suffix_dict = {0: 'com', 1: 'net', 2: 'me', 3: 'xyz', 4: 'cc', 5: 'im', 6: 'org', 7: 'io', 8: 'info', 9: 'name',
                   10: 'co', 11: 'tw', 12: 'cn', 13: 'com.cn', 14: 'mobi', 15: 'asia', 16: 'hk', 17: 'aero', 18: 'ca',
                   19: 'us', 20: 'fr', 21: 'se', 22: 'ie', 23: 'tv', 24: 'biz', 25: 'pro', 26: 'in', 27: 'nu', 28: 'ch',
                   29: 'ws', 30: 'be', 31: 'la', 32: 'wang'}

    word_dict = {1: '拼音字典', 3: '一位数字', 4: '二位数字', 5: '三位数字', 6: '一位字母', 7: '二位字母',
                 11: '英文单词', 111: '一位拼音', 112: '二位拼音', 113: '三位拼音', 114: '四位拼音'}

    suffix_dict = {7: 'io', 26: 'in'}
    word_dict = {3: '一位数字', 4: '二位数字'}

    driver = webdriver.PhantomJS(executable_path='./drivers/phantomjs')

    # 后缀
    for suffix_idx in suffix_dict:
        # print suffix_dict[suffix_value]
        f = open('temp/' + suffix_dict[suffix_idx] + '.txt', 'a')
        f.truncate()
        do_job(driver, f, suffix_idx, word_dict)
        f.close()

    print('Done!')


def do_job(driver, file, suffix_idx, word_dict):
    # group_filter(driver, file, suffix_idx, word_dict)
    single_filter(driver, file, suffix_idx, word_dict)


def single_filter(driver, file, suffix_idx, word_dict):
    for word_idx in word_dict:
        file.write(word_dict[word_idx] + '\r\n\r\n')

        query_url = 'http://www.qiuyumi.org/domain/?q=&d=%d&h=&s=%d' % (word_idx, suffix_idx)
        print query_url

        driver.get(query_url)
        time.sleep(300)
        driver.save_screenshot('./temp/single.png')

        html = driver.page_source
        soup = BeautifulSoup(html)

        domain_list = soup.find('ul', {'id': 'domainlist'}).findAll('li', {'class': 'onedomain'})
        for d in domain_list:
            reg_status = d.find('img', {'class': 'img-ava'})
            domain_name = d.find('div', {'class': 'domainname'})
            if reg_status:
                # print reg_status
                domain = domain_name.text.strip()
                status = d.find('div', {'class': 'avatips'}).find('span').previous_sibling
                line = status + '\t' + domain + '\r\n'
                print line
                file.write(line)

        file.write('\r\n\r\n')


def group_filter(driver, file, suffix_idx, word_dict):
    urls = get_url_by_generator(suffix_idx, word_dict)
    for u in urls:
        climb(driver, u['title'], u['url'], 1)


def get_url_by_generator(suffix_idx, word_dict):
    urls = []
    for d1 in word_dict:
        for d2 in word_dict:
            url_str = 'http://www.qiuyumi.org/dict2/?n1=&d1=%d&n2=&d2=%d&n3=&s=%d&p=' % (d1, d2, suffix_idx)
            url = {'title': word_dict[d1] + ' + ' + word_dict[d2], 'url': url_str}
            urls.append(url)

    return urls


def climb(driver, title, base_url, page=1):
    url = base_url + str(page)
    print url
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)

    domain_list = soup.find('ul', {'id': 'domainlist'}).findAll('li', {'class': 'onedomain'})
    if len(domain_list) > 1:
        for d in domain_list:
            reg_status = d.find('img', {'class': 'img-ava'})
            domain_name = d.find('div', {'class': 'domainname'})
            if reg_status:
                # print reg_status
                domain = domain_name.text.strip()
                status = d.find('div', {'class': 'avatips'}).find('span').previous_sibling
                line = status + '\t' + domain + '\r\n'
                print line
                file.write(line)
        file.write('\r\n\r\n')
        next_page = page + 1
        climb(driver, title, base_url, next_page)


def test(driver):
    url = 'http://www.qiuyumi.org/dict2/?n1=&d1=113&n2=&d2=114&n3=&s=7&p=105'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)

    domain_list = soup.find('ul', {'id': 'domainlist'}).findAll('li', {'class': 'onedomain'})
    print len(domain_list)
    if len(domain_list) > 1:
        print 'got'
    else:
        print 'none'
    exit()


run()
