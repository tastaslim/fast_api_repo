from typing import List
from app.resources.cset.csetModel import CSetModel


class CSetService:
    _cSets : List[CSetModel] = []
    async def listCsets(self) -> list[CSetModel]:
        return self._cSets

    async def createCset(self, csetPayload: CSetModel) -> CSetModel:
        self._cSets.append(csetPayload)
        return csetPayload
