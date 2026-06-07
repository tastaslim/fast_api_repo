from typing import Optional
from app.resources.backup.backupDtos import BackupCreateDTO, BackupResponseDTO, BackupUpdateDTO,  BackupListPageRequest, BackupSearchRequest
from sqlalchemy.orm import Session
from app.resources.backup.backupRespository import BackupRepository

class BackupService:
    def __init__(self):
        self.backupRepository = BackupRepository()
        
    async def listBackups(self, search: BackupSearchRequest, databaseCursor: Session) -> BackupListPageRequest:
        """
        List backups with optional filters and limit/offset pagination.
        :param search: BackupSearchRequest
        :param databaseCursor: Session database cursor
        :return: BackupListPageRequest
        """
        backups = self.backupRepository.listBackups(databaseCursor=databaseCursor, search=search)
        total = len(backups)
        return BackupListPageRequest(
            items=[BackupResponseDTO.model_validate(row) for row in backups],
            total=total,
            limit=search.limit,
            offset=search.offset,
        )

    async def createBackup(self, backupPayload: BackupCreateDTO, databaseCursor: Session) -> BackupResponseDTO:
        """
        Create a new backup
        :param backupPayload: BackupCreateDTO
        :param databaseCursor: Session database cursor
        :return: BackupResponseDTO
        """
        newBackupDefinition = self.backupRepository.createBackup(databaseCursor=databaseCursor, request=backupPayload)
        return BackupResponseDTO.model_validate(newBackupDefinition)

    async def getBackup(self, backupId: int, databaseCursor: Session) -> Optional[BackupResponseDTO]:
        """
        Get a backup by ID
        :param backupId: int
        :return: BackupResponseDTO | None
        """
        row = self.backupRepository.getBackup(databaseCursor=databaseCursor, backupId=backupId)
        return BackupResponseDTO.model_validate(row) if row else None
    
    async def deleteBackup(self, backupId: int, databaseCursor: Session) -> Optional[BackupResponseDTO]:
        """
        Delete a backup by ID
        :param backupId: int
        :param databaseCursor: Session database cursor
        :return: BackupResponseDTO | None
        """
        row = self.backupRepository.deleteBackup(databaseCursor=databaseCursor, backupId=backupId)
        return BackupResponseDTO.model_validate(row) if row else None
    
    async def updateBackup(self, backupId: int, request: BackupUpdateDTO, databaseCursor: Session) -> Optional[BackupResponseDTO]:
        """
        Partial update (PATCH): only fields included in the request body are changed.
        :param backupId: int
        :param request: BackupUpdateDTO
        :param databaseCursor: Session database cursor
        :return: BackupResponseDTO | None
        """
        updates = request.model_dump(exclude_unset=True) # Set only fields that are not None(sent from client)
        backupSchema = self.backupRepository.updateBackup(
            databaseCursor=databaseCursor,
            backupId=backupId,
            updates=updates,
        )
        return BackupResponseDTO.model_validate(backupSchema) if backupSchema else None