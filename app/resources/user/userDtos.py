from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserLoginDto(BaseModel):
    username: str
    password: str

class UserRegisterDto(BaseModel):
    name: str
    username: str
    email: str
    password: str

class UserAuthenticatedResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    username: str
    email: str

class UserRegisterResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    username: str
    email: str
    createdAt: datetime
    updatedAt: datetime