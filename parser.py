# -*- coding: utf-8 -*-
#!/usr/bin/env python


from urllib.request import urlopen
from urllib.parse import urljoin
from lxml.html import fromstring
from lxml import etree
import csv


URL = 'http://www.topinteractiveagencies.com/'
ITEM_PATH = '.sf-menu .menu-item-has-children'
COMPANY_PATH = '.articlecontainer .indextitle'
INFO_PATH = '.blogcontent'
PAGE_PATH = '.pagination'


def parselinks():
    f = urlopen(URL)
    list_html = f.read().decode('utf-8',errors='ignore')
    list_doc = fromstring(list_html)

    for elem in list_doc.cssselect(ITEM_PATH):
        a = elem.cssselect('a')[0]
        href = a.get('href')
        qpage = pagination(href)+1

        for i in range(1,qpage):
            new_href = href + 'page/'+str(i)+'/'
            #print new_href
            details_html = urlopen(new_href).read().decode('utf-8',errors='ignore')
            try:
                details_doc = fromstring(details_html)
                #print details_doc
            except XMLSyntaxError:
                continue
            for company_elem in details_doc.cssselect(COMPANY_PATH):
                _a = company_elem.cssselect('a')[0]
                company_link = _a.get('href')
                name = _a.text
                #print company_link
                #print name

		#create the dictionary
		#result = {'name':name, 'link':company_link]

                infos = get_info(company_link)
                projects = dictionary(name, company_link, infos)
                save(projects,'companies_info.csv')




def dictionary(name,link,infos):
    projects = []
    projects.append({
        'name':name,
        'link':link,
        'info':infos
    })
    return projects

def save(projects, path):
    with open(path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Название','Ссылка','Информация'))
        for project in projects:
            writer.writerow((project['name'],project['link'],', '.join(project['info'])))



def get_info(company_link):
    company_info_html = urlopen(company_link).read().decode('utf-8',errors = 'ignore')
    company_info_doc= fromstring(company_info_html)
    info_len = len(company_info_doc.xpath('.//div[@class="blogcontent"]/p'))
    #print(info_len)
    info_elems = company_info_doc.xpath('.//div[@class="blogcontent"]/p')
    infos = [info_elem.text_content() for info_elem in info_elems ]
    return infos

    #add key and value
    #result['info'] = info

'''
    for key in range(0,info_len):
        print(company_info_doc.xpath('.//div[@class="blogcontent"]/p')[key].text_content())
'''


def pagination(href):
    details_html = urlopen(href).read().decode('utf-8',errors='ignore')
    details_doc = fromstring(details_html)
    num = details_doc.cssselect(PAGE_PATH)[0].cssselect('a')[2].text
    if num=='Next »':
        num = details_doc.cssselect(PAGE_PATH)[0].cssselect('a')[1].text
    else:
        return int(num)

    return int(num)


def main():
    parselinks()

if __name__ == '__main__':
    main()
