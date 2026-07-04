from fastapi import FastAPI
from app.routes import auth,bookmark_route,user_route,paper_route,collection_paper_route,collection_route

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







