import asyncio
from aiohttp import web
from proxybroker import Broker

from binlist.core import get_card
from binlist.config import CONFIG

routes = web.RouteTableDef()
X_API_KEY = CONFIG.get('X_API_KEY', None)


@routes.get('/')
async def hello(request):
    """
    Info about app
    :param request: gotten request
    :return: web.Response, info about app
    """
    return web.Response(text='API for working with https://binlist.net/')


@routes.get('/cards/{card_numbers}')
async def get_cards(request):
    """
    Get info about cards
    :param request: gotten request
    :return: web.Response, info about cards or error
    """
    card_numbers = request.match_info['card_numbers']
    cards = card_numbers.split('-')

    x_api_key = request.headers.get("x-api-key", None)
    if not x_api_key or x_api_key != X_API_KEY:
        return web.json_response({'status_code': 403,
                                  'details': 'Forbidden'})

    proxy_list = []

    async def get_proxy(proxies):
        while True:
            proxy = await proxies.get()

            if proxy is None:
                break
            proxy_list.append(str(proxy.host) + ':' + str(proxy.port))

    proxies = asyncio.Queue()
    broker = Broker(proxies)
    await asyncio.gather(
        broker.find(types=['HTTP'], limit=20), get_proxy(proxies))

    tasks = [get_card(card, proxy_list) for card in cards]

    cards_with_info = await asyncio.gather(*tasks)

    return web.json_response({'status_code': 200,
                              'details': cards_with_info})


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8080)
