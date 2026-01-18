from datetime import datetime, timezone
from typing import Optional

from fastapi import Request
from starlette_context import context


def build_link_from_base_url(path: str) -> str:
    base_url = context.get("base_url")
    return f"{base_url}api/v1/{path}"


def set_origin_from_request(request: Request) -> str:
    origin = request.headers.get("origin")
    if origin:
        return origin
    host = request.headers.get("host")
    scheme = request.url.scheme
    return f"{scheme}://{host}"


def get_base_url() -> str:
    return context.get("base_url")


def get_request_origin() -> str:
    return context.get("origin")


def build_serial_no(name: str, id: int):
    prefix = name.upper().ljust(3, "X")[:3]
    current_year = str(datetime.now(timezone.utc).year)

    return f"{prefix}-{current_year}-{str(id).zfill(4)}"


def get_current_and_total_pages(limit: int, total: Optional[int] = None, offset: Optional[int] = None):
    if limit <= 0:
        raise ValueError("Limit must be greater than 0")

    if offset is None:
        offset = 0

    if total is None:
        total = 0

    if offset < 0:
        offset = 0

    current_page = (offset // limit) + 1
    total_pages = max(1, (total + limit - 1) // limit) if total > 0 else 1

    return current_page, total_pages
