from bs4 import BeautifulSoup
import requests as rqs
from ApartmentAlert.util_funcs import sendemail, with_logging, catch_exceptions
import pickle


@catch_exceptions
@with_logging
def check_for_immonet(url: str, from_mail: str, to_mail: str, pw_mail: str, smtp_server: str):
    immonet = url
    netpg = rqs.get(immonet)

    netsoup = BeautifulSoup(netpg.text, 'lxml')

    net_no_list = netsoup.find_all('span', id='totalCount')
    net_no_new = net_no_list[0].get_text().split()[0]

    try:
        file = open('../data/ImmonetNo.txt', 'rb')
        net_no_old = None
        net_no_old = pickle.load(file)
        file.close()
        print('Anzahl der Ergebnisse Initialisiert Alt: {} Neu: {}'.format(net_no_old, net_no_new))
    except:
        print('Anzahl der Ergebnisse neu Initialisiert {}'.format(net_no_new))
        file = open('../data/ImmonetNo.txt', 'wb')
        pickle.dump(net_no_new, file)
        file.close()
        net_no_old = None

    net_r_list = netsoup.find_all('a', class_='block ellipsis text-225 text-default')
    net_list = []
    for i in net_r_list:
        net_list.append(i.get('id').split('_')[1])

    try:
        file = open('../data/ImmonetID.txt', 'rb')
        netid_old = None
        netid_old = pickle.load(file)
        file.close()
        print('Links Initialisiert Alt: {} Neu: {}'.format(len(netid_old), len(net_list)))
    except:
        print('Links neu Initialisiert {}'.format(len(net_list)))
        file = open('../data/ImmonetID.txt', 'wb')
        pickle.dump(net_list, file)
        file.close()
        netid_old = None

        # Check
    if netid_old is not None:
        if net_no_new <= net_no_old and net_list[0] in netid_old:
            message = 'Es gibt keine neuen Wohnungen auf Immonet.\n\n'
        else:
            message = 'Es gibt neue Wohnungen auf Immonet!\n\n'
            sendemail(from_addr=from_mail,
                      to_addr=to_mail,
                      subject='Neue Wohnungen auf Immonet',
                      message='Suche {} \n\n Wohnung: https://www.immonet.de/angebot/{}'.format(url, net_list[0]),
                      login=from_mail,
                      password=pw_mail,
                      smtpserver=smtp_server)
    else:
        message = 'Du hast auf diesem Portal noch nicht gesucht.\n\n'
        sendemail(from_addr=from_mail,
                  to_addr=to_mail,
                  subject='Eingerichtete Suche Immonet',
                  message='Die Suche für das Portal Immonet wurde eingerichtet.\n Link: {}'.format(url),
                  login=from_mail,
                  password=pw_mail,
                  smtpserver=smtp_server)

    file = open('../data/ImmonetNo.txt', 'wb')
    pickle.dump(net_no_new, file)
    file.close()

    file = open('../data/ImmonetID.txt', 'wb')
    pickle.dump(net_list, file)
    file.close()

    return print(message)
