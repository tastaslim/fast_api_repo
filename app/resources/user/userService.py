from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi.security import HTTPAuthorizationCredentials
from app.common.utils.authentication import validateToken
from app.common.utils.errorClasses import DuplicateUserError, InvalidCredentialsError, UserNotFoundError
from app.db.settings import getSettings
from app.resources.user.userRespository import UserRepository
from app.resources.user.userDtos import UserAuthenticatedResponseDto, UserLoginDto, UserRegisterDto, UserRegisterResponseDto
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from app.common.utils.jwtUtil import JwtService
passwordHash = PasswordHash.recommended()

class UserService:
    def __init__(self):
        self.userRepository = UserRepository()
    
    def __generatePasswordHash(self, password: str) -> str:
        """
        Generate a password hash
        :param password: str
        :return: str
        """
        return passwordHash.hash(password)
    
    def __verifyPassword(self, password: str, hashedPassword: str) -> bool:
        """
        Verify a password
        :param password: str plain text password
        :param hashedPassword: str hashed password
        :return: bool
        """
        return passwordHash.verify(password=password, hash=hashedPassword)
        
    async def registerUser(self, userPayload: UserRegisterDto, databaseCursor: Session) -> UserRegisterResponseDto:
        """
        Register a new user
        :param userPayload: UserRegisterDto
        :param databaseCursor: Session database cursor
        :return: UserRegisterResponseDto
        """
        doesUsernameExist = self.userRepository.getUserByUsername(databaseCursor=databaseCursor, username=userPayload.username)
        doesEmailExist = self.userRepository.getUserByEmail(databaseCursor=databaseCursor, email=userPayload.email)
        if doesUsernameExist or doesEmailExist:
            raise DuplicateUserError()
        hashedPassword = self.__generatePasswordHash(password=userPayload.password)
        userPayload.password = hashedPassword
        userSchema = self.userRepository.registerUser(databaseCursor=databaseCursor, request=userPayload)
        return UserRegisterResponseDto.model_validate(userSchema)
    
    async def loginUser(self, userPayload: UserLoginDto, databaseCursor: Session):
        """
        Login a user
        :param userPayload: UserLoginDto
        :param databaseCursor: Session database cursor
        :return: UserLoginResponseDto
        """
        
        appSettings = getSettings()
        jwtService = JwtService(secretKey=appSettings.SECRET_KEY, algorithm=appSettings.ALGORITHM)
        expiresInMinutes: int = appSettings.ACCESS_TOKEN_EXPIRE_MINUTES
        user = self.userRepository.getUserByUsername(databaseCursor=databaseCursor, username=userPayload.username)
        if not user:
            raise UserNotFoundError()
        doesPasswordMatch = self.__verifyPassword(password=userPayload.password, hashedPassword=user.password)
        if not doesPasswordMatch:
            raise InvalidCredentialsError()
        # If password is correct, generate a JWT token
        claims: Dict[str, Any] = {
            "id": user.id,
            "username": user.username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expiresInMinutes)
        }
        token: str = jwtService.generateToken(claims=claims)
        return token
    
    async def decodeToken(self, token: str) -> Dict[str, Any]:
        """
        Check if a user is authenticated
        :param token: str
        :return: bool
        """
        appSettings = getSettings()
        jwtService: JwtService = JwtService(secretKey=appSettings.SECRET_KEY, algorithm=appSettings.ALGORITHM)
        decodedToken: Dict[str, Any] = jwtService.decodeToken(token=token)
        return decodedToken
            
    
    async def validateToken(self, jwtToken: str, databaseCursor: Session) -> UserAuthenticatedResponseDto:
        """
        Validate a JWT token
        :param jwtToken: str JWT token
        :param databaseCursor: Session database cursor
        :return: UserSchema
        """ 
        user = validateToken(credentials=HTTPAuthorizationCredentials(credentials=jwtToken, scheme="Bearer"), databaseCursor=databaseCursor)
        return UserAuthenticatedResponseDto.model_validate(user)