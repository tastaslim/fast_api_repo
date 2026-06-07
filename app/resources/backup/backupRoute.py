from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from app.common.utils.apiResponseUtil import toJsonResponse
from app.common.utils.authentication import validateToken
from app.db.database import getDatabase
from app.db.schema.userSchema import UserSchema
from app.resources.backup.backupHandler import BackupHandler
from app.resources.backup.backupDtos import BackupCreateDTO, BackupResponseDTO, BackupUpdateDTO, BackupSearchRequest
from sqlalchemy.orm import Session
backupRoute: APIRouter = APIRouter(prefix="/api/v1/backups", tags=["Backups"])
backupHandler = BackupHandler()


@backupRoute.get(path="/", response_model=List[BackupResponseDTO], status_code=status.HTTP_200_OK)
async def listBackups(filters: Annotated[BackupSearchRequest, Query()], databaseCursor: Session = Depends(getDatabase), user: UserSchema = Depends(validateToken)) -> JSONResponse:
    backups = await backupHandler.listBackups(search=filters, databaseCursor=databaseCursor)
    return toJsonResponse(backups)

@backupRoute.post(path="/", response_model=BackupResponseDTO, status_code=status.HTTP_201_CREATED)
async def createBackup(request: BackupCreateDTO, databaseCursor: Session = Depends(getDatabase), user: UserSchema = Depends(validateToken)) -> JSONResponse:
    backup = await backupHandler.createBackup(request=request, databaseCursor=databaseCursor)
    return toJsonResponse(backup)

@backupRoute.get(path="/{backupId}", response_model=BackupResponseDTO, status_code=status.HTTP_200_OK)
async def getBackup(backupId: int, databaseCursor: Session = Depends(getDatabase), user: UserSchema = Depends(validateToken)) -> JSONResponse:
    backup = await backupHandler.getBackup(backupId=backupId, databaseCursor=databaseCursor)
    return toJsonResponse(backup)

@backupRoute.delete(path="/{backupId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteBackup(backupId: int, databaseCursor: Session = Depends(getDatabase), user: UserSchema = Depends(validateToken)) -> JSONResponse:
    backup = await backupHandler.deleteBackup(backupId=backupId, databaseCursor=databaseCursor)
    return toJsonResponse(backup)

@backupRoute.patch(path="/{backupId}", response_model=BackupResponseDTO, status_code=status.HTTP_201_CREATED)
async def updateBackup(backupId: int, request: BackupUpdateDTO, databaseCursor: Session = Depends(getDatabase), user: UserSchema = Depends(validateToken)) -> JSONResponse:
    backup = await backupHandler.updateBackup(backupId=backupId, request=request, databaseCursor=databaseCursor)
    return toJsonResponse(backup)