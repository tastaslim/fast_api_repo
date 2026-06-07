from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class BackupCreateDTO(BaseModel):
    """Request body for creating a backup (server sets id and timestamps)."""
    name: str
    description: str
    encryptionKey: str

class BackupUpdateDTO(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255) 
    isActive: Optional[bool] = Field(default=None)

class BackupResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

class BackupSearchRequest(BaseModel):
    id: Optional[int] = Field(default=None, ge=0)
    name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)
    limit: int = Field(default=500, ge=1, le=5000)
    offset: int = Field(default=0, ge=0)


class BackupListPageRequest(BaseModel):
    items: list[BackupResponseDTO]
    total: int
    limit: int
    offset: int