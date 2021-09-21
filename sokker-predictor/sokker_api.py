import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_height_and_form(pid, requests_session):
    def download_file(url, save_path, requests_session):

        filename = save_path

        with open(filename, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)

    download_url = 'https://sokker.org/xml/player-{}.xml'.format(pid)
    response = requests_session.get(download_url, timeout=(15, 15))
    download_file(response.url, '../data_outputs/transfers.xml', requests_session)  # run function to download file

    with open('../data_outputs/transfers.xml', encoding="utf8") as rd:
        read_data = rd.read()

    soup = BeautifulSoup(read_data, 'html.parser')

    try:
        height = soup.find('height').text
        form = soup.find('skillform').text
    except:
        height = 0
        form = 0

    return height, form


def get_height_and_form_lists(requests_session, filepath):
    pidlist = pd.read_csv(filepath, low_memory=False)
    print('csv read complete')
    pidlist = pd.DataFrame(pidlist)
    height_list = []
    form_list = []
    pid_list = []
    for iteration, pid in enumerate(pidlist['PID']):
        height, form = get_height_and_form(pid, requests_session)
        height_list.append(height)
        form_list.append(form)
        pid_list.append(pid)
        print('Fetching player height and form ', iteration, '/', len(pidlist['PID']))
    return pid_list, height_list, form_list


def api_players(filepath, login, password):
    username = login
    password = password

    data_credentials = {'ilogin': username, 'ipassword': password}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    login_url = "https://sokker.org/start.php?session=xml"
    requests_session = requests.Session()  # create a requests Session
    response = requests_session.post(login_url, headers=headers,
                                     data=data_credentials)  # log in to the requests Session so that you can reuse it

    pid_list, height_list, form_list = get_height_and_form_lists(requests_session, filepath)
    return height_list, form_list
