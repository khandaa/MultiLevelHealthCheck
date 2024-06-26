from fastapi import FastAPI

api2 = FastAPI()

@api2.get("/api2/health")
async def api2_health():
    # No downstream for API 2
    return {"api2": "healthy"}
