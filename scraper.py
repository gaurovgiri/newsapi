from bs4 import BeautifulSoup
import requests
import re
import json
from hashlib import md5
import psycopg2


def scraping(site_name, site_url, title_elem, url_elem, domain, *args):
    r = requests.get(site_url)
    soup = BeautifulSoup(r.content, 'html5lib')
    titles = soup.select(title_elem)
    urls = soup.select(url_elem)
    site_json = json.loads(soup.text) if site_name == 'Ministry of Agriculture and Livestock Development' else None
    final = []
    if site_name == 'Department of Transport Management':
        i = 0
        for title, url in zip(titles, urls):
            title = titles[i].text
            hash_obj = md5(title.encode())
            md5_hash = hash_obj.hexdigest()
            news = {'source': site_name,
                    'domain': domain,
                    'title': str(title).strip(),
                    'date': str(titles[i + 1].text).strip(),
                    'news_link': str(site_url) + re.sub(r'\\', '/', str(url.get('href'))),
                    'md5': md5_hash
                    }
            i = i + 2
            final.append(news)

    elif site_name in ['Department of Immigration', 'Department of Land Management and Archive', 'Ministry of Home '
                                                                                                 'Affairs',
                       'Ministry of Communication and Information Technology']:
        for title, url in zip(titles, urls):
            hash_obj = md5(title.encode())
            md5_hash = hash_obj.hexdigest()
            news = {'source': site_name,
                    'domain': domain,
                    'title': re.sub('\t', '', str(title.text).strip().split('\n')[0]),
                    'news_link': url.get('href') if str(url.get('href')).startswith('http') else domain + str(
                        url.get('href')),
                    'md5': md5_hash
                    }
            final.append(news)

    elif site_name == 'Ministry of Agriculture and Livestock Development':
        for data in site_json['data']['dataList']:
            hash_obj = md5(data.get('title')['ne'].encode())
            md5_hash = hash_obj.hexdigest()
            news = {'source': site_name,
                    'domain': domain,
                    'title': re.sub('\t', '', str(data.get('title')['ne']).strip().split('\n')[0]),
                    'news_link': args[0] + str(data.get('slug')),
                    'md5': md5_hash
                    }
            final.append(news)

    else:
        for title, url in zip(titles, urls):
            hash_obj = md5(title.encode())
            md5_hash = hash_obj.hexdigest()
            news = {'source': site_name,
                    'domain': domain,
                    'title': str(title.text).strip(),
                    'news_link': url.get('href') if str(url.get('href')).startswith('http') else domain + str(
                        url.get('href')),
                    'md5': md5_hash
                    }
            final.append(news)

    return final


# Information about the sources

# Departments:

DOTM = {
    'site_name': 'Department of Transport Management',
    'site_url': 'https://www.dotm.gov.np',
    'title_elem': 'td',
    'url_elem': 'td > div.sectionNotice > div > a',
    'domain': 'https://www.dotm.gov.np/'
}

DOIB = {
    'site_name': 'Department of Information & Broadcasting',
    'site_url': 'http://www.doinepal.gov.np/en/',
    'title_elem': '.col-sm-10 > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > '
                  'ol:nth-of-type(1) > li > a',
    'url_elem': '.col-sm-10 > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > '
                'ol:nth-of-type(1) > li > a ',
    'domain': 'https://www.doinepal.gov.np/'
}

DOFE = {
    'site_name': 'Department of Foreign Employment',
    'site_url': 'https://dofe.gov.np/News',
    'title_elem': '.divNewsList > ul:nth-of-type(1) > li > h3:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1)',
    'url_elem': '.divNewsList > ul:nth-of-type(1) > li > h3:nth-of-type(1) > a:nth-of-type(1)',
    'date_elem': '.divNewsList > ul:nth-of-type(1) > li > p:nth-of-type(2) > span:nth-of-type(1)',
    'domain': 'https://www.dofe.gov.np/'
}

IRD = {
    'site_name': 'Inland Revenue Department',
    'site_url': 'http://ird.gov.np/',
    'title_elem': '#notice > ul:nth-of-type(1) > li > a:nth-of-type(1) > div:nth-of-type(2)',
    'url_elem': '#notice > ul:nth-of-type(1) > li:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'https://www.doinepal.gov.np/'
}

