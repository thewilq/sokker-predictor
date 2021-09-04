import pickle
import pandas as pd
import numpy as np
from datetime import datetime


def make_predictions(prediction_csv_path, full_scrap_path):
    model = pickle.load(open('Models/mlp_hla13k_adap_lri01_iter200_lean.sav', 'rb'))  # wczytujemy model
    players_table = pd.read_csv(prediction_csv_path)  # wczytujemy dane potrzebne do modelu
    full_data = pd.read_csv(full_scrap_path)  # pelny zestaw danych potrzebny do zbudowania pliku wyjsciowego
    players_table['wiek'] = players_table['wiek'] + players_table[
        'tydzien'] / 16  # poprawa wieku zeby brac pod uwage tydzien sezonu
    players_table = players_table.drop(['tydzien'], axis=1)  # usuwamy niepotrzebna kolumne tydzien

    actual_prediction = model.predict(players_table)  # odpalamy model na naszych danych i zapisujemy
    # players_table['predicted_price'] = actual_prediction  # aktualizujemy dataframe o kolumne predykcji

    # szybkosc
    players_table_backup = players_table.copy()
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['szybkość'] = np.where((players_table['szybkość'] <= 17), players_table['szybkość'] + 1,
                                         players_table['szybkość'])
    szyb1_tyg5 = model.predict(players_table)  # predict
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['szybkość'] = np.where((players_table['szybkość'] <= 17), players_table['szybkość'] + 1,
                                         players_table['szybkość'])
    szyb2_tyg10 = model.predict(players_table)  # predict
    players_table = players_table_backup.copy()

    # technika
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['technika'] = np.where((players_table['technika'] <= 17), players_table['technika'] + 1,
                                         players_table['technika'])
    tech1_tyg5 = model.predict(players_table)  # predict
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['technika'] = np.where((players_table['technika'] <= 17), players_table['technika'] + 1,
                                         players_table['technika'])
    tech2_tyg10 = model.predict(players_table)  # predict
    players_table = players_table_backup.copy()

    # rozgrywający
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['rozgrywający'] = np.where((players_table['rozgrywający'] <= 17), players_table['rozgrywający'] + 1,
                                             players_table['rozgrywający'])
    rozg1_tyg5 = model.predict(players_table)  # predict
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['rozgrywający'] = np.where((players_table['rozgrywający'] <= 17), players_table['rozgrywający'] + 1,
                                             players_table['rozgrywający'])
    rozg2_tyg10 = model.predict(players_table)  # predict
    players_table = players_table_backup.copy()

    # podania
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['podania'] = np.where((players_table['podania'] <= 17), players_table['podania'] + 1,
                                        players_table['podania'])
    pod1_tyg5 = model.predict(players_table)  # predict
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['podania'] = np.where((players_table['podania'] <= 17), players_table['podania'] + 1,
                                        players_table['podania'])
    pod2_tyg10 = model.predict(players_table)  # predict
    players_table = players_table_backup.copy()

    # obronca
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['obrońca'] = np.where((players_table['obrońca'] <= 17), players_table['obrońca'] + 1,
                                        players_table['obrońca'])
    obr1_tyg5 = model.predict(players_table)  # predict
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['obrońca'] = np.where((players_table['obrońca'] <= 17), players_table['obrońca'] + 1,
                                        players_table['obrońca'])
    obr2_tyg10 = model.predict(players_table)  # predict
    players_table = players_table_backup.copy()

    # strzal
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['strzelec'] = np.where((players_table['strzelec'] <= 17), players_table['strzelec'] + 1,
                                         players_table['strzelec'])
    strz1_tyg5 = model.predict(players_table)  # predict
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    players_table['strzelec'] = np.where((players_table['strzelec'] <= 17), players_table['strzelec'] + 1,
                                         players_table['strzelec'])
    strz2_tyg10 = model.predict(players_table)  # predict
    players_table = players_table_backup.copy()

    # 5 tygodni bez skoku (szybkki zysk bez treningu)
    players_table['wiek'] = players_table['wiek'] + 5 / 16
    nic_5tyg = model.predict(players_table)  # predict
    players_table = players_table_backup.copy()

    full_data = full_data.drop(['transfer_id', 'wartość', 'dzien_tygodnia'], axis=1)
    full_data['aktualna_wycena'] = actual_prediction
    full_data['nic_5tyg'] = nic_5tyg
    full_data['szyb1_tyg5'] = szyb1_tyg5
    full_data['szyb2_tyg10'] = szyb2_tyg10
    full_data['obr1_tyg5'] = obr1_tyg5
    full_data['obr2_tyg10'] = obr2_tyg10
    full_data['tech1_tyg5'] = tech1_tyg5
    full_data['tech2_tyg10'] = tech2_tyg10
    full_data['rozg1_tyg5'] = rozg1_tyg5
    full_data['rozg2_tyg10'] = rozg2_tyg10
    full_data['pod1_tyg5'] = pod1_tyg5
    full_data['pod2_tyg10'] = pod2_tyg10
    full_data['strz1_tyg5'] = strz1_tyg5
    full_data['strz2_tyg10'] = strz2_tyg10
    # fix minus values, set to 0
    full_data['aktualna_wycena'] = np.where((full_data['aktualna_wycena'] < 0), 0,
                                            full_data['aktualna_wycena'])
    full_data['nic_5tyg'] = np.where((full_data['nic_5tyg'] < 0), 0,
                                     full_data['nic_5tyg'])
    full_data['szyb1_tyg5'] = np.where((full_data['szyb1_tyg5'] < 0), 0,
                                       full_data['szyb1_tyg5'])
    full_data['szyb2_tyg10'] = np.where((full_data['szyb2_tyg10'] < 0), 0,
                                        full_data['szyb2_tyg10'])
    full_data['obr1_tyg5'] = np.where((full_data['obr1_tyg5'] < 0), 0,
                                      full_data['obr1_tyg5'])
    full_data['obr2_tyg10'] = np.where((full_data['obr2_tyg10'] < 0), 0,
                                       full_data['obr2_tyg10'])
    full_data['tech1_tyg5'] = np.where((full_data['tech1_tyg5'] < 0), 0,
                                       full_data['tech1_tyg5'])
    full_data['tech2_tyg10'] = np.where((full_data['tech2_tyg10'] < 0), 0,
                                        full_data['tech2_tyg10'])
    full_data['rozg1_tyg5'] = np.where((full_data['rozg1_tyg5'] < 0), 0,
                                       full_data['rozg1_tyg5'])
    full_data['rozg2_tyg10'] = np.where((full_data['rozg2_tyg10'] < 0), 0,
                                        full_data['rozg2_tyg10'])
    full_data['pod1_tyg5'] = np.where((full_data['pod1_tyg5'] < 0), 0,
                                      full_data['pod1_tyg5'])
    full_data['pod2_tyg10'] = np.where((full_data['pod2_tyg10'] < 0), 0,
                                       full_data['pod2_tyg10'])
    full_data['strz1_tyg5'] = np.where((full_data['strz1_tyg5'] < 0), 0,
                                       full_data['strz1_tyg5'])
    full_data['strz2_tyg10'] = np.where((full_data['strz2_tyg10'] < 0), 0,
                                        full_data['strz2_tyg10'])

    datemask = datetime.now().strftime('%Y%m%d%H%M')
    prediction_output_filepath = '../Predictions/Prediction_Output_{}.xlsx'.format(datemask)
    full_data.to_excel(prediction_output_filepath)
    print('Wygenerowano plik: {}'.format(prediction_output_filepath))
