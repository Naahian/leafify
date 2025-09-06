from fastapi import APIRouter

router = APIRouter()

from . import auth, item, user

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(item.router, prefix="/items", tags=["items"])
router.include_router(user.router, prefix="/users", tags=["users"])