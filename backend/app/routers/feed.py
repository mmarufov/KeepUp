from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import os
import httpx


router = APIRouter()


class PersonalizedFeedItem(BaseModel):
    article_id: int
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    source: str | None = None
    published_at: str | None = None
    lang: str | None = None
    score: float | None = None


SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")


async def supabase_rpc(session: httpx.AsyncClient, name: str, payload: dict):
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(status_code=500, detail="Supabase is not configured")
    url = f"{SUPABASE_URL}/rest/v1/rpc/{name}"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }
    r = await session.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.json()


@router.get("/feed/personalized", response_model=list[PersonalizedFeedItem])
async def get_personalized_feed(
    user_id: str = Query(..., description="Auth user id (UUID)"),
    limit: int = Query(20, ge=1, le=100),
    before: str | None = Query(None),
):
    payload = {"p_user_id": user_id, "p_limit": limit, "p_before": before}
    async with httpx.AsyncClient() as session:
        data = await supabase_rpc(session, "get_personalized_feed", payload)
        return data


class InteractionIn(BaseModel):
    article_id: int
    kind: str
    dwell_ms: int | None = None


@router.post("/interaction")
async def log_interaction(body: InteractionIn):
    async with httpx.AsyncClient() as session:
        data = await supabase_rpc(
            session,
            "log_interaction",
            {"p_article_id": body.article_id, "p_kind": body.kind, "p_dwell_ms": body.dwell_ms},
        )
        return data


