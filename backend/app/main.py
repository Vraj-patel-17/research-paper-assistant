from fastapi import FastAPI
from app.routes import auth,bookmark_route,user_route,paper_route,collection_paper_route,collection_route,topic
from app.routes.ingestion import router as ingestion_router
from app.routes.note_route import router as note_router
from app.routes.summary_route import router as summary_router
from app.core.logging import setup_logging
from app.routes import recommendation_route
from app.routes import chat_routes
from app.routes import health
from app.core.exception_handlers import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from app.core.rate_limiter import limiter
from app.core.config import settings
setup_logging()
app=FastAPI(title="Research Paper Assistant API",
    description="Backend API for AI-powered research paper discovery and analysis.",
    version="1.0.0",)

app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter
app.add_exception_handler( RateLimitExceeded, _rate_limit_exceeded_handler,)
register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"])

app.add_middleware(SecurityHeadersMiddleware)
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(user_route.router)
app.include_router(paper_route.router)
app.include_router(bookmark_route.router)
app.include_router(collection_route.router)
app.include_router(collection_paper_route.router)
app.include_router(ingestion_router)
app.include_router(topic.router)
app.include_router(note_router)
app.include_router(summary_router)
app.include_router(recommendation_route.router)
app.include_router(chat_routes.router)






