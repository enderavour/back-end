async def test_redis_connection(redis_client):
    await redis_client.set("ping", "pong")

    result = await redis_client.get("ping")

    assert result == "pong"
