import datetime as dt
from scraper import *
from constants import *


def home():
    print(header)
    print('(1) Scraping\n(2) Keluar')

    choice = input('\nPilih (1/2): ')
    os.system('cls')
    if choice == '1':
        topic_choice_menu()
    elif choice == '2':
        print('Keluar dari program')
        time.sleep(0.5)
        os.system('cls')
        exit()
    else:
        invalid_selection()
        home()

def topic_choice_menu():
    print('+{} {} {}+'.format('-'*15, 'Topik Berita', '-'*15))
    print('\n(1) Cari topik berita\n(2) Topik berita campuran\n(K) Kembali')

    choice = input('\nPilih (1/2/K): ')
    os.system('cls')

    if choice == '1':
        topic_search_menu(True)
    elif choice == '2':
        topic_search_menu(False)
    elif choice == 'K' or choice == 'k':
        home()
    else:
        invalid_selection()
        topic_choice_menu()

def topic_search_menu(is_topic):
    if is_topic:
        print('+{} {} {}+'.format('-'*15, 'Pencarian Topik Berita', '-'*15))
        topic = input('\nCari topik berita: ')
        if topic == '':
            print('[Pencarian tidak boleh kosong!]')
            time.sleep(0.5)
            os.system('cls')
            topic_search_menu(is_topic)
    else:
        topic = '+'
    
    os.system('cls')
    news_dates_menu(topic)

def news_dates_menu(topic):
    print('+{} {} {}+'.format('-'*15, 'Rentang Waktu Berita', '-'*15)+'\n')
    date_start = in_date_start()
    date_end = in_date_end(date_start)

    os.system('cls')
    news_cat_menu(topic, date_start, date_end)

def news_cat_menu(topic, date_start, date_end):
    print('+{} {} {}+'.format('-'*15, 'Kategori Berita', '-'*15))
    print('\nPilih kategori berita:\n' + category_ls_str)
    print('\n(K)  Kembali\n(B)  Beranda')
    
    n_cat = 20
    choice = input('\nPilih (1/2/.../20/K/B): ')
    os.system('cls')

    if choice == 'K' or choice == 'k':
        topic_choice_menu()
    elif choice == 'B' or choice == 'b':
        home()
    elif choice.isnumeric():
        if int(choice) in range(1, n_cat):
            cat_choice = int(choice)
            ads_options_menu(topic, date_start, date_end, cat_choice)
        elif int(choice) == 20:
            cat_choice = int(choice)
            ads_options_menu(topic, date_start, date_end, cat_choice)
        else:
            invalid_selection()
            news_cat_menu(topic, date_start, date_end)
    else:
        invalid_selection()
        news_cat_menu(topic, date_start, date_end)

def ads_options_menu(topic, date_start, date_end, cat_choice):
    print('+{} {} {}+'.format('-'*15, 'Artikel Avertorial', '-'*15))
    print('\nSertakan artikel avertorial?')
    print('(Y) Ya\n(N) Tidak\n(K) Kembali\n(B) Beranda')

    choice = input('\nPilih (Y/N/K/B): ')
    os.system('cls')

    if choice == 'Y' or choice == 'y':
        is_avertorial = True
        content_options_menu(topic, date_start, date_end, cat_choice, is_avertorial)
    elif choice == 'N' or choice == 'n':
        is_avertorial = False
        content_options_menu(topic, date_start, date_end, cat_choice, is_avertorial)
    elif choice == 'K' or choice == 'k':
        news_cat_menu(topic, date_start, date_end)
    elif choice == 'B' or choice == 'b':
        home()
    else:
        invalid_selection()
        ads_options_menu(topic, date_start, date_end, cat_choice)

def content_options_menu(topic, date_start, date_end, cat_choice, is_avertorial):
    print('+{} {} {}+'.format('-'*15, 'Konten Artikel', '-'*15))
    print('\nEkstrak konten/isi artikel?')
    print('(Y) Ya\n(N) Tidak\n(K) Kembali\n(B) Beranda')

    choice = input('\nPilih (Y/N/K/B): ')
    os.system('cls')

    if choice == 'Y' or choice == 'y':
        is_content = True
        news_scrape_menu(topic, date_start, date_end, cat_choice, is_avertorial, is_content)
    elif choice == 'N' or choice == 'n':
        is_content = False
        news_scrape_menu(topic, date_start, date_end, cat_choice, is_avertorial, is_content)
    elif choice == 'K' or choice == 'k':
        ads_options_menu(topic, date_start, date_end, cat_choice)
    elif choice == 'B' or choice == 'b':
        home()

