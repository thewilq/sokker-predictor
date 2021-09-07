import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from time import sleep
import sokker_api
from math import floor
import predict
from pathlib import Path
from functions import getpass

print('Zaloguj się do sokkera')
login = input('Wpisz login: ')
password = getpass('Wpisz hasło: ')

print('Logowanie...')

Path("../data_outputs").mkdir(parents=True, exist_ok=True)
Path("../Predictions").mkdir(parents=True, exist_ok=True)

options = Options()
options.headless = True
options.add_argument("--log-level=3")

driver = webdriver.Chrome(executable_path='./Chromedriver/chromedriver.exe', options=options)
driver.get('https://sokker.org/transferSearch/trainer/0/pg/1/transfer_list/1/sort/end')
driver.find_element_by_id('ilogin').send_keys(login)
driver.find_element_by_id('ipassword').send_keys(password)
driver.find_element_by_xpath('//*[@id="logon-logon-cart"]/div[2]/form/div[3]/div/button').click()
print('Zalogowano do sokker.org')
sleep(3)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

transfer_id = []
player_name = []
player_pid = []
player_age = []
player_value = []
kondycja_num = []
szybkosc_num = []
technika_num = []
podania_num = []
bramkarz_num = []
obronca_num = []
rozgrywajacy_num = []
strzelec_num = []
end_of_auction_time_list = []
end_of_auction_date_list = []
aktualna_cena = []
week_num = []

global_counter = 0

while soup.findAll(attrs='well'):
    # print('foundsomething')
    page_number = global_counter + 1
    sokker_tl_webpath = 'https://sokker.org/transferSearch/trainer/0/pg/{}/transfer_list/1/sort/end'.format(page_number)
    print('currently scraping TL page number - {}'.format(page_number))
    driver.get(sokker_tl_webpath)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    # age, name, pid
    # for element in soup.findAll(attrs='h5 title-block-2 text-primary'):
    for element in soup.findAll(attrs='h5 title-block-2 text-primary c-player__cell'):
        pid = element.find('a')['href']
        name = element.find('a').contents[0]
        age = element.text
        if age not in player_age:
            player_age.append(int(age[-4:-1]))
        if name not in player_name:
            player_name.append(name)
        if pid not in player_pid:
            player_pid.append(pid[-8:])
            transfer_id.append(pid[-8:] + datetime.now().strftime('%Y%m%d'))
    for element in soup.findAll(attrs='col-md-6 col-sm-5 col-xs-12 small'):
        value = element.find().text
        player_value.append(int(value.replace(' ', '')[:-2]))
    for element in soup.findAll(attrs='well'):
        table_body = element.find('tbody')
        rows = table_body.find_all('tr')
        counter: int = 0
        for row in rows:
            values = row.find_all(attrs='skillNameNumber')
            value1 = values[0].text
            value2 = values[1].text
            if counter == 0:
                kondycja_num.append(int(value1[1:-1]))
                bramkarz_num.append(int(value2[1:-1]))
            if counter == 1:
                szybkosc_num.append(int(value1[1:-1]))
                obronca_num.append(int(value2[1:-1]))
            if counter == 2:
                technika_num.append(int(value1[1:-1]))
                rozgrywajacy_num.append(int(value2[1:-1]))
            if counter == 3:
                podania_num.append(int(value1[1:-1]))
                strzelec_num.append(int(value2[1:-1]))
            counter = counter + 1
    for element in soup.findAll(attrs='col-md-6 col-sm-5 col-xs-12 small'):
        for linebreak in soup.find_all('br'):
            linebreak.extract()
        end_of_auction_datetime = datetime.strptime(element.contents[-3:-2][0].text, '%Y-%m-%d %H:%M')
        end_of_auction_date = end_of_auction_datetime.date()
        end_of_auction_time = end_of_auction_datetime.time()
        end_of_auction_date_list.append(end_of_auction_date)
        end_of_auction_time_list.append(end_of_auction_time)
        aktualna_cena.append(element.contents[-7:-6][0].text)
        week_of_year = end_of_auction_date.isocalendar()[1]
        sokker_week = week_of_year - ((floor(week_of_year / 16)) * 16)
        week_num.append(sokker_week)

    global_counter = global_counter + 1

zipped_lists = zip(kondycja_num, bramkarz_num, szybkosc_num, obronca_num, technika_num, rozgrywajacy_num,
                   podania_num, strzelec_num)
sumskil = [sum(item) for item in zipped_lists]

driver.quit()

df = pd.DataFrame({'transfer_id': transfer_id
                      , 'PID': player_pid
                      , 'zawodnik': player_name
                      , 'wiek': player_age
                      , 'wartość': player_value
                      , 'kondycja': kondycja_num
                      , 'bramkarz': bramkarz_num
                      , 'szybkość': szybkosc_num
                      , 'obrońca': obronca_num
                      , 'technika': technika_num
                      , 'rozgrywający': rozgrywajacy_num
                      , 'podania': podania_num
                      , 'strzelec': strzelec_num
                      , 'sumskill': sumskil
                      , 'data_koniec_aukcji': end_of_auction_date_list
                      , 'czas_koniec_aukcji': end_of_auction_time_list
                      , 'dzien_tygodnia': datetime.isoweekday(end_of_auction_date)
                      , 'aktualna_cena': aktualna_cena})

datemask = datetime.now().strftime('%Y%m%d%H%M')
full_filepath = '../data_outputs/transfer_list_{}'.format(datemask)
df.to_csv(full_filepath, index=False, encoding='utf-8')

lista_wzrost, lista_forma = sokker_api.api_players(full_filepath, login, password)

df_prediction_input = pd.DataFrame({'wiek': player_age
                                       , 'bramkarz': bramkarz_num
                                       , 'szybkość': szybkosc_num
                                       , 'obrońca': obronca_num
                                       , 'technika': technika_num
                                       , 'rozgrywający': rozgrywajacy_num
                                       , 'podania': podania_num
                                       , 'strzelec': strzelec_num
                                       , 'wzrost': lista_wzrost
                                       , 'forma': lista_forma
                                       , 'tydzien': sokker_week})

prediction_input_filepath = '../data_outputs/transfer_list_prediction_input_{}'.format(datemask)
df_prediction_input.to_csv(prediction_input_filepath, index=False, encoding='utf-8')

predict.make_predictions(prediction_input_filepath, full_filepath)
