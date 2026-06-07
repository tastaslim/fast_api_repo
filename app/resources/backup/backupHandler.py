from app.common.models.apiResponseModel import ApiResponse
from app.resources.backup.backupDtos import BackupCreateDTO, BackupResponseDTO, BackupUpdateDTO, BackupListPageRequest, BackupSearchRequest
from app.resources.backup.backupService import BackupService
from pydantic import ValidationError
from sqlalchemy.orm import Session
import logging
backupService = BackupService()

class BackupHandler:
    async def listBackups(self, search: BackupSearchRequest, databaseCursor: Session) -> ApiResponse[BackupListPageRequest]:
        """
        List backups with optional filters and limit/offset pagination.
        :param search: BackupSearchRequest
        :param databaseCursor: Session database cursor
        :return: BackupListPageRequest
        """
        try:
            backups = await backupService.listBackups(search=search, databaseCursor=databaseCursor)
            return ApiResponse(status=200, message="Backups retrieved successfully", data=backups)
        except ValidationError:
            raise
        except Exception as e:
            logging.error(msg=f"error=Error listing backups: {e}")
            return ApiResponse(status=500, message=f"Internal server error", data=None)

    async def createBackup(self, request: BackupCreateDTO, databaseCursor: Session) -> ApiResponse[BackupResponseDTO]:
        """
        Create a new backup
        :param request: BackupCreateDTO
        :param databaseCursor: Session database cursor
        :return: BackupResponseDTO
        """
        try:
            backup = await backupService.createBackup(backupPayload=request, databaseCursor=databaseCursor)
            return ApiResponse(status=200, message="Backup created successfully", data=backup)
        except ValidationError:
            raise
        except Exception as e:
            logging.error(msg=f"error=Error creating backup: {e}")
            return ApiResponse(status=500, message=f"Internal server error", data=None)
    
    async def getBackup(self, backupId: int, databaseCursor: Session) -> ApiResponse[BackupResponseDTO]:
        """
        Get a backup by ID
        :param backupId: int
        :param databaseCursor: Session database cursor
        :return: BackupResponseDTO
        """
        try:
            backup = await backupService.getBackup(backupId=int(backupId), databaseCursor=databaseCursor)
            if backup is None:
                return ApiResponse(status=404, message="Backup not found", data=None)
            return ApiResponse(status=200, message="Backup retrieved successfully", data=backup)
        except ValidationError:
            raise
        except Exception as e:
            logging.error(msg=f"error=Error getting backup: {e}")
            return ApiResponse(status=500, message=f"Internal server error", data=None)
    
    async def deleteBackup(self, backupId: int, databaseCursor: Session) -> ApiResponse[BackupResponseDTO]:
        """
        Delete a backup by ID
        :param backupId: int
        :param databaseCursor: Session database cursor
        :return: BackupResponseDTO
        """
        try:
            backup = await backupService.deleteBackup(backupId=int(backupId), databaseCursor=databaseCursor)
            if backup is None:
                return ApiResponse(status=404, message="Backup not found", data=None)
            return ApiResponse(status=200, message="Backup deleted successfully", data=None)
        except ValidationError:
            raise
        except Exception as e:
            logging.error(msg=f"error=Error deleting backup: {e}")
            return ApiResponse(status=500, message=f"Internal server error", data=None)
    
    async def updateBackup(self, backupId: int, request: BackupUpdateDTO, databaseCursor: Session) -> ApiResponse[BackupResponseDTO]:
        """
        Update a backup by ID
        :param backupId: int
        :param request: BackupUpdateDTO
        :param databaseCursor: Session database cursor
        :return: BackupResponseDTO
        """
        try:
            backup = await backupService.updateBackup(backupId=int(backupId), request=request, databaseCursor=databaseCursor)
            if backup is None:
                return ApiResponse(status=404, message="Backup not found", data=None)
            
            return ApiResponse(status=200, message="Backup updated successfully", data=backup)
        except Exception as e:
            logging.error(msg=f"error=Error updating backup: {e}")
            return ApiResponse(status=500, message=f"Internal server error", data=None)