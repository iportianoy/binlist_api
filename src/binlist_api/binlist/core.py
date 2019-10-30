import logging
import urllib.request
import urllib.error

from aiohttp import ClientSession
from proxyscrape import create_collector

from .config import CONFIG


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

BINLIST_API_URL = CONFIG.get('BINLIST_API_URL', None)
CHECK_PROXY = bool(CONFIG.get('CHECK_PROXY', None))
collector = create_collector('my-collector', 'http')
session = ClientSession()


async def get_card(card_number):
    """
    Make request to binlist API and get info about card
    :param card_number: str, first 8 numbers of card
    :param proxy_list: list, list of proxy servers
    :return: dict, info about card or error
    """
    proxy = collector.get_proxy()
    proxy = proxy.host + ':' + proxy.port

    if CHECK_PROXY:
        work_proxy = working_proxy(proxy)
        while not work_proxy:
            proxy = collector.get_proxy()
            proxy = proxy.host + ':' + proxy.port
            work_proxy = working_proxy(proxy)

    proxy = 'http://' + proxy

    try:
        async with session.get(BINLIST_API_URL + card_number, proxy=proxy) as resp:
            if resp.status == 200:
                logging.info(card_number)
                logging.info(resp.status)
                logging.info('OK!')
                logging.info('---------------')

                card_info = await resp.json()

                return {card_number: card_info}

            else:
                logging.info(card_number)
                logging.info(resp.status)
                logging.info(resp)
                logging.info('---------------')

                return {card_number: 'Card doesn\'t exist'}
    except Exception as e:
        logging.info(card_number)
        logging.info(proxy)
        logging.error(f'Getting card {card_number} Error: ' + str(e))
        logging.info('---------------')

        return {card_number: {'Error': str(e)}}


def working_proxy(proxy):
    """
    Check if proxy is working
    :param proxy: proxy adress
    :return: bool
    """
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req = urllib.request.Request('http://www.google.com')
        sock = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        logging.error(f'Cheking proxy {proxy} Error: ' + str(e))
        return False
    except Exception as detail:
        logging.error(f'Cheking proxy {proxy} Error: ' + str(detail))
        return False

    return True

