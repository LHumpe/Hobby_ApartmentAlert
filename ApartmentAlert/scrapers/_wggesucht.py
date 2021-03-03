from bs4 import BeautifulSoup
import requests as rqs
from ApartmentAlert.util_funcs import sendemail, with_logging, catch_exceptions
import pickle


@catch_exceptions
@with_logging
def check_for_wggesucht(url: str, from_mail: str, to_mail: str, pw_mail: str, smtp_server: str):
    # get URl
    wgges = url
    wggespg = rqs.get(wgges)

    # Get Html
    wggessoup = BeautifulSoup(wggespg.text, 'lxml')

    # Get number of Results
    wgges_no_string = wggessoup.find_all('h1', class_='headline headline-default', limit=1)
    wgges_no_new = str(wgges_no_string[0]).split()[6]

    try:
        file = open('../data/WgGesuchtNoRes.txt', 'rb')
        wgges_no_old = pickle.load(file)
        file.close()
        print('Anzahl der Ergebnisse Initialisiert Alt: {} Neu: {}'.format(wgges_no_old, wgges_no_new))
    except:
        print('Anzahl der Ergebnisse neu Initialisiert {}'.format(wgges_no_new))
        file = open('../data/WgGesuchtNoRes.txt', 'wb')
        pickle.dump(wgges_no_new, file)
        file.close()
        wgges_no_old = None

    # Get Result links
    wgges_r_list = wggessoup.find_all('div',
                                      class_='panel panel-default panel-hidden display-none list-details-ad-border noprint')

    list = []
    for i in wgges_r_list:
        list.append(i.find('a'))

    links = []
    for a in list:
        links.append(a['href'])

    try:
        file = open('../data/WgGesuchtID.txt', 'rb')
        wggesid_old = None
        wggesid_old = pickle.load(file)
        file.close()
        print('Links Initialisiert Alt: {} Neu: {}'.format(len(wggesid_old), len(links)))
    except:
        print('Links neu Initialisiert {}'.format(len(links)))
        file = open('../data/WgGesuchtID.txt', 'wb')
        pickle.dump(links, file)
        file.close()
        wggesid_old = None

    # Check
    if wgges_no_old is not None:
        if wgges_no_new <= wgges_no_old and links[0] in wggesid_old:
            message = 'Es gibt keine neuen Wohnungen auf WgGesucht.\n\n'
        else:
            message = 'Es gibt neue Wohnungen auf WgGesucht!\n\n'
            sendemail(from_addr=from_mail,
                      to_addr=to_mail,
                      subject='Neue Wohnungen auf WgGesucht',
                      message='Suche {} \n\n Wohnung: https://www.wg-gesucht.de/{}'.format(url, links[0]),
                      login=from_mail,
                      password=pw_mail,
                      smtpserver=smtp_server)

    else:
        message = 'Du hast auf diesem Portal noch nicht gesucht. \n\n'
        sendemail(from_addr=from_mail,
                  to_addr=to_mail,
                  subject='Eingerichtete Suche WgGesucht',
                  message='Die Suche für das Portal WgGesucht wurde eingerichtet. \n Link zur Suche: {}'.format(url),
                  login=from_mail,
                  password=pw_mail,
                  smtpserver=smtp_server)

    file = open('../data/WgGesuchtNoRes.txt', 'wb')
    pickle.dump(wgges_no_new, file)
    file.close()

    file = open('../data/WgGesuchtID.txt', 'wb')
    pickle.dump(links, file)
    file.close()

    return print(message)
