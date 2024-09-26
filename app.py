from fastapi import FastAPI, Depends, Form, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import sqlite3
from datetime import datetime, timedelta
import jwt
import bcrypt

# 설정
SECRET_KEY = "your_secret_key"  # 비밀 키
ALGORITHM = "HS256"  # 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 액세스 토큰 유효 기간(분)

app = FastAPI()
manager = OAuth2PasswordBearer(tokenUrl="/token")
con = sqlite3.connect('your_database.db')
cur = con.cursor()

# 예외 처리 클래스
class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid credentials")

# 비밀번호 해시화 함수
def hash_password(password: str) -> str:
    # 비밀번호를 바이트로 인코딩
    password_bytes = password.encode('utf-8')
    
    # 해시화하고 소금을 추가
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    
    # 해시된 비밀번호를 문자열로 반환
    return hashed.decode('utf-8')

# 사용자 쿼리 함수
def query_user(user_id: str):
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE id=?
                       """, (user_id,)).fetchone()
    return user

# 액세스 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 로그인 엔드포인트
@app.post('/login')
def login(
    id: Annotated[str, Form()],
    password: Annotated[str, Form()],
    response: Response  # Response 객체 추가
):
    user = query_user(id)
    if not user:
        raise InvalidCredentialsException()

    # 입력한 비밀번호를 해시화하여 데이터베이스와 비교
    if hash_password(password) != user['password']:
        raise InvalidCredentialsException()

    # 액세스 토큰 생성
    access_token = create_access_token(data={
        'sub': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email']
        }
    })

    # 쿠키에 액세스 토큰 저장
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)

    return JSONResponse(content={'message': 'Login successful'})

# 회원가입 엔드포인트
@app.post('/signup')
def signup(
    id: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
):
    # 비밀번호 해시화
    hashed_password = hash_password(password)

    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES (?, ?, ?, ?)
                """, (id, name, email, hashed_password))
    con.commit()
    return JSONResponse(content={'message': 'User registered successfully'}, status_code=201)

# 보호된 리소스에 접근하는 엔드포인트
@app.get('/secure-data')
def secure_data(response: Response, token: str = Depends(manager)):
    # 액세스 토큰을 이용해 보호된 리소스에 접근
    return JSONResponse(content={"data": "This is protected data."})

