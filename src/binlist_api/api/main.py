import asyncio
from aiohttp import web
from proxybroker import Broker
from binlist_api.binlist.core import get_card

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.Response(text='API for working with https://binlist.net/')


@routes.get('/cards/{card_numbers}')
async def get_cards(request):
    card_numbers = request.match_info['card_numbers']
    cards = card_numbers.split('-')

    proxy_list = []

    async def get_proxy(proxies):
        while True:
            proxy = await proxies.get()

            if proxy is None:
                break
            proxy_list.append('http://' + str(proxy.host) + ':' + str(proxy.port))

    proxies = asyncio.Queue()
    broker = Broker(proxies)
    await asyncio.gather(
        broker.find(types=['HTTP'], limit=20), get_proxy(proxies))

    tasks = [get_card(card, proxy_list=proxy_list) for card in cards]

    cards_with_info = await asyncio.gather(*tasks)

    return web.json_response({'result': cards_with_info})


async def get_proxy(proxies):
    proxy = None
    while True:
        prev_proxy, proxy = proxy, await proxies.get()
        if proxy is None:
            break

    return str(prev_proxy.host) + ':' + str(prev_proxy.port)

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8080)
