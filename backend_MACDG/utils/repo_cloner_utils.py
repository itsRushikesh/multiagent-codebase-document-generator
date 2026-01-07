import os
from git import Repo
import uuid

def clone_github_repo(repo_url: str, base_dir: str = "cloned_repos"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    project_id = str(uuid.uuid4())
    project_path = os.path.join(base_dir, project_id)
    Repo.clone_from(repo_url, project_path)
    return project_id, project_path
