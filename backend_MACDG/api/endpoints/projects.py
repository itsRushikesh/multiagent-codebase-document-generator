from fastapi import APIRouter, Depends, HTTPException
from backend_MACDG.api.dependencies import get_current_user
from backend_MACDG.storage.db_manager import get_db_session, Project
from backend_MACDG.api.schemas.project import ProjectInitResponse,ProjectCreateRequest
from backend_MACDG.utils.repo_cloner_utils import clone_github_repo
from backend_MACDG.utils.db_ops_utils import save_project_config

project_router = APIRouter()

@project_router.get("/list-projects", response_model=list)
def list_projects(user=Depends(get_current_user)):
    db = next(get_db_session())
    if user['role'] == 'Admin':
        projects = db.query(Project).all()
    else:
        projects = db.query(Project).filter(Project.user_id == user['id']).all()
    return [p.as_dict() for p in projects]


@project_router.post("/initiate-project", response_model=ProjectInitResponse)
def initiate_project(request: ProjectCreateRequest,user=Depends(get_current_user)):
    try:
        user_id = user['id']
        project_id, repo_path = clone_github_repo(request.repo_url)
        db = next(get_db_session())
        save_project_config(project_id,user_id, repo_path, request.personas, request.repo_url, db=db)
        return ProjectInitResponse(project_id=project_id, personas=request.personas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