def news_scrape_menu(topic, date_start, date_end, cat_choice, is_avertorial, is_content):
    if cat_choice == 20:
        df_articles = pd.DataFrame(columns=['title', 'category', 'publish_date', 'article_url', 'content'])
        for cat in category_id:
            print(f'Kategori: {category_id_name[category_id[cat]]}')
            df_articles_cat, articles_num = detikcom_articles(topic,
                                                category_id[cat],
                                                date_start,
                                                date_end,
                                                is_avertorial,
                                                is_content
                                                )
            df_articles = pd.concat([df_articles, df_articles_cat], ignore_index=True)
            print()

    else:
        df_articles, articles_num = detikcom_articles(topic,
                                        category_id[cat_choice],
                                        date_start,
                                        date_end,
                                        is_avertorial,
                                        is_content
                                        )
    os.system('cls')
    if df_articles.empty:
        articles_not_found(topic)

    else:
        save_to_file(topic, date_start, date_end, cat_choice, is_avertorial, is_content, df_articles, articles_num)

def save_to_file(topic, date_start, date_end, cat_choice, is_avertorial, is_content, df_articles, articles_num):
    if cat_choice == 20:
        news_cat = 'all'
        articles_num = len(df_articles)
    else:
        news_cat = category_id_name[category_id[cat_choice]]
    
    if topic == '+':
        topic = 'none'
    else:
        topic = topic.lower()
    
    is_content = str(is_content).lower()
    is_avertorial = str(is_avertorial).lower()

    date_start = date_start.replace('/', '')
    date_end = date_end.replace('/', '')
    current_time = dt.datetime.now().strftime('%d%m%Y-%H%M%S')

    current_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(current_directory, 'data')
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    print('+{} {} {}+'.format('-'*15, 'Simpan Hasil Scraping', '-'*15))
    print('\nSimpan hasil scraping ke file?\n(1) CSV\n(2) Excel\n(3) CSV & Excel')

    choice = input('\nPilih (1/2/3): ')
    os.system('cls')

    if choice == '1':
        df_articles.to_csv(f'{data_directory}/{topic}_{articles_num}_{date_start}_{date_end}_{news_cat}_{is_avertorial}_{is_content}_ds-{current_time}.csv', index=False)
        print('[Hasil scraping telah disimpan menjadi file CSV.]')
        time.sleep(2)
        os.system('cls')
        home()
    elif choice == '2':
        df_articles.to_excel(f'{data_directory}/{topic}_{articles_num}_{date_start}_{date_end}_{news_cat}_{is_avertorial}_{is_content}_ds-{current_time}.xlsx', index=False)
        print('[Hasil scraping telah disimpan menjadi file Excel.]')
        time.sleep(2)
        os.system('cls')
        home()
    elif choice == '3':
        df_articles.to_csv(f'{data_directory}/{topic}_{articles_num}_{date_start}_{date_end}_{news_cat}_{is_avertorial}_{is_content}_ds-{current_time}.csv', index=False)
        df_articles.to_excel(f'{data_directory}/{topic}_{articles_num}_{date_start}_{date_end}_{news_cat}_{is_avertorial}_{is_content}_ds-{current_time}.xlsx', index=False)
        print('[Hasil scraping telah disimpan menjadi file CSV dan Excel.]')
        time.sleep(2)
        os.system('cls')
        home()
    else:
        invalid_selection()
        save_to_file(topic, date_start, date_end, cat_choice, is_avertorial, is_content, df_articles, articles_num)

def articles_not_found(topic):
    print(f'Tidak ada artikel yang ditemukan mengenai "{topic}".')
    print('(1) Cari topik lain\n(B) Beranda')

    choice = input('\nPilih (1/B): ')
    os.system('cls')

    if choice == '1':
        topic_search_menu(True)
    elif choice == 'B' or choice == 'b':
        home()
    else:
        articles_not_found(topic)

def invalid_selection():
    os.system('cls')
    print('[Pilihan tidak valid!]')
    time.sleep(0.5)
    os.system('cls')

if __name__ == '__main__':
    home()