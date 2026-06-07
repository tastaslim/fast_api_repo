from typing import Annotated
from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from app.common.utils.apiResponseUtil import toJsonResponse
from app.db.database import getDatabase
from sqlalchemy.orm import Session
from app.resources.user.userDtos import UserLoginDto, UserRegisterDto, UserRegisterResponseDto
from app.resources.user.userHandler import UserHandler
userRoute: APIRouter = APIRouter(prefix="/api/v1/users", tags=["Users"])
userHandler = UserHandler()


@userRoute.post(path="/register", response_model=UserRegisterResponseDto, status_code=status.HTTP_201_CREATED)
async def registerUser(request: UserRegisterDto,databaseCursor: Session = Depends(getDatabase)) -> JSONResponse:
    userResponse = await userHandler.registerUser(userPayload=request, databaseCursor=databaseCursor)
    return toJsonResponse(userResponse)

@userRoute.post(path="/login", response_model=str, status_code=status.HTTP_200_OK)
async def loginUser(request: UserLoginDto, databaseCursor: Session = Depends(getDatabase)) -> JSONResponse:
    loginResponse = await userHandler.loginUser(userPayload=request, databaseCursor=databaseCursor)
    return toJsonResponse(loginResponse)

@userRoute.get(path="/authenticate", status_code=status.HTTP_200_OK)
async def isUserAuthenticated(authorization: Annotated[str, Header(alias="Authorization", description="JWT access token. Required. Format: `Bearer <JwtToken>`")],    databaseCursor: Session = Depends(getDatabase)) -> JSONResponse:
    """
    Validates the JWT sent in the **Authorization** header (`Bearer <token>`).
    """
    userCredentials = await userHandler.validateToken(authorization=authorization, databaseCursor=databaseCursor)
    return toJsonResponse(userCredentials)
