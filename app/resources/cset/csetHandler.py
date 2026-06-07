from app.resources.cset.csetModel import CSetModel
from app.resources.cset.csetService import CSetService
cSetService = CSetService()

class CsetHandler:
    async def listCsets(self) -> list[CSetModel]:
        return await cSetService.listCsets()

    async def createCset(self, request: CSetModel) -> CSetModel:
        return await cSetService.createCset(csetPayload=request)
