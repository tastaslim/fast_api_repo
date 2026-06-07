from fastapi import FastAPI
from app.common.exceptionHandlers import registerExceptionHandlers
from app.routes.allRoutes import routers
from app.db.database import engine, Base
from app.db.schema import databaseSchemas
for schema in databaseSchemas:
    Base.metadata.create_all(bind=engine, tables=[schema.__table__])

def createApp() -> FastAPI:
    app = FastAPI(title="Fast API Service")
    registerExceptionHandlers(app)
    for router in routers:
        app.include_router(router=router)
    return app

app = createApp()