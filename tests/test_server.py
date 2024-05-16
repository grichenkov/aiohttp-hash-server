import pytest
from aiohttp import web

from app.app import hash_string, healthcheck


@pytest.fixture
async def cli(aiohttp_client):
    app = web.Application()
    app.router.add_get("/healthcheck", healthcheck)
    app.router.add_post("/hash", hash_string)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_healthcheck(cli):
    client = await cli
    resp = await client.get("/healthcheck")
    assert resp.status == 200
    assert await resp.json() == {}


@pytest.mark.asyncio
async def test_hash_string_success(cli):
    client = await cli
    data = {"string": "hello"}
    resp = await client.post("/hash", json=data)
    assert resp.status == 200
    result = await resp.json()
    assert "hash_string" in result


@pytest.mark.asyncio
async def test_hash_string_missing_field(cli):
    client = await cli
    data = {}
    resp = await client.post("/hash", json=data)
    assert resp.status == 400
    result = await resp.json()
    assert "error" in result
    assert result["error"] == "Empty request body"


@pytest.mark.asyncio
async def test_hash_string_invalid_json(cli):
    client = await cli
    resp = await client.post("/hash", json={"data": 123})
    assert resp.status == 400
    result = await resp.json()
    assert "validation_errors" in result
    assert result["validation_errors"] == 'Field "string" is required'


@pytest.mark.asyncio
async def test_hash_string_empty_request(cli):
    client = await cli
    resp = await client.post("/hash", data="")
    assert resp.status == 400
    result = await resp.json()
    assert "error" in result
    assert result["error"] == "Invalid JSON format in request"
