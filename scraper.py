import re
import os
import time
import math
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


def is_valid_date(year, month, day):
    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year%4==0 and (year%100 != 0 or year%400==0):
        day_count_for_month[2] = 29

    return (1 <= month <= 12 and 1 <= day <= day_count_for_month[month]) 

def is_valid_period(start_date, end_date):
    s_day, s_month, s_year = map(int, start_date.split('/')) 
    e_day, e_month, e_year = map(int, end_date.split('/'))

    if s_year != e_year:
        if e_year > s_year:
            return True
    elif s_month != e_month:
        if e_month > s_month:
            return True 
    elif s_day != e_day:
        if e_day > s_day:
            return True
    elif s_day == e_day and s_month == e_month and s_year == e_year:
        return True

def in_date_start():
    s_date = input("Tanggal awal  (dd/mm/yyyy): ")

    if not re.match(r'\d{2}/\d{2}/\d{4}$', s_date):
        os.system('cls')
        print("[Format penulisan tanggal salah!]")
        time.sleep(0.5)
        os.system('cls')
        s_date = in_date_start()
    
    day, month, year = map(int, s_date.split('/'))
    if not is_valid_date(year, month, day):
        os.system('cls')
        print("[Tanggal tidak valid!]")
        time.sleep(0.5)
        os.system('cls')
        s_date = in_date_start()

    return s_date

def in_date_end(date_start):
    e_date = input("Tanggal akhir (dd/mm/yyyy): ")

    if not re.match(r'\d{2}/\d{2}/\d{4}$', e_date):
        os.system('cls')
        print("[Format penulisan tanggal salah!]")
        time.sleep(0.5)
        os.system('cls')
        e_date = in_date_end() 

    day, month, year = map(int, e_date.split('/'))
    if not is_valid_date(year, month, day):
        os.system('cls')
        print("[Tanggal tidak valid!]")
        time.sleep(0.5)
        os.system('cls')
        e_date = in_date_end(date_start)

    if not is_valid_period(date_start, e_date):
        os.system('cls')
        print("[Tanggal akhir harus lebih besar dari tanggal awal!]")
        time.sleep(0.5)
        os.system('cls')
        e_date = in_date_end(date_start)

    return e_date

def detikcom_url(query, category_id, date_start, date_end, pages_num=1):
    url = f"https://www.detik.com/search/searchnews?query={query}&siteid={category_id}&sortby=time&fromdatex={date_start}&todatex={date_end}&page={pages_num}&result_type=latest"
    response = requests.get(url)
    page = bs(response.content, "html.parser")

    return page

def last_page_article_count(query, category_id, date_start, date_end, page_num):
    last_page = detikcom_url(query, category_id, date_start, date_end, page_num)
    article_list = last_page.find("div", {"class": "list-content"})
    
    if article_list:
        articles = article_list.find_all('article', class_='list-content__item')
        
    article_count = len(articles)

    return article_count


def detikcom_search_results(query, category_id, date_start, date_end):
    page = detikcom_url(query, category_id, date_start, date_end)

    pagination = page.find("div", {"class": "pagination"})
    if pagination:
        page_numbers = pagination.find_all('a', class_='pagination__item')
        if page_numbers:
            last_page_number = int(page_numbers[-2].text)
        
        last_page_articles = last_page_article_count(query, category_id, date_start, date_end, last_page_number)

        num = (last_page_number - 1) * 10 + last_page_articles 
    else: 
        num = 0
        last_page_number = 1

    if num == 0:
        print(f'Tidak ditemukan artikel mengenai "{query}".')
        return num, last_page_number
    elif num > 9:
        print(f"Jumlah artikel yang ditemukan: {num}")
        return num, last_page_number
    else:
        print(f"Jumlah artikel yang ditemukan: {num}")
        return num, last_page_number

def detikcom_article_need(num_result, last_page):
    try:
        number_need = int(input("Masukkan jumlah artikel yang ingin diekstrak: "))
    except ValueError:
        print("Masukkan angka!")
        number_need, pages = detikcom_article_need(num_result)

    if number_need < 0:
        print("Jumlah artikel minimal 1.")
        number_need, pages = detikcom_article_need(num_result)
    elif number_need > num_result:
        print("Permintaan melebihi hasil pencarian. Mohon kurangi jumlah permintaan.")
        number_need, pages = detikcom_article_need(num_result)
    else:
        pages = last_page

    return number_need, pages

