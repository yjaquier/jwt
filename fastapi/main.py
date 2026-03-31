from datetime import datetime, timedelta, timezone
import hashlib
from typing import Annotated
from pydantic import BaseModel
import mariadb
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, Body, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

SECRET_KEY = "your_secret_key_long_enough_to_satisfy_requirement" # 32 characters minimum
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class LoginUser(BaseModel):
  username: str
  password: str

class RegisterUser(BaseModel):
  firstname: str
  lastname: str
  username: str
  password: str

class Todo(BaseModel):
  item: str

class TodoId(BaseModel):
  id: int

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

# Connect to MariaDB Platform
def getMariaDBConnection() -> mariadb.Connection:
  """
  Connect to MariaDB Platform

  Returns
  -------
    mariadb.Connection
      A MariaDB connection
  """
  try:
    connection = mariadb.connect(
      user="jwt",
      password="secure_password",
      host="localhost",
      port=3306,
      database="jwt"
    )
    return connection
  except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    exit(1)

def getMariaDBCursor(connection: mariadb.Connection, buffered_cursor: bool | None = False) -> mariadb.Cursor:
  """
  Return a cursor from a connection

  Parameters
  ----------
    connection : mariadb.Connection
      MariaDB connection
    buffered_cursor : bool or None = False
      Wether or not the cursor will be buffered
  
  Returns
  -------
    mariadb.Cursor
      A MariaDB cursor
  """
  try:
    cursor = connection.cursor(buffered = buffered_cursor)
    return cursor
  except mariadb.Error as e:
    print(f"Error getting cursor from MariaDB Platform: {e}")
    exit(1)

def create_access_token(data: dict, expires_delta: timedelta | None = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    current_date = datetime.now(timezone.utc)
    if expires_delta:
      expire = current_date + expires_delta
    else:
      expire = current_date + timedelta(minutes = 15) # Default to 15 minutes
    to_encode.update({"exp": expire, "iat": current_date})
    encoded_jwt = jwt.encode(payload = to_encode, key = SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/#wildcards
origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#more-info

@app.post("/")
def homePage(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
  credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})
  # print(token)
  try:
    payload = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = [ALGORITHM])
    # print(payload)
    fullname = payload.get("firstname") + ' ' + payload.get("lastname")
    if fullname is None:
      raise credentials_exception
    # token_data = TokenData(username=username)
  except InvalidTokenError:
    raise credentials_exception
  # user = get_user(fake_users_db, username=token_data.username)
  # if user is None:
  #   raise credentials_exception
  return JSONResponse(content = { "fullname": fullname })

@app.post("/register")
async def register(form_data: Annotated[RegisterUser, Body()]) -> dict:
  # print(form_data)
  # print("Firstname: " + form_data.firstname + ", Lastname: "+ form_data.lastname)
  try:
    # We store hash of password and not password in clear obviously
    m = hashlib.sha256()
    m.update(form_data.password.encode("utf-8"))
    connection01 = getMariaDBConnection()
    cursor01 = getMariaDBCursor(connection01)
    sql01 = 'insert into users(firstname, lastname, username, password) values("' + form_data.firstname + '","' + form_data.lastname + '","' + form_data.username + '","' + m.hexdigest() + '")'
    # print(sql01)
    cursor01.execute(sql01)
    # Commit
    connection01.commit()
    # Close cursor and connection
    cursor01.close()
    connection01.close()
    return JSONResponse(content = {"registerStatus": "Success"})
  except mariadb.Error as e:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= {"registerStatus": "Failed", "Code": e.errno ,"Error": str(e)} )

