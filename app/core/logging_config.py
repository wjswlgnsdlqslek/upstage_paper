import os
import sys
import time
import uuid
from typing import Optional

from fastapi import Request
from loguru import logger

# ---------------------------
# Loguru configuration (Step 1-A)
# ---------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "0") == "1"
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "app/log/app.log")

logger.remove()
logger.add(
    sys.stdout,
    level=LOG_LEVEL,
    backtrace=False,
    diagnose=False,
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[request_id]} | {message}",
)
if LOG_TO_FILE:
    logger.add(
        LOG_FILE_PATH,
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        level=LOG_LEVEL,
        enqueue=True,
        backtrace=False,
        diagnose=False,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[request_id]} | {message}",
    )

# 로깅 시 과도한 페이로드/민감정보 노출 방지
MAX_BODY_LOG_BYTES = int(os.getenv("MAX_BODY_LOG_BYTES", "4096"))
REDACT_HEADERS = {"authorization", "cookie", "set-cookie"}


# ---------------------------
# Logging Middleware (Step 1-B/1-C)
# ---------------------------
def _redact_headers(headers: dict) -> dict:
    out = {}
    for k, v in headers.items():
        if k.lower() in REDACT_HEADERS:
            out[k] = "<redacted>"
        else:
            out[k] = v
    return out


def _safe_decode(data: bytes) -> str:
    if not data:
        return ""
    chunk = data[:MAX_BODY_LOG_BYTES]
    try:
        text = chunk.decode("utf-8")
    except Exception:
        return f"<{len(data)} bytes binary>"
    if len(data) > MAX_BODY_LOG_BYTES:
        text += f"... <truncated {len(data) - MAX_BODY_LOG_BYTES} bytes>"
    return text


async def log_http(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    log = logger.bind(request_id=request_id)

    start = time.perf_counter()

    # --- Request logging (Step 1-B) ---
    req_headers = {
        "host": request.headers.get("host"),
        "user-agent": request.headers.get("user-agent"),
        "content-type": request.headers.get("content-type"),
        "authorization": request.headers.get("authorization"),
    }
    # 가능한 헤더를 구조적으로 남기되, 민감정보는 마스킹
    req_headers = _redact_headers({k: v for k, v in req_headers.items() if v is not None})

    query_params = dict(request.query_params)

    body_text: Optional[str] = None
    if request.method in {"POST", "PUT", "PATCH"}:
        try:
            body_bytes = await request.body()
            body_text = _safe_decode(body_bytes)
            # body를 읽으면 downstream에서 못 읽는 이슈가 있어 receive를 재주입
            async def receive():
                return {"type": "http.request", "body": body_bytes, "more_body": False}
            request._receive = receive  # type: ignore[attr-defined]
        except Exception:
            body_text = "<unavailable>"

    log.info(
        "REQ method={method} url={url} path={path} query={query} headers={headers}{body}",
        method=request.method,
        url=str(request.url),
        path=request.url.path,
        query=query_params,
        headers=req_headers,
        body=(f" body={body_text}" if body_text else ""),
    )

    # --- Response handling ---
    try:
        response = await call_next(request)
    except Exception:
        log.exception("ERR method={method} path={path}", method=request.method, path=request.url.path)
        raise

    duration_ms = (time.perf_counter() - start) * 1000

    # --- Response logging (Step 1-C) ---
    res_headers = {
        "content-type": response.headers.get("content-type"),
        "content-length": response.headers.get("content-length"),
    }
    res_headers = {k: v for k, v in res_headers.items() if v is not None}

    # response body 로깅 (가능한 경우에만, 스트리밍/대용량은 truncate)
    resp_body_text: Optional[str] = None
    if hasattr(response, "body") and isinstance(getattr(response, "body", None), (bytes, bytearray)):
        resp_body_text = _safe_decode(response.body)  # type: ignore[arg-type]

    log.info(
        "RES status={status} headers={headers}{body} duration_ms={duration_ms:.1f}",
        status=getattr(response, "status_code", None),
        headers=res_headers,
        body=(f" body={resp_body_text}" if resp_body_text else ""),
        duration_ms=duration_ms,
    )

    response.headers["X-Request-ID"] = request_id
    return response
