from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, product_id: int) -> Product:
        result = await self.db.get(Product, product_id)
        if not result:
            raise NotFoundError("Product", product_id)
        return result

    async def list(self, page: int = 1, page_size: int = 20) -> tuple[list[Product], int]:
        offset = (page - 1) * page_size

        total_result = await self.db.execute(select(func.count(Product.id)))
        total: int = total_result.scalar_one()

        items_result = await self.db.execute(
            select(Product).order_by(Product.id).offset(offset).limit(page_size)
        )
        items = list(items_result.scalars().all())
        return items, total

    async def create(self, payload: ProductCreate) -> Product:
        # Enforce SKU uniqueness at service layer (DB constraint is the safety net)
        existing = await self.db.execute(select(Product).where(Product.sku == payload.sku))
        if existing.scalar_one_or_none():
            raise ConflictError(f"SKU '{payload.sku}' already exists")

        product = Product(**payload.model_dump())
        self.db.add(product)
        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def update(self, product_id: int, payload: ProductUpdate) -> Product:
        product = await self.get(product_id)

        if payload.sku and payload.sku != product.sku:
            existing = await self.db.execute(select(Product).where(Product.sku == payload.sku))
            if existing.scalar_one_or_none():
                raise ConflictError(f"SKU '{payload.sku}' already exists")

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def delete(self, product_id: int) -> None:
        product = await self.get(product_id)
        await self.db.delete(product)
        await self.db.flush()
