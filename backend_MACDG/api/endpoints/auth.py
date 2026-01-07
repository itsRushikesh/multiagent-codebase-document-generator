from fastapi import APIRouter, HTTPException, status, Depends
from backend_MACDG.api.schemas.auth import UserSignup, UserLogin, TokenOut
from backend_MACDG.storage.db_manager import get_db_session, User
from backend_MACDG.utils.auth_utils import hash_password, verify_password
from backend_MACDG.utils.jwt_utils import create_access_token
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session


auth_router = APIRouter()

@auth_router.post("/signup", response_model=TokenOut)
def signup(user: UserSignup, db: Session = Depends(get_db_session)):
    exists = db.query(User).filter(User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered.")
        
    new_user = User(
        email=user.email,
        password_hash=user.password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"user_id": new_user.id, "role": new_user.role})
    return {"access_token": token}

@auth_router.post("/login", response_model=TokenOut)
def login(user: UserLogin, db: Session = Depends(get_db_session)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not user.password == db_user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    token = create_access_token({"user_id": db_user.id, "role": db_user.role})
    return {"access_token": token}
