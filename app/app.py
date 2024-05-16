import hashlib
import json

import click
from aiohttp import web

HTTP_STATUS_BAD_REQUEST = 400


async def healthcheck(request):
    return web.json_response({})


async def hash_string(request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response(
            {"error": "Invalid JSON format in request"},
            status=HTTP_STATUS_BAD_REQUEST,
        )
    except Exception as es:
        return web.json_response(
            {"error": str(es)},
            status=HTTP_STATUS_BAD_REQUEST,
        )

    if not data:
        return web.json_response(
            {"error": "Empty request body"},
            status=HTTP_STATUS_BAD_REQUEST,
        )

    if not isinstance(data, dict):
        return web.json_response(
            {"error": "Request body must be a JSON object"},
            status=HTTP_STATUS_BAD_REQUEST,
        )

    if "string" not in data:
        return web.json_response(
            {"validation_errors": 'Field "string" is required'},
            status=HTTP_STATUS_BAD_REQUEST,
        )

    input_string = data["string"]
    if not isinstance(input_string, str):
        return web.json_response(
            {"validation_errors": 'Field "string" must be a string'},
            status=HTTP_STATUS_BAD_REQUEST,
        )

    hash_value = hashlib.sha256(input_string.encode()).hexdigest()
    return web.json_response({"hash_string": hash_value})


@click.command()
@click.option("--host", default="0.0.0.0", help="Host IP")
@click.option("--port", default=8080, help="Port number")
def run_server(host, port):
    app = web.Application()
    app.router.add_get("/healthcheck", healthcheck)
    app.router.add_post("/hash", hash_string)
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
