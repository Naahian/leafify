from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.models.user_model import User
from database import get_db
from app.schemas.auth_schema import UserCreate, UserUpdate, UserResponse, Token
from app.crud.user_crud import *
from app.services import ALGORITHM, SECRET_KEY, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials, user_id none",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValueError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials,{e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials,  user is none.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = create_user(db=db, user=user)
    return new_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username)

    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Prevent updating email to an existing one
    if user_update.email and user_update.email != current_user.email:
        existing_user = get_user_by_email(db, email=user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
            )

    updated_user = update_user(db=db, user_id=current_user.id, user=user_update)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    deleted_user = delete_user(db=db, user_id=current_user.id)

    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return None
