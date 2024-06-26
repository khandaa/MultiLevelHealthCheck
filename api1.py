from fastapi import FastAPI

api1 = FastAPI()

@api1.get("/api1/health")
async def api1_health():
    # No downstream for API 3
    return {"api1": "healthy"}
