"""
Lightweight HTTP server so Render's health-check pings don't
kill the service. Runs as an asyncio task alongside the bot.
"""
import asyncio
import logging
from aiohttp import web

logger = logging.getLogger(__name__)


async def health(request):
    return web.Response(text="OK ✅", status=200)


async def run_http_server(port: int = 8080):
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"🌐 Health-check server listening on port {port}")

    # Run forever
    while True:
        await asyncio.sleep(3600)
