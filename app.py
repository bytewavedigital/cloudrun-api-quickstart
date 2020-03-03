from core.aio_cinch import AioCinch
from core.route import Route


async def post_handler(request):
    return {"message": "hello REST POST"}, 200


async def handler(request):
    return {"message": "hello REST"}, 422


if __name__ == "__main__":
    config = {
        "reload": True,
        "logger": "debug",
        "cors": True,
        "port": 8080,
        "routes": {
            "/": {
                "handlers": [Route(method="GET", handler=handler)],
            }
        },
        "prefix": "/api"
    }
    AioCinch(config).run(__file__)
