from fastapi import FastAPI
app=FastAPI()
@app.get("/")
async def root():
    return {"message":"Research Paper Assistant API"}
@app.get("/health")
async def health():
    return { "status": "healthy"}