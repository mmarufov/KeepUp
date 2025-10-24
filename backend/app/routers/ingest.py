from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx
import hashlib


router = APIRouter()


SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")


async def supabase_upsert(session: httpx.AsyncClient, table: str, payload: dict):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=representation",
    }
    r = await session.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    data = r.json()
    return data[0] if isinstance(data, list) and data else data


class IngestResponse(BaseModel):
    inserted: int


@router.post("/ingest/top-headlines", response_model=IngestResponse)
async def ingest_top_headlines():
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(status_code=500, detail="Supabase is not configured")
    if not NEWS_API_KEY:
        raise HTTPException(status_code=500, detail="NEWS_API_KEY is not set")

    params = {
        "language": "en",
        "pageSize": 50,
        "apiKey": NEWS_API_KEY,
    }
    inserted = 0
    async with httpx.AsyncClient() as session:
        r = await session.get("https://newsapi.org/v2/top-headlines", params=params, timeout=30)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        payload = r.json()
        for a in payload.get("articles", []):
            url = (a.get("url") or "").strip()
            if not url:
                continue
            url_hash = hashlib.sha256(url.encode()).hexdigest()
            up = await supabase_upsert(
                session,
                "articles",
                {
                    "url": url,
                    "url_hash": url_hash,
                    "title": a.get("title"),
                    "description": a.get("description"),
                    "content": a.get("content"),
                    "source": (a.get("source") or {}).get("name"),
                    "author": a.get("author"),
                    "published_at": a.get("publishedAt"),
                    "image_url": a.get("urlToImage"),
                    "lang": "en",
                },
            )
            if up:
                inserted += 1

    return IngestResponse(inserted=inserted)



