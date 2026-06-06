from fastapi import APIRouter, Depends, Query, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.auth import TokenData
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.services.product import ProductService

settings = get_settings()
limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/products", tags=["products"])


def _svc(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get("/", response_model=ProductListResponse, summary="List products")
@limiter.limit(settings.RATE_LIMIT)
async def list_products(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    svc: ProductService = Depends(_svc),
    _: TokenData = Depends(get_current_user),
) -> ProductListResponse:
    items, total = await svc.list(page=page, page_size=page_size)
    return ProductListResponse(items=items, total=total, page=page, page_size=page_size)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, summary="Create product")
@limiter.limit(settings.RATE_LIMIT)
async def create_product(
    request: Request,
    payload: ProductCreate,
    svc: ProductService = Depends(_svc),
    _: TokenData = Depends(get_current_user),
) -> ProductResponse:
    return await svc.create(payload)


@router.get("/{product_id}", response_model=ProductResponse, summary="Get product")
@limiter.limit(settings.RATE_LIMIT)
async def get_product(
    request: Request,
    product_id: int,
    svc: ProductService = Depends(_svc),
    _: TokenData = Depends(get_current_user),
) -> ProductResponse:
    return await svc.get(product_id)


@router.patch("/{product_id}", response_model=ProductResponse, summary="Update product (partial)")
@limiter.limit(settings.RATE_LIMIT)
async def update_product(
    request: Request,
    product_id: int,
    payload: ProductUpdate,
    svc: ProductService = Depends(_svc),
    _: TokenData = Depends(get_current_user),
) -> ProductResponse:
    return await svc.update(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete product")
@limiter.limit(settings.RATE_LIMIT)
async def delete_product(
    request: Request,
    product_id: int,
    svc: ProductService = Depends(_svc),
    _: TokenData = Depends(get_current_user),
) -> None:
    await svc.delete(product_id)
