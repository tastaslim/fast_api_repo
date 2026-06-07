from typing import Any
import jwt

class JwtService:
    def __init__(self, secretKey: str, algorithm: str) -> None:
        self._secretKey: str = secretKey
        self._algorithm: str = algorithm

    def generateToken(self, claims: dict[str, Any]) -> str:
        """
        Generate a JWT token
        :param claims: dict[str, Any]
        :return: str
        """
        return jwt.encode(payload=claims, key=self._secretKey, algorithm=self._algorithm)  # pyright: ignore[reportUnknownMemberType] — PyJWT stubs omit full overloads

    def decodeToken(self, token: str) -> dict[str, Any]:
        """
        Decode a JWT token
        :param token: str
        :return: dict[str, Any]
        """
        return jwt.decode(jwt=token, key=self._secretKey, algorithms=[self._algorithm])  # pyright: ignore[reportUnknownMemberType] — PyJWT stubs omit full overloads