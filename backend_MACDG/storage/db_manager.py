from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@127.0.0.1:5432/multiagentdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    # projects = relationship("projects", back_populates="users")
    def as_dict(self):
        return {"id": self.id, "email": self.email, "role": self.role}

class Project(Base):
    __tablename__ = 'projects'
    id = Column(String, primary_key=True, index=True)
    user_id = Column(nullable=False)
    repo_path = Column(String, nullable=False)
    repo_url = Column(String, nullable=False)
    personas = Column(String, nullable=False)  
    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "repo_path": self.repo_path,
            "repo_url": self.repo_url,
            "personas": self.personas,
        }
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(engine)
