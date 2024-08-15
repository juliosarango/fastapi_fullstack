from fastapi import APIRouter,  Depends
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.util_seguros import generar_emisiones, obtener_emision
from app.models import PlanRequest
from app.core.config import settings

router = APIRouter()


@router.post(
    "/",
    # dependencies=[Depends(get_current_active_superuser)],
)
def ingresar_plan(data: PlanRequest):    
    return generar_emisiones(data.dict())

@router.get(
    "/{id}",
    # dependencies=[Depends(get_current_active_superuser)],
)
def consultar_plan(id: str):
    return obtener_emision(id)