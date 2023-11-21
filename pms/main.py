# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routes import vehicles, login_credentials, tags, parking_permissions

app = FastAPI()

# Add CORS middleware to enable Cross-Origin Resource Sharing
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["http://localhost:5173/", "http://localhost:8000/"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)

@app.middleware("http")
async def set_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Include the routers in your main app
app.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(login_credentials.router, prefix="/login_credentials", tags=["login_credentials"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(parking_permissions.router, prefix="/parking_permissions", tags=["parking_permissions"])
