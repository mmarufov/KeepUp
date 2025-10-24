from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.feed import router as feed_router
from .routers.ingest import router as ingest_router


def create_app() -> FastAPI:
    app = FastAPI(title="KeepUp Backend", version="0.1.0")

    # CORS: allow local iOS simulator and dev
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://127.0.0.1",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict:
        return {"ok": True}

    app.include_router(feed_router, prefix="")
    app.include_router(ingest_router, prefix="")
    return app


app = create_app()