DOI = {
    'site_name': 'Department of Industry',
    'site_url': 'https://www.doind.gov.np/index.php/notice',
    'title_elem': 'article:nth-of-type(1) > h1:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': 'article:nth-of-type(1) > h1:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'https://www.doind.gov.np/'
}

DOIM = {
    'site_name': 'Department of Immigration',
    'site_url': 'https://www.immigration.gov.np/page/news',
    'title_elem': 'table.table > tbody > tr > td > a',
    'url_elem': 'table.table > tbody > tr > td > a',
    'domain': 'https://www.immigration.gov.np/'
}

DRI = {
    'site_name': 'Department of Revenue Investigation',
    'site_url': 'http://dri.gov.np/notice-board/2/2019/64281965/',
    'title_elem': '.table-striped > tbody:nth-of-type(1) > tr > td:nth-of-type(2) > a:nth-of-type(1)',
    'url_elem': '.table-striped > tbody:nth-of-type(1) > tr > td:nth-of-type(2) > a:nth-of-type(1)',
    'domain': 'http://www.dri.gov.np/'
}

DMG = {
    'site_name': 'Department of Mines and Geology',
    'site_url': 'https://www.dmgnepal.gov.np/posts',
    'title_elem': 'aside.col-md-3 > div > div > nav > a',
    'url_elem': 'aside.col-md-3 > div > div > nav > a',
    'domain': 'https://www.dmgnepal.gov.np/'
}

DCSI = {
    'site_name': 'Department of Cottage and Small Industries',
    'site_url': 'http://www.dcsi.gov.np/en/site/noticedetail',
    'title_elem': '.box > div > div > div > div > h4 > strong > a',
    'url_elem': '.box > div > div > div > div > h4 > strong > a',
    'domain': 'http://www.dcsi.gov.np/'
}

OCR = {
    'site_name': 'Office of the Company Registar',
    'site_url': 'http://ocr.gov.np/category/6',
    'title_elem': 'div.col-md-4 > div > div > div > div > a > h6',
    'url_elem': 'div.col-md-4 > div > div > div > div > a',
    'domain': 'http://www.ocr.gov.np/'
}

DOAN = {
    'site_name': 'Department of Agriculture',
    'site_url': 'http://www.doanepal.gov.np/notice-board/1/2018/51775759',
    'title_elem': '#example > tbody > tr > td:nth-of-type(2)',
    'url_elem': '#example > tbody > tr > td:nth-of-type(5) > a:nth-of-type(1)',
    'domain': 'http://www.doanepal.gov.np/'
}

PSD = {
    'site_name': 'Postal Service Department',
    'site_url': 'http://postalservice.gov.np/newslist',
    'title_elem': 'div.timeline-slide > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > '
                  'div:nth-of-type(1) > '
                  'div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': 'div.timeline-slide > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type('
                '1) > '
                'div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'http://www.postalservice.gov.np/'
}

DLS = {
    'site_name': 'Department of Livestock Services',
    'site_url': 'http://dls.gov.np/notice-board/3/2018/15159527',
    'title_elem': 'tr > td:nth-of-type(2)',
    'url_elem': 'tr > td:nth-of-type(5) > a:nth-of-type(1)',
    'domain': 'http://www.dls.gov.np/'
}

DEOC = {
    'site_name': 'Department of Co-operatives',
    'site_url': 'http://www.deoc.gov.np/english/notice-board/1/2017/61926379',
    'title_elem': '#example > tbody > tr > td:nth-of-type(2)',
    'url_elem': '#example > tbody > tr > td:nth-of-type(5) > a:nth-of-type(1)',
    'domain': 'http://www.deoc.gov.np/'
}

DFTQC = {
    'site_name': 'Department of Food Technology and Quality Control',
    'site_url': 'http://www.dftqc.gov.np/notice-board/2/2019/35918240/',
    'title_elem': '#example > tbody > tr > td:nth-of-type(2)',
    'url_elem': '#example > tbody > tr > td:nth-of-type(5) > a:nth-of-type(1)',
    'domain': 'http://www.dftqc.gov.np/'
}

