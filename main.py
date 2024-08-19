from fastapi import FastAPI
from endpoints import router as api_router
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Include the router from endpoints.py
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Zomato Data API"}
