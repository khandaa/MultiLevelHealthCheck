# main.py
from fastapi import FastAPI, HTTPException
import httpx,json
import yaml
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Optional


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load the configuration
try:
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
except Exception as e:
    logger.error("Failed to load configuration file: %s", e)
    raise e

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:9001",
    "http://localhost:9002",
    "http://localhost:9003",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

async def check_api_health(api_name: str,api_host:str, api_port:int):
    timeout = httpx.Timeout(5.0)  # 5 seconds timeout
    try:
        #print(f"{api_host}:{api_port}/{api_name}/health")
        health_status = httpx.get(f"{api_host}:{api_port}/{api_name}/health", timeout=timeout)
    except HTTPException as exc:
        logger.error("Request error while calling %s: %s", api_name, exc)
        health_status = json.loads({api_name: "Unhealthy"})
        return health_status
    return health_status


@app.get("/healthcheck")
async def healthcheck(api_name: Optional[str] = 'api1',api_host: Optional[str] = 'http://localhost',api_port:Optional[int] = 9001):
    try:
        health_status = await check_api_health(api_name=api_name, api_host = api_host, api_port=api_port)
        final_status = health_status.json()
        downstream = config[api_name]['downstream']
        for downstream_apis in downstream:
            downstream_api_name=downstream_apis['api_name']
            downstream_api_host=downstream_apis['api_host']
            downstream_api_port=downstream_apis['api_port']
            try:
                health_status = await check_api_health(api_name=downstream_api_name, api_host = downstream_api_host, api_port=downstream_api_port)
                #If the api call is successful add it to the success list
                final_status.update(health_status.json())
                # print(final_status)
            #if the API does not return a success response , add it to error list
            except HTTPException as exc:
                #health_status = json.loads({"status": "unhealthy", "detail": str(exc.detail)})
                health_status = json.loads({api_name: "Unhealthy"+str(exc.detail)})
                final_status.update(health_status.json())
        return final_status
    except HTTPException as exc:
        logger.error("Healthcheck failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"Healthcheck failed: {str(exc.detail)}")
