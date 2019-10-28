import json
from random import choice
from aiohttp import ClientSession
from . import api_url

session = ClientSession()


async def get_card(card_number, proxy_list):
    proxy = choice(proxy_list)
    print(card_number)
    try:
        async with session.get(api_url + card_number, proxy=proxy) as resp:

            print(resp.status)
            if resp.status == 200:
                print('OK!')
                print('---------------')
                return await resp.json()

            else:
                print(resp)
                print('---------------')
                return {'error': 'card not found'}
    except Exception as e:
        print(proxy)
        print('Error')
        print(e)
        print('---------------')
        return {'error': str(e)}
