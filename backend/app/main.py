from fastapi import FastAPI
from app.routes import auth,bookmark_route,user_route,paper_route,collection_paper_route,collection_route,topic
from app.routes.ingestion import router as ingestion_router
from app.routes.note_route import router as note_router
from app.routes import paper_content


app=FastAPI()
@app.get("/")
async def root():
    return {"message":"Research Paper Assistant API"}
@app.get("/health")
async def health():
    return { "status": "healthy"}
app.include_router(auth.router)
app.include_router(user_route.router)
app.include_router(paper_route.router)
app.include_router(bookmark_route.router)
app.include_router(collection_route.router)
app.include_router(collection_paper_route.router)
app.include_router(ingestion_router)
app.include_router(topic.router)
app.include_router(note_router)
app.include_router(paper_content.router)






