from datetime import datetime
from typing import Any, Optional
from app.resources.backup.backupDtos import BackupCreateDTO, BackupSearchRequest
from app.db.schema.backupSchema import BackupSchema
from sqlalchemy.orm import Session

class BackupRepository:
    def listBackups(self, databaseCursor: Session, search: BackupSearchRequest) -> list[BackupSchema]:
        """
        List backups with optional filters and limit/offset pagination.
        :param databaseCursor: Session database cursor
        :param search: BackupSearchRequest
        :return: list[BackupSchema]
        """
        query = databaseCursor.query(BackupSchema)
        if search.id:
            query = query.filter(BackupSchema.id == search.id)

        if search.name:
            query = query.filter(BackupSchema.name.ilike(f"%{search.name}%"))

        if search.description:
            query = query.filter(BackupSchema.description.ilike(f"%{search.description}%"))
        query = query.order_by(BackupSchema.id.asc())
        query = query.offset(search.offset).limit(search.limit)
        return query.all()

    def countBackups(self, databaseCursor: Session, search: BackupSearchRequest) -> int:
        query = databaseCursor.query(BackupSchema)
        if search.id:
            query = query.filter(BackupSchema.id == search.id)
        if search.name:
            query = query.filter(BackupSchema.name.ilike(f"%{search.name}%"))
        if search.description:
            query = query.filter(BackupSchema.description.ilike(f"%{search.description}%"))
        return query.count()

    def getBackup(self, databaseCursor: Session, backupId: int) -> Optional[BackupSchema]:
        return databaseCursor.get(BackupSchema, backupId)
    
    def createBackup(self, databaseCursor: Session, request: BackupCreateDTO) -> BackupSchema:
        backupSchema = BackupSchema(
            name=request.name,
            description=request.description,
            encryptionKey=request.encryptionKey,
            isActive=True,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
        databaseCursor.add(backupSchema)
        databaseCursor.commit()
        databaseCursor.refresh(backupSchema)
        return backupSchema
    
    def deleteBackup(self, databaseCursor: Session, backupId: int) -> Optional[BackupSchema]:
        backupSchema = databaseCursor.get(BackupSchema, backupId)
        if backupSchema is None:
            return None
        databaseCursor.delete(backupSchema)
        databaseCursor.commit()
        return backupSchema
    
    def updateBackup(self, databaseCursor: Session, backupId: int, updates: dict[str, Any]) -> Optional[BackupSchema]:
        """
        Update a backup by ID
        :param databaseCursor: Session database cursor
        :param backupId: int
        :param updates: dict[str, Any]
        :return: Optional[BackupSchema]
        """
        backupSchema = databaseCursor.get(BackupSchema, backupId)
        if not backupSchema or not updates:
            return None
        for key, value in updates.items():
            setattr(backupSchema, key, value)
        
        backupSchema.updatedAt = datetime.now()
        databaseCursor.commit()
        databaseCursor.refresh(backupSchema)
        return backupSchema