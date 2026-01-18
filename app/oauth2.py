from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # đường dẫn để tự động lấy token từ request của người dùng
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # Thêm thời gian hết hạn vào payload của token

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")

        if id is None:
            raise credential_exception
        
        token_Data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception

    return token_Data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)): # oauth2_scheme tự động trích xuất token từ header đi kèm trong HTTP request
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

# ==================== JWT Authentication Flow ====================
# 1. Client đến /docs → click "Authorize"
# 2. Nhập username/password
# 3. Browser gửi POST /login với credentials (username/password)
# 4. Server xác thực credentials, tạo token bằng create_access_token():
#    - Payload chứa: user_id, exp (thời gian hết hạn)
#    - Ký token với SECRET_KEY
#    - Trả token cho client
# 5. Browser lưu token (localStorage, sessionStorage, cookie...)
# 6. Browser tự động thêm vào mọi HTTP request header: Authorization: Bearer <token>
# 7. Mọi request tiếp theo (POST /posts, DELETE /posts/{id}...) đều kèm token
# 8. oauth2_scheme tự động rút trích token từ HTTP header
# 9. get_current_user() gọi verify_access_token():
#    - jwt.decode() kiểm tra chữ ký (signature) của token bằng SECRET_KEY (tái tạo lại signature từ payload + SECRET_KEY(trên server) và so sánh với signature trong token)
#    - Nếu signature hợp lệ → giải mã payload lấy user_id
#    - Nếu signature sai / token hết hạn → JWTError exception
# 10. Nếu token hợp lệ → lấy user từ database dùng user_id
# 11. Nếu token không hợp lệ → trả HTTP 401 Unauthorized
# 12. Server sử dụng current_user trong endpoint (VD: kiểm tra quyền delete)
# ================================================================
