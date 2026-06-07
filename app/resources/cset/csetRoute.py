from fastapi import APIRouter
from app.resources.cset.csetHandler import CsetHandler
from app.resources.cset.csetModel import CSetModel

csetRoute: APIRouter = APIRouter(prefix="/csets", tags=["CSets"])
csetHandler = CsetHandler()

@csetRoute.get(path="/")
async def listCsets() -> list[CSetModel]:
    return await csetHandler.listCsets()


@csetRoute.post(path="/")
async def createCset(request: CSetModel) -> CSetModel:
    return await csetHandler.createCset(request=request)
