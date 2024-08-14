from fastapi import APIRouter,  Depends
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.util_seguros import obtener_cotizaciones
from app.models import RequestCotizacion
from app.core.config import settings

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
)
def consultat_cotizaciones(data: RequestCotizacion):    
    return obtener_cotizaciones(data.dict(), settings.API_URL_COTIZACIONES)