DOF = {
    'site_name': 'Department of Forest and Soil Conservation',
    'site_url': 'http://dof.gov.np/notices?page=1',
    'title_elem': 'p.news_list > a:nth-of-type(1)',
    'url_elem': 'p.news_list > a:nth-of-type(1)',
    'domain': 'http://www.dof.gov.np/'
}

DOED = {
    'site_name': 'Department of Electricity Development',
    'site_url': 'http://www.doed.gov.np/pages/notices',
    'title_elem': '.lower_man_img > div > div > ul > li > a',
    'url_elem': '.lower_man_img > div > div > ul > li > a',
    'domain': 'http://www.doed.gov.np/'
}

DOA = {
    'site_name': 'Department of Archaeology',
    'site_url': 'http://www.doa.gov.np/notice-board/2/2019/64281965',
    'title_elem': '#example > tbody > tr > td:nth-of-type(2)',
    'url_elem': '#example > tbody > tr > td:nth-of-type(5) > a:nth-of-type(1)',
    'domain': 'http://www.doa.gov.np/'
}

DOR = {
    'site_name': 'Department of Roads',
    'site_url': 'https://dor.gov.np/home/news',
    'title_elem': 'article.post > h3 > a:nth-of-type(1)',
    'url_elem': 'article.post > h3 > a:nth-of-type(1)',
    'domain': 'https://www.dor.gov.np/home/'
}

DOHS = {
    'site_name': 'Department of Health Services',
    'site_url': 'http://dohs.gov.np/category/news-notice/',
    'title_elem': 'li.col-xs-12 > div:nth-of-type(1) > div:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': 'li.col-xs-12 > div:nth-of-type(1) > div:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'http://www.dohs.gov.np/'
}

DOLMA = {
    'site_name': 'Department of Land Management and Archive',
    'site_url': 'http://dolma.gov.np/office/118/allnews',
    'title_elem': '.panel-list > li',
    'url_elem': '.panel-list > li > a:nth-of-type(1)',
    'domain': 'http://www.dolma.gov.np/'
}

DONIDCR = {
    'site_name': 'Department of National Id and Civil Registration',
    'site_url': 'https://donidcr.gov.np/Download/News?id=12',
    'title_elem': 'tr > td:nth-of-type(2)',
    'url_elem': 'tr > td:nth-of-type(5) > a:nth-of-type(1)',
    'domain': 'https://www.donidcr.gov.np/'
}

DOIT = {
    'site_name': 'Department of Information Technology',
    'site_url': 'https://doit.gov.np/en/notices',
    'title_elem': '.presslist > li > div:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': '.presslist > li > div:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'https://www.doit.gov.np/'
}

# Ministries:


MOD = {
    'site_name': 'Ministry of Defence',
    'site_url': 'https://mod.gov.np/en/site/noticeall',
    'title_elem': 'div.col-md-12 > div:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': 'div.col-md-12 > div:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'http://mod.gov.np/'
}

MOHA = {
    'site_name': 'Ministry of Home Affairs',
    'site_url': 'https://www.moha.gov.np/en/page/news',
    'title_elem': '.table > tbody > tr > td:nth-of-type(2) > a:nth-of-type(1)',
    'url_elem': '.table > tbody > tr > td:nth-of-type(2) > a:nth-of-type(1)',
    'domain': 'http://moha.gov.np/'
}

MOFA = {
    'site_name': 'Ministry of Foreign Affairs',
    'site_url': 'https://mofa.gov.np/news-and-activities/',
    'title_elem': 'article > div > div > header > h1 > a',
    'url_elem': 'article > div > div > header > h1 > a',
    'domain': 'http://mofa.gov.np/'
}

MOFAGA = {
    'site_name': 'Ministry of Federal Affairs & General Administration',
    'site_url': 'https://mofaga.gov.np/archiving?_token=J3YhyV0YzUTQiYgiho1pEDUfJnKTpabzbnIS2IC9&div_section=&cat_id'
                '=&date_from=&date_to=&fiscal_year=&visible=100&q=',
    'title_elem': '.table > tbody > tr > td:nth-of-type(2) > a:nth-of-type(1)',
    'url_elem': '.table > tbody > tr > td:nth-of-type(2) > a:nth-of-type(1)',
    'domain': 'http://mofaga.gov.np/'
}

