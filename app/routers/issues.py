from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(tags=["issues"])


@router.post("/", response_model=schemas.IssueRead)
def issue_book(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    try:
        db_issue = crud.create_issue(db, issue)
        return db_issue
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{issue_id}/return", response_model=schemas.IssueRead)
def return_book_endpoint(issue_id: int, db: Session = Depends(get_db)):
    db_issue = crud.return_book(db, issue_id)
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found or already returned")
    return db_issue

@router.get("/{issue_id}", response_model=schemas.IssueRead)
def read_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = crud.get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue
