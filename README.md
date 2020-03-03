# API QuickStarter

#### Simplified HTTP REST Framework based on AIOHTTP

#### Optimized for running serverless

### Example REST

```
from core.aio_cinch import AioCinch
from core.route import Route

async def handler(request):
    return {"message": "Hello"}, 422

if __name__ == "__main__":
    config = {
        "debug": True,
        "port": 8080,
        "encoder": None,
        "plugins": {},
        "routes": {
            "/": {
               "handlers": [Route(method='GET', handler=get_handler, req_schema={'name': {'type': 'string', 'required': True}}), Route(method='POST', handler=post_handler)]
            }
        }
    }
    AioCinch(config).run(__file__)

```

### Example WS

```
from core.aio_cinch import AioCinch

async def handler(ws, msg, msg_type):
    if msg.type == msg_type.TEXT:
        if msg.data == 'close':
            await ws.close()
        else:
            await ws.send_str(msg.data + '/answer')
    elif msg.type == msg_type.ERROR:
        print('ws connection closed with exception %s' %
              ws.exception())
    return True

if __name__ == "__main__":
    config = {
        "debug": True,
        "port": 8080,
        "encoder": None,
        "plugins": {},
        "ws": {
            "/ws": handler
        }
    }
    AioCinch(config).run(__file__)

```

| Config                | Type                              | Comment                                                                           |
| --------------------- | --------------------------------- | --------------------------------------------------------------------------------- |
| reload (optional)     | bool(True/False) default: False   | To enable the auto reload on file change                                          |
| port (optional)       | int default: 8080                 | Port number                                                                       |
| encoder(optional)     | class default: None               | custom encoder cls used to encode the json response                               |
| plugins(optional)     | dict default {}                   | The plugins need to be added like db connection etc this is accessible in request |
| routes (optional)     | Instance of Route class           | The routes                                                                        |
| ws (optional)         | dict default {}                   | The ws routes                                                                     |
| cors(optional)        | bool(True/False) default False    | To enable cors                                                                    |
| logger(optional)      | debug(default), info, warn, error | To enable framework log                                                           |
| prefix(optional)      | default: (empty)                  | Route prefix                                                                      |
| version(optional)     | default: (empty)                  | API version                                                                       |
| pre_request(optional) | default: (empty)                  | Method to execute before request                                                  |
