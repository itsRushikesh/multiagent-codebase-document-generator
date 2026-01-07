from backend_MACDG.storage.db_manager import Project,SessionLocal

def save_project_config(project_id, user_id, repo_path, personas, repo_url, db=None):
    """Save or update project configuration in the DB."""
    personas_str = ",".join(personas) if isinstance(personas, list) else personas

    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    try:
        # Upsert: delete if exists (by id) and insert new
        existing = db.query(Project).filter(Project.id == project_id).first()
        if existing:
            db.delete(existing)
            db.commit()
        new_project = Project(
            id=project_id,
            user_id=user_id,
            repo_path=repo_path,
            repo_url=repo_url,
            personas=personas_str
        )
        db.add(new_project)
        db.commit()
    finally:
        if close_db:
            db.close()
