from operator import le
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel): # Send from user to server
    """
    This is schema/pydantic model that defines the structure of a request & response
    This ensure that when a user wants to create a post, the request will only go through if it has a "title" and "content" in the request body.
    """
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase): # Send from user to server
    pass

class Post(PostBase): # Send from server to user (does not include "id" and "created_at")
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    """
    Lỗi xảy ra khi bạn kế thừa PostBase cho PostOut thay vì kế thừa trực tiếp từ BaseModel.
    Vì sao lại lỗi?
    - PostBase có các trường như title, content, published.
    - Khi bạn khai báo class PostOut(PostBase): ..., Pydantic mong đợi object trả về từ API phải có đủ các trường này ở ngoài cùng (ví dụ: title, content, published, ...).
    - Nhưng thực tế, bạn trả về dữ liệu dạng {"Post": Post, "Votes": int} (tức là các trường title, content nằm trong object Post, không phải ở ngoài cùng).
    - Do đó, Pydantic báo lỗi "Field required" vì không tìm thấy các trường này ở ngoài cùng của response.
    - Khi sửa lại thành class PostOut(BaseModel): ...
    -> Pydantic chỉ mong đợi các trường bạn khai báo trực tiếp trong PostOut (ví dụ: Post, Votes). Dữ liệu trả về từ API sẽ khớp với schema:
    {
    "Post": {...},
    "Votes": 5
    }
    - Không còn lỗi thiếu trường nữa.

    """
    Post: Post
    Votes: int
    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: bool  # 1 or 0 