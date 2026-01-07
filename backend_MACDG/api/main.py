from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend_MACDG.api.endpoints import auth,projects
from backend_MACDG.storage.db_manager import init_db

app = FastAPI(title="Multi-Agent Code Doc Auth", docs_url="/swagger")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(auth.auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(projects.project_router,prefix="/project",tags=["Initiate Project"])

@app.get("/")
def root():
    return {"status": "Auth API running"}
