import asyncio
from proxybroker import Broker


async def get_proxy(proxies):
    while True:
        proxy = await proxies.get()

        if proxy is None:
                break
        prox_list.append(str(proxy.host) + ':' + str(proxy.port))

proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.find(types=['HTTP', 'HTTPS'], limit=20), get_proxy(proxies))

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)

print(len(prox_list))

print(prox_list)

# import gray_harvest
#
# ''' spawn a harvester '''
# harvester = grey_harvest.GreyHarvester()
#
# ''' harvest some proxies from teh interwebz '''
# count = 0
# for proxy in harvester.run():
#     print(proxy)
#     count += 1
#     if count >= 20:
#         break


# import time
# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
#
# if __name__ == '__main__':
#
#     start = time.time()
#     req_proxy = RequestProxy()
#     req_proxy.logger.disabled = False
#     print("Initialization took: {0} sec".format((time.time() - start)))
#     print("Size: {0}".format(len(req_proxy.get_proxy_list())))
#     print("ALL = {0} ".format(list(map(lambda x: x.get_address(), req_proxy.get_proxy_list()))))
