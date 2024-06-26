from fastapi import FastAPI

api3 = FastAPI()

@api3.get("/api3/health")
async def api3_health():
    # No downstream for API 2
    return {"api3": "healthy"}
