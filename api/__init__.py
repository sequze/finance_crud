from fastapi import APIRouter

from .users.views import router as users_router
from .categories.views import router as category_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=category_router, prefix="/categories")