MOE = {
    'site_name': 'Ministry of Education, Science and Technology',
    'site_url': 'http://moe.gov.np/category/news.html',
    'title_elem': 'div.news > ul:nth-of-type(1) > li:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': 'div.news > ul:nth-of-type(1) > li:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'http://moe.gov.np/'
}

MOEWRI = {
    'site_name': 'Ministry of Energy, Water Resources and Irrigation',
    'site_url': 'http://www.moewri.gov.np/pages/notices',
    'title_elem': 'div.text > ul:nth-of-type(1) > li > a:nth-of-type(1)',
    'url_elem': 'div.text > ul:nth-of-type(1) > li > a:nth-of-type(1)',
    'domain': 'http://moewri.gov.np/'
}

MOALD = {
    'site_name': 'Ministry of Agriculture and Livestock Development',
    'site_url': 'https://www.moald.gov.np/api/notice/list?page=1&perpage=5&category=News',
    'news_site': 'https://www.moald.gov.np/news/detail/',
    'title_elem': 'np > td:nth-of-type(2) > span:nth-of-type(1) > span:nth-of-type(1)',
    'url_elem': 'slug > td:nth-of-type(2) > span:nth-of-type(1) > span:nth-of-type(1)',
    'domain': 'http://moald.gov.np/'
    # JSON EXTRACTED
}

MOHP = {
    'site_name': 'Ministry of Health and Population',
    'site_url': 'https://www.mohp.gov.np/en/news',
    'title_elem': '.post > header > h1 > a',
    'url_elem': '.post > header > h1 > a',
    'domain': 'http://mohp.gov.np/'
}

MOICS = {
    'site_name': 'Ministry of Industry, Commerce and Supplies',
    'site_url': 'https://moics.gov.np/en/category/notice',
    'title_elem': '.no-mar > div > div > h3',
    'url_elem': '.no-mar > div > div > div > a',
    'domain': 'http://moics.gov.np/'
}

MOCTCA = {
    'site_name': 'Ministry of Culture, Tourism and Civil Aviation',
    'site_url': 'https://www.tourism.gov.np/news',
    'title_elem': 'tr > td > a',
    'url_elem': 'tr > td > a',
    'domain': 'http://tourism.gov.np/'
}

MOLESS = {
    'site_name': 'Ministry of Labour, Employment and Social Security',
    'site_url': 'http://moless.gov.np/?page_id=1462',
    'title_elem': 'article.post > div > h4 > a',
    'url_elem': 'article.post > div > h4 > a',
    'domain': 'http://moless.gov.np/'
}

MOF = {
    'site_name': 'Ministry of Finance',
    'site_url': 'https://mof.gov.np/en/news/',
    'title_elem': 'tr.row1 > td:nth-of-type(3) > a:nth-of-type(1)',
    'url_elem': 'tr.row1 > td:nth-of-type(3) > a:nth-of-type(1)',
    'domain': 'http://mof.gov.np/'
}

MOCIT = {
    'site_name': 'Ministry of Communication and Information Technology',
    'site_url': 'https://mocit.gov.np/',
    'title_elem': 'li.d-flex > a',
    'url_elem': 'li.d-flex > a',
    'domain': 'http://mocit.gov.np/'
}

MOYS = {
    'site_name': 'Ministry of Youth and Sports',
    'site_url': 'http://moys.gov.np/',
    'title_elem': '.view-display-id-block_game > div:nth-of-type(1) > div:nth-of-type(1) > ul:nth-of-type(1) > li > '
                  'div:nth-of-type(1) > span:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': '.view-display-id-block_game > div:nth-of-type(1) > div:nth-of-type(1) > ul:nth-of-type(1) > li > '
                'div:nth-of-type(1) > span:nth-of-type(1) > a:nth-of-type(1) ',
    'domain': 'http://moys.gov.np/'
}

MOLCPA = {
    'site_name': 'Ministry of Land Managements, Cooperatives and Poverty Alleviation',
    'site_url': 'http://www.molcpa.gov.np/notices.php',
    'title_elem': '.blog-item > div > div:nth-of-type(1) > div:nth-of-type(2) > h3:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': '.blog-item > div > div:nth-of-type(1) > div:nth-of-type(2) > h3:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'http://molcpa.gov.np/'
}

