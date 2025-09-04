from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import  schemas, models, database, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model = schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {'access_token': access_token, "token_type": "bearer"}
"""
Với Depends(database.get_db): truyền vào một hàm, FastAPI sẽ gọi hàm này để lấy dữ liệu (ở đây là kết nối database).
Với Depends(): không truyền đối số, thường dùng với các class đặc biệt của FastAPI như OAuth2PasswordRequestForm.
FastAPI sẽ tự động tạo instance của class này từ dữ liệu request (form-data: username, password).

Depends(): FastAPI thấy bạn khai báo Depends() trong hàm, nên sẽ tự động xử lý dependency.
OAuth2PasswordRequestForm: FastAPI dùng class này để lấy dữ liệu từ request (form-data: username, password) và tạo một instance.
user_credentials: Instance của OAuth2PasswordRequestForm được gán vào biến này, để bạn sử dụng trong hàm.
Tóm lại:
FastAPI → gọi Depends() → tạo object OAuth2PasswordRequestForm từ request → gán vào biến user_credentials.

Depends có thể nhận đối số hoặc không:
- Nếu truyền hàm/class vào Depends, FastAPI sẽ gọi hàm/class đó để lấy dữ liệu và truyền vào biến.
- Nếu dùng Depends() không truyền gì, FastAPI sẽ tự động tạo instance của class đặc biệt từ dữ liệu request.
"""