def detikcom_get_content(article_url):
    response = requests.get(article_url)
    content_page = bs(response.content, "html.parser")

    content_list = []
    multiple_page = content_page.find("div", {"class": "detail__multiple"})
    if multiple_page:
        multiple_page = [x.get("href") for x in multiple_page.find_all("a")][:-1]
        for page in multiple_page:
            response = requests.get(page)
            content_page = bs(response.content, "html.parser")
            content_list.extend([p.get_text() for p in content_page.find_all("p") if not p.get_text().startswith('\n\n\n\nHalaman\n\n') and
                                p.get_text() not in ['',
                                                     '[Gambas:Instagram]',
                                                     '[Gambas:Video 20detik]',
                                                     '\r\nADVERTISEMENT\r\n',
                                                     '\r\n    ADVERTISEMENT\r\n',
                                                     '\r\n    ADVERTISEMENT\r\n  ',
                                                     '\r\n   ADVERTISEMENT\r\n  ',
                                                     '\r\n   ADVERTISEMENT\r\n',
                                                     '\r\n        SCROLL TO RESUME CONTENT\r\n  ',
                                                     'Selengkapnya di halaman selanjutnya.',
                                                     '\n\t\t\t\t\tAyo share cerita pengalaman dan upload photo album travelingmu di sini.\n\n\t\t\t\t\t\t\t\t\t\t\tSilakan Daftar atau Masuk\n']])
    else:
        content_list.extend([p.get_text() for p in content_page.find_all("p")
                            if p.get_text() not in ['',
                                                    '[Gambas:Instagram]',
                                                    '[Gambas:Video 20detik]',
                                                    '\r\nADVERTISEMENT\r\n',
                                                    '\r\n    ADVERTISEMENT\r\n',
                                                    '\r\n    ADVERTISEMENT\r\n  ',
                                                    '\r\n   ADVERTISEMENT\r\n  ',
                                                    '\r\n   ADVERTISEMENT\r\n',
                                                    '\r\n        SCROLL TO RESUME CONTENT\r\n  ',
                                                    '\n\t\t\t\t\tAyo share cerita pengalaman dan upload photo album travelingmu di sini.\n\n\t\t\t\t\t\t\t\t\t\t\tSilakan Daftar atau Masuk\n']])

    content_list = '\n\n'.join(content_list)

    return content_list

def detikcom_advertorial_check(article_url):
    response = requests.get(article_url)
    content_page = bs(response.content, "html.parser")

    author = content_page.find("meta", {"content": "Advertorial"})

    if author:
        return True
    else:
        return False

def detikcom_articles(query, category_id, from_date, to_date, ads_article, article_content):
    results_num, last_page = detikcom_search_results(query, category_id, from_date, to_date)
    article_lists = []

    if results_num == 0:
        article_lists = []
        data = pd.DataFrame(article_lists, columns=["title", "category", "publish_date", "article_url", "content"])
    else:
        number_need, pages = detikcom_article_need(results_num, last_page)
        print(f"Mengekstrak {number_need} artikel ...")

        for i in range(1, pages+1):
            page = detikcom_url(query, category_id, from_date, to_date, i)
            articles = page.find_all("article", class_="list-content__item")

            for article in articles:
                title = article.find("a", {"class": "media__link"}).get('dtr-ttl')
                category = article.find('h2', class_='media__subtitle').text.strip()
                publish_date = article.find('span', title=True).get('title')
                article_url = article.find("a", {"class": "media__link"}).get('href')

                if ads_article and detikcom_advertorial_check(article_url):
                    continue
                else:
                    if article_content:
                        content = detikcom_get_content(article_url)
                        if any(title in existing_article["title"] for existing_article in article_lists) or any(content in existing_article["content"] for existing_article in article_lists):
                            continue
                        else:
                            article_lists.append({
                                "title": title,
                                "category": category,
                                "publish_date": publish_date,
                                "article_url": article_url,
                                "content": content
                            })
                    else:
                        if any(title in existing_article["title"] for existing_article in article_lists):
                            continue
                        else:
                            article_lists.append({
                                "title": title,
                                "category": category,
                                "publish_date": publish_date,
                                "article_url": article_url
                            })
                if len(article_lists) == number_need:
                    break
            if len(article_lists) == number_need:
                break
        print(f"Selesai mengekstrak {len(article_lists)} artikel.")
        data = pd.DataFrame(article_lists)

    return data, len(data)