MOWS = {
    'site_name': 'Ministry of Water Supply',
    'site_url': 'http://mows.gov.np/category/notice/?lang=en',
    'title_elem': 'li.custom-list-item > a:nth-of-type(1)',
    'url_elem': 'li.custom-list-item > a:nth-of-type(1)',
    'domain': 'http://mows.gov.np/'
}

MOPIT = {
    'site_name': 'Ministry of Physical Infrastructure and Transport',
    'site_url': 'http://www.mopit.gov.np/notice-board/1/2018/38194426',
    'title_elem': '.table-striped > tbody:nth-of-type(1) > tr > td:nth-of-type(2) > a:nth-of-type(1)',
    'url_elem': '.table-striped > tbody:nth-of-type(1) > tr > td:nth-of-type(2) > a:nth-of-type(1)',
    'domain': 'http://mopit.gov.np/'
}

MOUD = {
    'site_name': 'Ministry of Urban Development',
    'site_url': 'https://www.moud.gov.np/index.php',
    'title_elem': 'div.content-side > div > div > div > div > ul > li > a',
    'url_elem': 'div.content-side > div > div > div > div > ul > li > a',
    'domain': 'http://moud.gov.np/'

}

MOWCSC = {
    'site_name': 'Ministry of Women, Children and Senior Citizen',
    'site_url': 'http://mowcsc.gov.np/notice-news',
    'title_elem': 'li.col-xs-12 > div:nth-of-type(1) > div:nth-of-type(1) > a:nth-of-type(1)',
    'url_elem': 'li.col-xs-12 > div:nth-of-type(1) > div:nth-of-type(1) > a:nth-of-type(1)',
    'domain': 'http://mowcsc.gov.np/'
}

MOLJPA = {
    'site_name': 'Ministry of Law, Justice and Parliamentary Affairs',
    'site_url': 'http://www.moljpa.gov.np/category/सूचना/',
    'title_elem': '.entry-title > a:nth-of-type(1)',
    'url_elem': '.entry-title > a:nth-of-type(1)',
    'domain': 'http://moljpa.gov.np/'
}

sources = [[DOTM, DOIB, DOFE, DOI, DOIM, DRI, DMG, DCSI, OCR, DOAN, PSD, DLS, DEOC, DFTQC, DOF, DOED, DOA, DOR, DOHS,
            DOLMA, DONIDCR, DOIT],
           [MOD, MOHA, MOFA, MOFAGA, MOE, MOEWRI, MOALD, MOHP, MOICS, MOCTCA, MOLESS, MOF, MOCIT,
            MOYS, MOLCPA, MOWS, MOPIT, MOUD, MOWCSC, MOLJPA]]

# Executing
for num in range(len(sources)):
    for num2 in range(len(sources[num])):
        print(scraping(sources[num][num2]['site_name'], sources[num][num2]['site_url'], sources[num][num2]['title_elem']
                       , sources[num][num2]['url_elem'], sources[num][num2]['domain'],
                       sources[num][num2]['news_site']
                       if sources[num][num2]['site_name'] == 'Ministry of Agriculture and Livestock Development'
                       else None))


# Database Connection:
class Database:
    def __init__(self):

        try:

            self.con = psycopg2.connect(
                host="127.0.0.1",
                database="Anmup",
                user="postgres",
                password="powerful"
            )
            self.con.autocommit = True
            self.cursor = self.con.cursor()

        except:

            print("DataBase Connection Error")

    def create_table(self):
        create_table_article = "CREATE TABLE Article(id serial PRIMARY KEY, title, url, site_url, md5)"
        create_table_sites = "CREATE TABLE Article(id serial PRIMARY KEY, name, domain, app_id, app_secret)"
        create_table_sites_crawling_points = "CREATE TABLE Article(id serial PRIMARY KEY, site_url, title_element, " \
                                             "url_element) "
        command_list = [create_table_article, create_table_sites, create_table_sites_crawling_points]
        for each_command in command_list:
            self.cursor.execute(each_command)
