from app.resources.cset.csetRoute import csetRoute
from app.resources.backup.backupRoute import backupRoute
from app.resources.user.userRoute import userRoute
routers = [
    csetRoute,
    backupRoute,
    userRoute
]