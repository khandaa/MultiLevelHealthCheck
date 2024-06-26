from fastapi import FastAPI

api4 = FastAPI()

@api4.get("/api4/health")
async def api4_health():
    # No downstream for API 4
    return {"api4": "healthy"}