@app.post("/login")
async def login(form_data: Annotated[LoginUser, Body()]) -> dict:
  try:
    m = hashlib.sha256()
    m.update(form_data.password.encode("utf-8"))
    connection01 = getMariaDBConnection()
    cursor01 = getMariaDBCursor(connection01, True)
    sql01 = 'select id, firstname, lastname from users where username = "' + form_data.username + '" and password = "' + m.hexdigest() + '"'
    # print(sql01)
    cursor01.execute(sql01)
    existing_user = cursor01.rowcount
    # print(existing_user)
    # Close cursor and connection
    if existing_user > 0:
      # for row in cursor01:
      #   existing_user = row[0]
      results = cursor01.fetchall()
      user_id = results[0][0]
      firtname = results[0][1]
      lastname = results[0][2]
      # print(user_id)
      cursor01.close()
      connection01.close()
      # return {"loginStatus": "Success"}
      return JSONResponse(content = { "access_token": create_access_token(data = { "id": user_id, "firstname": firtname, "lastname": lastname, "username": form_data.username }, expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)), "token_type": "Bearer" })
    else:
      cursor01.close()
      connection01.close()
      # return {"loginStatus": "Failed", "Reason": "Username/password mismatch"}
      raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= {"loginStatus": "Failed", "Code": 20000 , "Error": "Username/password mismatch"} )
  except mariadb.Error as e:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= {"loginStatus": "Failed", "Code": e.errno , "Error": str(e)} )

# Non required part to handle Todo lists
@app.get("/todos")
async def get_todos(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
  try:
    payload = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = [ALGORITHM])
    # print(payload)
    users_id = payload.get("id")
    if users_id is None:
      raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = {"Code": 20001 , "Error": "Invalid username"}, headers = {"WWW-Authenticate": "Bearer"})
    connection01 = getMariaDBConnection()
    cursor01 = getMariaDBCursor(connection01)
    sql01 = 'select id, item from todos where users_id = ' + str(users_id)
    # print(sql01)
    cursor01.execute(sql01)
    data = []
    for row in cursor01:
      data.append({"id": row[0], "item": row[1]})
    # Close cursor and connection
    cursor01.close()
    connection01.close()
    return JSONResponse(content = data)
  except mariadb.Error as e:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= {"registerStatus": "Failed", "Code": e.errno ,"Error": str(e)} )
  except InvalidTokenError as e:
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = {"Code": 20001 , "Error": "Invalid token"}, headers = {"WWW-Authenticate": "Bearer"})

@app.post("/todos")
async def create_todo(form_data: Annotated[Todo, Body()], token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
  try:
    item = form_data.item
    payload = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = [ALGORITHM])
    # print(payload)
    users_id = payload.get("id")
    connection01 = getMariaDBConnection()
    cursor01 = getMariaDBCursor(connection01)
    sql01 = 'insert into todos(id, users_id, item) select a.*, '+ str(users_id) + ', "' + item + '" from (select max(id)+1 from todos where users_id=1) a'
    # print(sql01)
    cursor01.execute(sql01)
    # Commit
    connection01.commit()
    # Close cursor and connection
    cursor01.close()
    connection01.close()
    return JSONResponse(content = { "Insert": "Success" })
  except mariadb.Error as e:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= {"Insert": "Failed", "Code": e.errno , "Error": str(e)} )
  except InvalidTokenError as e:
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = {"Code": 20001 , "Error": "Invalid token"}, headers = {"WWW-Authenticate": "Bearer"})

@app.delete("/todos/{todo_id}")
async def delete_todo(form_data: Annotated[TodoId, Body()], token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
  try:
    id = form_data.id
    payload = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = [ALGORITHM])
    # print(payload)
    users_id = payload.get("id")
    connection01 = getMariaDBConnection()
    cursor01 = getMariaDBCursor(connection01)
    sql01 = 'delete from todos where id = ' + str(id) + ' and users_id = ' + str(users_id)
    # print(sql01)
    cursor01.execute(sql01)
    # Commit
    connection01.commit()
    # Close cursor and connection
    cursor01.close()
    connection01.close()
    return JSONResponse(content = { "Delete": "Success" })
  except mariadb.Error as e:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= {"Delete": "Failed", "Code": e.errno , "Error": str(e)} )
  except InvalidTokenError as e:
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = {"Code": 20001 , "Error": "Invalid token"}, headers = {"WWW-Authenticate": "Bearer"})