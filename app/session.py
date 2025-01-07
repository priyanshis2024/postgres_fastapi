# app/session.py
from sqlalchemy.orm import Session
from app import models
from datetime import datetime
from fastapi import HTTPException


def logout(user_id: int, db: Session):
    # Find the active session of the user
    session_to_delete = db.query(models.ActiveSession).filter(models.ActiveSession.user_id == user_id).first()
    
    if session_to_delete:
        # If session exists, delete it from the database
        db.delete(session_to_delete)
        db.commit()
    else:
        # If no session found, handle it (either log or raise an error)
        raise HTTPException(status_code=404, detail="No active session found for user")


# Get all active users (users with valid sessions)
def get_all_logged_in_users(db: Session):
    # Fetch all sessions that are not expired
    active_sessions = db.query(models.ActiveSession).filter(models.ActiveSession.expires_at > datetime.utcnow()).all()
    active_users = [session.user_id for session in active_sessions]
    return active_users
