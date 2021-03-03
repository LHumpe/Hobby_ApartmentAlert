from bs4 import BeautifulSoup
import requests as rqs
from ApartmentAlert.util_funcs import sendemail, with_logging, catch_exceptions
import pickle


# Immobilienscout
@catch_exceptions
@with_logging
def check_for_immobilienscout(url: str, from_mail: str, to_mail: str, pw_mail: str, smtp_server: str):
    # get Url
    immoscout = url
    scoutpg = rqs.get(immoscout)

    # Get Html
    scoutsoup = BeautifulSoup(scoutpg.text, 'lxml')

    # Get number of results
    scout_no_list = scoutsoup.find_all('span', class_='font-normal')
    scout_no_string = str(scout_no_list[0]).split('>')
    scout_no_string = str(scout_no_string[1]).split('<')
    scout_no_new = scout_no_string[0]

    try:
        file = open('../data/ImmobilienscoutNo.txt', 'rb')
        scout_no_old = None
        scout_no_old = pickle.load(file)
        file.close()
        print('Anzahl der Ergebnisse Initialisiert Alt: {} Neu: {}'.format(scout_no_old, scout_no_new))
    except:
        print('Anzahl der Ergebnisse neu Initialisiert {}'.format(scout_no_new))
        file = open('../data/ImmobilienscoutNo.txt', 'wb')
        pickle.dump(scout_no_new, file)
        file.close()
        scout_no_old = None

    # Get Result links
    scout_r_list = scoutsoup.find_all('div', class_='result-list-entry__data')
    s_list = []
    for i in scout_r_list:
        s_list.append(i.find('button'))

    scout_links = []
    for a in s_list:
        scout_links.append(a['data-id'])

    try:
        file = open('../data/ImmobilienscoutID.txt', 'rb')
        scoutid_old = None
        scoutid_old = pickle.load(file)
        file.close()
        print('Links Initialisiert Alt: {} Neu: {}'.format(len(scoutid_old), len(scout_links)))
    except:
        print('Links neu Initialisiert {}'.format(len(scout_links)))
        file = open('../data/ImmobilienscoutID.txt', 'wb')
        pickle.dump(scout_links, file)
        file.close()
        scoutid_old = None

        # Check
    if scout_no_old is not None:
        if scout_no_new <= scout_no_old and scout_links[0] in scoutid_old:
            message = 'Es gibt keine neuen Wohnungen auf Immobilienscout24. \n\n'
        else:
            message = 'Es gibt neue Wohnungen auf Immobilienscout24!\n\n'
            sendemail(from_addr=from_mail,
                      to_addr=to_mail,
                      subject='Neue Wohnungen auf Immobilienscout24',
                      message='Suche {} \n\n Wohnung: https://www.immobilienscout24.de/expose/{}'.format(url, scout_links[0]),
                      login=from_mail,
                      password=pw_mail,
                      smtpserver=smtp_server)
    else:
        message = 'Du hast auf diesem Portal noch nicht gesucht. \n\n'
        sendemail(from_addr=from_mail,
                  to_addr=to_mail,
                  subject='Eingerichtete Suche Immobilienscout24',
                  message='Die Suche für das Portal Immobilienscout24 wurde eingerichtet.\n Link: {}'.format(url),
                  login=from_mail,
                  password=pw_mail,
                  smtpserver=smtp_server)

    file = open('../data/ImmobilienscoutNo.txt', 'wb')
    pickle.dump(scout_no_new, file)
    file.close()

    file = open('../data/ImmobilienscoutID.txt', 'wb')
    pickle.dump(scout_links, file)
    file.close()

    return print(message)
