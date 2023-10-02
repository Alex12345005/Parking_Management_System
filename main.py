from fastapi import FastAPI

app = FastAPI(title='Parking Management System (PMS)', description='API & Database for the Parking Managment System', version='0.1')

@app.on_event("startup")
async def startup():
    print("Connecting...")

@app.get("/")
async def root():
    return {"message": "Hello World!"}
