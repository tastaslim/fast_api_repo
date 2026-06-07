from sqlalchemy.orm import Session
from app.db.schema.userSchema import UserSchema
from app.resources.user.userDtos import UserRegisterDto

class UserRepository:
    
    def getUserById(self, databaseCursor: Session, id: int) -> UserSchema:
        """
        Get a user by id
        :param databaseCursor: Session database cursor
        :param id: int
        :return: UserSchema
        """
        return databaseCursor.query(UserSchema).filter(UserSchema.id == id).first()
    
    def getUserByUsername(self, databaseCursor: Session, username: str) -> UserSchema:
        """
        Get a user by username
        :param databaseCursor: Session database cursor
        :param username: str
        :return: UserSchema
        """
        return databaseCursor.query(UserSchema).filter(UserSchema.username == username).first()
    
    def getUserByEmail(self, databaseCursor: Session, email: str) -> UserSchema:
        """
        Get a user by email
        :param databaseCursor: Session database cursor
        :param email: str
        :return: UserSchema
        """
        return databaseCursor.query(UserSchema).filter(UserSchema.email == email).first()
    
    def registerUser(self, databaseCursor: Session, request: UserRegisterDto) -> UserSchema:
        """
        Create a new user
        :param databaseCursor: Session database cursor
        :param request: UserRegisterDto
        :return: UserSchema
        """
        userSchema = UserSchema(
            name=request.name,
            username=request.username,
            email=request.email,
            password=request.password,
            isActive=True
        )
        databaseCursor.add(userSchema)
        databaseCursor.commit()
        databaseCursor.refresh(userSchema)
        return userSchema