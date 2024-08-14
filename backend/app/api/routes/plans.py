from fastapi import APIRouter,  Depends
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.util_seguros import obtener_emisiones
from app.models import PlanRequest
from app.core.config import settings

router = APIRouter()


@router.post(
    "/",
    # dependencies=[Depends(get_current_active_superuser)],
)
def consultar_cotizaciones(data: PlanRequest):    
    return obtener_emisiones(data.dict())