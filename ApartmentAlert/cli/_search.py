import ast
import click
import datetime
import schedule
import time
import sys
from ApartmentAlert.scrapers import check_for_wggesucht, check_for_immonet, check_for_immobilienscout


@click.command(startAgent)
@click.option('--immoscout_url', required=True, type=str)
@click.option('--immonet_url', required=True, type=str)
@click.option('--wggesucht_url', required=True, type=str)
@click.option('--from_mail', required=True, type=str)
@click.option('--to_mail', required=True, type=str)
@click.option('--pw_mail', required=True, type=str)
@click.option('--smtp_server', required=True, type=str)
@click.option('--log_path', required=True, type=str)
@click.option('--stop_time', required=False, type=str)
def startAgent(immoscout_url: str, immonet_url: str, wggesucht_url: str,
                 from_mail: str, to_mail: str, pw_mail: str, smtp_server: str,
                 log_path: str, stop_time: str = None):
    log_file = open('{}/{}.txt'.format(log_path, datetime.datetime.now().strftime('%d_%b_%y|%H:%M:%S')), 'w')
    sys.stdout = log_file
    
    to_mail = ast.literal_eval(to_mail)

    check_for_immobilienscout(immoscout_url, from_mail, to_mail, pw_mail, smtp_server)
    check_for_immonet(immonet_url, from_mail, to_mail, pw_mail, smtp_server)
    check_for_wggesucht(wggesucht_url, from_mail, to_mail, pw_mail, smtp_server)

    schedule.every(1).to(2).minutes.do(check_for_immobilienscout)
    schedule.every(1).to(2).minutes.do(check_for_immonet)
    schedule.every(1).to(2).minutes.do(check_for_wggesucht)

    while True:
        schedule.run_pending()
        time.sleep(1)
        if stop_time:
            if datetime.datetime.now().strftime('%H:%M:%S') >= stop_time:
                break

    sys.stdout.close()
