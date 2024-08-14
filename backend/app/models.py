import uuid

from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# API Cotizacion Request

class DetSolicitudes(SQLModel):
    plan: str
    renovacion: int
    tipo: str
    paquete: str
    fechaNacimiento: str
    iniVigReportada: str
    finVigReportada: str = ""
    plazoReportado: int
    tipoVig: int
    sumAseg4: float
    sumAseg5: float
    coberturasPrimaNeta: List[None] = Field(default_factory=list)
    
class Cotizaciones(SQLModel):
    planComercial: str
    detSolicitudes: list[DetSolicitudes]

class RequestCotizacion(SQLModel):
    idConvenio: str = Field(min_length=10)
    sucClave: str = Field(min_length=1, max_length=10)
    sucNombre: str = Field(min_length=1)
    distribuidorClave: str = Field(min_length=1)
    distribuidorNombre: str = Field(min_length=1)
    distribuidorEmail: EmailStr = Field(max_length=255)
    cotizaciones: list[Cotizaciones]

#Plan Request

class AseguradosAdicionales(SQLModel):
    parentesco: str = Field(min_length=2)
    tipoIdentificacion: str = Field(min_length=2)
    numeroIdentificacion: str = Field(min_length=5)
    nombre: str = Field(min_length=5)
    fechaNacimiento: str = Field(min_length=10),
    sexo: str = Field(min_length=1),
    edad: int
       
class certificadosDetalle(SQLModel):
    tipo: str = Field(min_length=1)
    tipoIdentificacion: str = Field(min_length=5)
    numeroIdentificacion: str = Field(min_length=1)
    nombre: str = Field(min_length=5)
    sexo: str = Field(min_length=1)
    etiquetaAdicional1: str = Field(min_length=5)
    datoAdicional1: str = Field(min_length=5)
    etiquetaAdicional2: str = Field(min_length=5)
    datoAdicional2: str = Field(min_length=5)
    etiquetaAdicional3: str = Field(min_length=5)
    datoAdicional3: str = Field(min_length=5)
    objetoAsegurado: str = Field(min_length=5)
    fechaCompra: str = Field(min_length=10)
    marca: str = Field(min_length=2)
    modelo: str = Field(min_length=2)
    aseguradosAdicionales: Optional[list[AseguradosAdicionales]]

    
class Certificados(SQLModel):
    idTrackCotizacion: str = Field(min_length=10)
    filialRfc: str = Field(min_length=5)
    contratanteNombre: str = Field(min_length=10)
    contratanteRfc: str = Field(min_length=10)
    contratanteRegimenFiscal: str = Field(min_length=1)
    contratanteUsoCfdi: str = Field(min_length=2)
    contratanteCodigoPostal: str = Field(min_length=4)
    referenciaDePago: str = Field(min_length=10)
    transaccionDePago: str = Field(min_length=10)
    contratanteCurp: str = Field(min_length=10)
    contratanteEmail: EmailStr = Field(max_length=255)
    contratanteCelular: str = Field(min_length=5)
    contratanteDomicilio: str = Field(min_length=10)
    certificadosDetalle: list[certificadosDetalle]
    

class PlanRequest(SQLModel):
   idConvenio: str = Field(min_length=10)
   sucClave: str = Field(min_length=3)
   sucNombre: str = Field(min_length=5)
   distribuidorClave: str = Field(min_length=3)
   distribuidorNombre: str = Field(min_length=2)
   distribuidorEmail: EmailStr = Field(max_length=255)
   certificados: list[Certificados]