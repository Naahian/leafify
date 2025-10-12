from fastapi import APIRouter


from . import auth_route

router = APIRouter()
router.include_router(auth_route.router, prefix="/auth", tags=["auth"])
