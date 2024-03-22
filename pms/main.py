# app/main.py
from fastapi_login import LoginManager
from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import *
from .routes import vehicles, users, tags, parking_permissions, vehicle_parking_permission, rasp
from fastapi import Depends
from . import crud, models, schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.responses import RedirectResponse
from datetime import timedelta 

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.middleware("http")
async def set_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

SECRET = 'your-super-secret-key'
# Add the necessary configurations for the LoginManager
manager = LoginManager(
    SECRET,
    token_url='/login',
    use_cookie=True,
    cookie_name='custom-cookie-name',
    use_header=False,
    default_expiry=timedelta(hours=12)  # Set default expiration for tokens
)

@manager.user_loader()
def load_user(email: str, db: Session = Depends(get_db)):
    user_data = users.query_user(db, email)
    if user_data:
        return user_data
    return None

# Update the login route to use the set_cookie method
@app.post('/login')
def login(response: Response, data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("Login post start")
    print("Received data:", data.username, data.password)  # Print the received data
    username = data.username
    password = data.password

    # Use the query_user function with the correct argument
    user = crud.get_user_by_username(db, username)
    print("This is the User:", user)
    # Ensure user is an instance of schemas.Users
    if password == user.Password:
        access_token = manager.create_access_token(data={'sub': username})
        manager.set_cookie(response, access_token)  # Set the cookie
        return {'access_token':access_token}
    else:
        raise InvalidCredentialsException

# Include the routers in your main app
app.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(parking_permissions.router, prefix="/parking_permissions", tags=["parking_permissions"])
app.include_router(vehicle_parking_permission.router, prefix="/vehicle_parking_permissions", tags=["vehicle_parking_permissions"])
app.include_router(rasp.router, prefix="/rasp", tags=["rasp"])

class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(
    SECRET,
    token_url='/login',
    cookie_name='custom-cookie-name',
    use_cookie=True,
    use_header=False,
    custom_exception=NotAuthenticatedException
)

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url='/login')

@app.get('/protected')
def protected_route(user=Depends(manager)):
    return {'user': user}

@app.get('/protected_optional')
def protected_route_optional(user=Depends(manager.optional)):
    if user is None:
        # Do something for unauthorized users
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    return {'user': user}

@manager.user_loader()
def load_user(user_id, db: Session = Depends(get_db)):
    """
    Get a user from the db based on user ID
    :param user_id: ID of the user
    :param db: The currently active connection to the database
    :return: None or the user object
    """
    return crud.get_user_by_id(db, user_id)

@app.options("/login", response_model=None)
def login():
    return {}

@app.options("/protected", response_model=None)
def protected_route():
    return {}

@app.options("/protected_optional", response_model=None)
def protected_route_optional():
    return {}
