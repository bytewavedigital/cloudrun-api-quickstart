import aiohttp_cors
from aiohttp import web
from .route import Route
from .observer import reload
from .plugins import register
from .response import Response
from .aio_cinch_exception import AioCinchException
from .logger import Logger


class AioCinch:
    def __init__(self, config={}):
        self.config = config
        self.app = web.Application()
        if self.get_config('cors'):
            self.cors = aiohttp_cors.setup(self.app, defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
            })
        self.logger = Logger(self.get_config('logger'))

    def get_config(self, key):
        defaults = {
            'cors': False,
            'port': 8080,
            'logger': 'warn',
            'routes': {},
            'ws': {},
            'debug': False,
            'prefix': "",
            'version': "",
            'reload': False,
            'plugins': {},
            'pre_request': None,
            'encoder': None
        }
        mapped_config = {**defaults, **self.config}
        return mapped_config.get(key, None)

    def register_ws_handler(self, route, handler):
        try:
            return web.get(route, Response().handle_ws(handler))
        except Exception as e:
            raise AioCinchException(e)

    def register_handler(self, route, method, handler, encoder, schema):
        try:
            func = getattr(web, method.lower())
            return func(route, Response().handler(handler, encoder, schema, self.get_config('pre_request')))
        except Exception as e:
            raise AioCinchException(e)

    def register_routes(self):
        routes = []
        for key, value in self.get_config('routes').items():
            handlers = value.get('handlers', None)
            if not handlers:
                self.logger.info(f"No route handlers")
                continue
            for handler in handlers:
                if not isinstance(handler, Route):
                    self.logger.warn(
                        f"Handler {handler} must be an instance of Route class")
                    continue
                validate = handler.validate()
                if validate is not True:
                    self.logger.warn(
                        f"Route registration error for {key} errors: {validate}")
                    continue
                route = self.get_config('prefix') + \
                    self.get_config('version') + key
                routes.append(
                    self.register_handler(route, handler.method, handler.handler, self.get_config('encoder'),
                                          handler.req_schema))
                self.logger.info(
                    f"Route: {route} method: {handler.method} Registered")
        self.app.add_routes(routes)
        if self.get_config("cors"):
            for route in list(self.app.router.routes()):
                self.cors.add(route)

    def register_plugin(self):
        for key, value in register(self.get_config('plugins')).items():
            self.app[key] = value

    def register_ws(self):
        ws = []
        for key, value in self.get_config('ws').items():
            ws.append(self.register_ws_handler(key, value))
        self.app.add_routes(ws)

    def run(self, file):
        try:
            self.register_routes()
            self.register_ws()
            self.register_plugin()
            if self.get_config('reload'):
                self.logger.info("Enabled live reloading")
                reload(file, self.logger)
            web.run_app(self.app, port=self.get_config('port'))
        except Exception as e:
            raise AioCinchException(e)
