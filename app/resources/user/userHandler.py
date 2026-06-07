import logging
from sqlalchemy.orm import Session
from app.common.models.apiResponseModel import ApiResponse
from app.resources.user.userDtos import UserAuthenticatedResponseDto, UserLoginDto, UserRegisterDto, UserRegisterResponseDto
from app.resources.user.userService import UserService
from app.common.utils.errorClasses import DuplicateUserError, InvalidCredentialsError, UnauthorizedAccessError, UserNotFoundError
userService = UserService()

class UserHandler:
    
    async def registerUser(self, userPayload: UserRegisterDto, databaseCursor: Session) -> ApiResponse[UserRegisterResponseDto]:
        """
        Register a new user
        :param userPayload: UserRegisterDto
        :param databaseCursor: Session database cursor
        :return: ApiResponse[UserRegisterResponseDto]
        """
        try:
            userResponse = await userService.registerUser(userPayload=userPayload, databaseCursor=databaseCursor)
            return ApiResponse(status=200, message="User registered successfully", data=userResponse)
        except DuplicateUserError as e:
            return ApiResponse(status=409, message=str(e), data=None)
        except Exception as e:
            logging.error(msg=f"error=Error registering user: {e}")
            return ApiResponse(status=500, message=f"Internal server error", data=None)
    
    async def loginUser(self, userPayload: UserLoginDto, databaseCursor: Session) -> ApiResponse[str]:
        """
        Login a user
        :param userPayload: UserLoginDto
        :param databaseCursor: Session database cursor
        :return: ApiResponse[UserLoginResponseDto]
        """
        try:
            token: str = await userService.loginUser(userPayload=userPayload, databaseCursor=databaseCursor)
            return ApiResponse(status=200, message="User logged in successfully", data=token)
        except (InvalidCredentialsError, UserNotFoundError) as e:
            return ApiResponse(status=401, message=str(e), data=None)
        except Exception as e:
            logging.error(msg=f"error=Error logging in user: {e}")
            return ApiResponse(status=500, message=f"Internal server error", data=None)
    
    async def validateToken(self, authorization: str, databaseCursor: Session) -> ApiResponse[UserAuthenticatedResponseDto]:
        """
        Validate JWT from the ``Authorization: Bearer <token>`` header.
        """
        try:
            user = await userService.validateToken(jwtToken=authorization, databaseCursor=databaseCursor)
            return ApiResponse(status=200, message="User is authenticated", data=user)
        except (UnauthorizedAccessError, UserNotFoundError) as e:
            return ApiResponse(status=401, message=str(e), data=None)
        except Exception as e:
            logging.error(msg=f"error=Error checking if user is authenticated: {e}")
            return ApiResponse(status=500, message="Internal server error", data=None)