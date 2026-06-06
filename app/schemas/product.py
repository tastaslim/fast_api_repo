from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    sku: str = Field(..., min_length=1, max_length=100)
    stock: int = Field(default=0, ge=0)
    is_active: bool = True

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v: str) -> str:
        return v.strip().upper()


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    """All fields optional for PATCH semantics."""
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    sku: str | None = Field(None, min_length=1, max_length=100)
    stock: int | None = Field(None, ge=0)
    is_active: bool | None = None

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v: str | None) -> str | None:
        return v.strip().upper() if v else v


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
