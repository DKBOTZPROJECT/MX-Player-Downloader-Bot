"""Gofile.io upload helper used when a file is larger than Telegram's upload limit."""

import asyncio
import json
import os

import aiohttp

GOFILE_SERVERS_URL = "https://api.gofile.io/servers"


class _ProgressFile:
    """Synchronous file wrapper that records bytes read in a shared state dict.

    aiohttp reads file-like payloads from a default executor thread, so the
    callback used for progress runs on the event loop side via a polling task
    (see `upload_to_gofile`) to avoid cross-thread coroutine scheduling.
    """

    def __init__(self, path, state):
        self._fp = open(path, "rb")
        self._state = state

    def read(self, size=-1):
        chunk = self._fp.read(size)
        if chunk:
            self._state["read"] += len(chunk)
        return chunk

    def close(self):
        try:
            self._fp.close()
        except Exception:
            pass


async def _get_server(session, token=None, zone=None):
    params = {}
    if zone:
        params["zone"] = zone

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    timeout = aiohttp.ClientTimeout(total=30)
    async with session.get(
        GOFILE_SERVERS_URL,
        params=params or None,
        headers=headers,
        timeout=timeout,
    ) as resp:
        text = await resp.text()

    try:
        data = json.loads(text)
    except Exception as e:
        raise RuntimeError(f"Bad gofile servers response: {text[:200]}") from e

    if data.get("status") != "ok":
        raise RuntimeError(f"Failed to get gofile servers: {data}")

    servers = (data.get("data") or {}).get("servers") or []
    if not servers:
        raise RuntimeError("No gofile servers available")

    return servers[0]["name"]


async def upload_to_gofile(file_path, on_progress=None, token=None, zone=None, poll_interval=2.0):
    """Upload `file_path` to gofile.io and return the response `data` dict.

    Parameters
    ----------
    file_path : str
        Path of the file to upload.
    on_progress : Optional[Callable[[int, int], Awaitable[None]]]
        Async callable invoked roughly every `poll_interval` seconds with the
        number of bytes uploaded so far and the total file size.
    token : Optional[str]
        Gofile account token. When omitted, a guest account is used.
    zone : Optional[str]
        Optional gofile zone (`eu` or `na`) to prefer when picking a server.
    poll_interval : float
        Seconds between progress callback invocations.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    total = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    state = {"read": 0, "done": False}

    async def _poll_progress():
        if not on_progress:
            return
        while not state["done"]:
            try:
                await on_progress(state["read"], total)
            except Exception:
                pass
            try:
                await asyncio.sleep(poll_interval)
            except asyncio.CancelledError:
                break

    timeout = aiohttp.ClientTimeout(total=None, sock_connect=30, sock_read=None)
    connector = aiohttp.TCPConnector(force_close=True)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        server = await _get_server(session, token=token, zone=zone)
        upload_url = f"https://{server}.gofile.io/contents/uploadfile"

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        progress_task = asyncio.create_task(_poll_progress())
        f = _ProgressFile(file_path, state)
        try:
            form = aiohttp.FormData()
            if token:
                form.add_field("token", token)
            form.add_field(
                "file",
                f,
                filename=filename,
                content_type="application/octet-stream",
            )

            async with session.post(upload_url, data=form, headers=headers) as resp:
                text = await resp.text()
                try:
                    result = json.loads(text)
                except Exception as e:
                    raise RuntimeError(f"Bad gofile upload response: {text[:200]}") from e
        finally:
            state["done"] = True
            f.close()
            progress_task.cancel()
            try:
                await progress_task
            except (asyncio.CancelledError, Exception):
                pass

    if result.get("status") != "ok":
        raise RuntimeError(f"Gofile upload failed: {result}")

    if on_progress:
        try:
            await on_progress(total, total)
        except Exception:
            pass

    return result.get("data") or {}
