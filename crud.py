from typing import Optional, List
from sqlalchemy.orm import Session
import models

# Helper functions for "User" table.
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    # This function returns the user with the given username, or None if not found.
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )

def create_user(db: Session, username: str) -> models.User:
    """
    This function creates a new user with the given username.

    Raises:
        ValueError: if a user with this username already exists.
    """
    existing_user = get_user_by_username(db, username)
    if existing_user:
        raise ValueError(f"User with username '{username}' already exists.")

    db_user = models.User(username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_or_create_user(db: Session, username: str) -> models.User:
    # This function returns existing user if found, otherwise create and return a new one.
    user = get_user_by_username(db, username)
    if user:
        return user
    return create_user(db, username)

# Helper functions for "CalculationRecord" table.
def create_calc_record(
    db: Session,
    user_id: Optional[int],
    calc_type: str,
    inputs: dict,
    result: dict,
) -> models.CalculationRecord:
    """
    This function creates and helps a calculation record persist.

    user_id can be None if you allow anonymous records.
    """
    record = models.CalculationRecord(
        user_id=user_id,
        calc_type=calc_type,
        inputs=inputs,
        result=result,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_calc_record(
    db: Session,
    record_id: int,
) -> Optional[models.CalculationRecord]:
    # This function returns a single calculation record by id, or None if not found.
    return (
        db.query(models.CalculationRecord)
        .filter(models.CalculationRecord.id == record_id)
        .first()
    )

def list_calc_records_by_user(
    db: Session,
    user_id: int,
    calc_type: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[models.CalculationRecord]:
    # This function returns a list of calculation records for a given user, optionally filtered by calc_type, ordered by newest first.
    query = db.query(models.CalculationRecord).filter(
        models.CalculationRecord.user_id == user_id
    )

    if calc_type:
        query = query.filter(models.CalculationRecord.calc_type == calc_type)

    return (
        query.order_by(models.CalculationRecord.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

def delete_calc_record(
    db: Session,
    record_id: int,
    user_id: Optional[int] = None,
) -> bool:
    """
    This function deletes a calculation record.

    If user_id is provided, it ensure the record belongs to that user.

    Returns:
        True if a record was deleted, False if nothing matched.
    """
    query = db.query(models.CalculationRecord).filter(
        models.CalculationRecord.id == record_id
    )

    if user_id is not None:
        query = query.filter(models.CalculationRecord.user_id == user_id)

    record = query.first()
    if not record:
        return False

    db.delete(record)
    db.commit()
    return True

def update_calc_record(
    db: Session,
    record_id: int,
    inputs: Optional[dict] = None,
    result: Optional[dict] = None,
    user_id: Optional[int] = None,
) -> Optional[models.CalculationRecord]:
    """
    This function updates a calculation record's inputs and/or result.

    If user_id is provided, it ensures the record belongs to that user.

    Returns:
        The updated record, or None if not found.
    """
    query = db.query(models.CalculationRecord).filter(
        models.CalculationRecord.id == record_id
    )

    if user_id is not None:
        query = query.filter(models.CalculationRecord.user_id == user_id)

    record = query.first()
    if not record:
        return None

    if inputs is not None:
        record.inputs = inputs
    if result is not None:
        record.result = result

    db.commit()
    db.refresh(record)
    return record
