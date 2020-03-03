import inspect
import json
from aiohttp import web, WSMsgType
from .validation import validate


class Response:
    async def validate_request(self, request, schema):
        if request.method == 'GET':
            return validate(dict(request.query), schema)
        if request.content_type == 'application/json':
            data = await request.json()
            return validate(data, schema)
        return True, None

    def handle_ws(self, handler):
        async def ws_handler(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            async for msg in ws:
                await handler(ws, msg, WSMsgType)
            return ws

        return ws_handler

    def handler(self, route_handler, encoder, schema, pre_request):
        async def parser(request):
            if pre_request and callable(pre_request):
                if inspect.iscoroutinefunction(pre_request):
                    res = await pre_request(request, web)
                else:
                    res = pre_request(request, web)
                if res is not True:
                    return res
            if schema:
                is_valid = await self.validate_request(request, schema)
                if is_valid[0] is False:
                    return self.encode((is_valid[1], 422), encoder)
            data = await route_handler(request)
            return self.encode(data, encoder)

        return parser

    def custom_encoder(self, data, encoder):
        if encoder:
            return json.loads(json.dumps(data, cls=encoder))
        return data

    def encode(self, data, encoder):
        if isinstance(data, dict) or isinstance(data, list):
            return web.json_response(self.custom_encoder(data, encoder), status=200)
        elif isinstance(data, tuple) and len(data) == 2:
            return web.json_response(self.custom_encoder(data[0], encoder), status=data[1])
        else:
            return web.FileResponse(data)
