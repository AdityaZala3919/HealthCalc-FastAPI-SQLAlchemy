from fastapi import FastAPI, HTTPException, Depends, Query
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from database import get_db, engine, Base
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import pathlib

import models
import crud
from calculators import (calculate_bmi,
                        calculate_bmr,
                        calculate_body_fat,
                        calculate_calories, 
                        calculate_ideal_weight)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # No shutdown actions required

app = FastAPI(title="HealthMetricsTracking", lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files at /static
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
@app.get("/", include_in_schema=False)
def serve_spa_index():
    index_path = pathlib.Path("frontend") / "index.html"
    return FileResponse(index_path)

# Request Models
class BMIRequest(BaseModel):
    username: Optional[str] = Field(None, description= "Username to save in record")
    age_years: int = Field(..., description= "Age in years")
    gender: bool = Field(..., description= "True = 'M' False 'F'")
    weight_kg: float = Field(..., description= "Weight in kg")
    height_cm: float = Field(..., description= "Height in cm")

class BodyFatRequest(BaseModel):
    username: Optional[str] = Field(None, description= "Username to save in record")
    age_years: int = Field(..., description= "Age in years")
    gender: bool = Field(..., description= "True = 'M' False 'F'")
    weight_kg: float = Field(..., description= "Weight in kg")
    height_cm: float = Field(..., description= "Height in cm")
    neck_cm: float = Field(..., description= "Neck measurement in cm")
    waist_cm: float = Field(..., description= "Waist measurement in cm")
    hip_cm: float = Field(..., description= "Hip measurement in cm")

class CalorieRequest(BaseModel):
    username: Optional[str] = Field(None, description= "Username to save in record")
    age_years: int = Field(..., description= "Age in years")
    gender: bool = Field(..., description= "True = 'M' False 'F'")
    weight_kg: float = Field(..., description= "Weight in kg")
    height_cm: float = Field(..., description= "Height in cm")
    activity_factor: str = Field(..., description= "Select one from: Sedentary, Lightly Active, Moderately Active, Very Active, Extra Active")

class BMRRequest(BaseModel):
    username: Optional[str] = Field(None, description= "Username to save in record")
    age_years: int = Field(..., description= "Age in years")
    gender: bool = Field(..., description= "True = 'M' False 'F'")
    weight_kg: float = Field(..., description= "Weight in kg")
    height_cm: float = Field(..., description= "Height in cm")

class IdealWeightRequest(BaseModel):
    username: Optional[str] = Field(None, description= "Username to save in record")
    age_years: int = Field(..., description= "Age in years")
    gender: bool = Field(..., description= "True = 'M' False 'F'")
    height_cm: float = Field(..., description= "Height in cm")

class HistoryUpdateRequest(BaseModel):
    username: str = Field(..., description="Username who owns this record")
    inputs: Optional[dict] = Field(None, description="New inputs JSON (optional)")
    result: Optional[dict] = Field(None, description="New result JSON (optional)")

# Response Models
class BMIResponse(BaseModel):
    bmi_value: float
    bmi_category: str

class BodyFatResponse(BaseModel):
    body_fat_percentage: float

class CalorieResponse(BaseModel):
    daily_calories: int

class BMRResponse(BaseModel):
    bmr_value: int

class IdealWeightResponse(BaseModel):
    min_weight_kg: float
    max_weight_kg: float

@app.get("")
def working():
    return{"Yes": "API is working"}

@app.get("/health")
def test():
    return {"Ok": "Phase-1 Working"}

def _maybe_save_record(
        db: Session,
        username: Optional[str],
        calc_type: str,
        inputs: dict,
        result: dict
):
    """
    If username provided, get_or_create user and save a CalculationRecord.
    If username is None, still create record with user_id=None (optional).
    """
    user_id = None
    if username:
        user = crud.get_or_create_user(db, username)
        user_id = user.id
    
    crud.create_calc_record(db=db, user_id=user_id, calc_type=calc_type, inputs=inputs, result=result)

def record_to_dict(r: models.CalculationRecord) -> dict:
    return {
        "id": r.id,
        "calc_type": r.calc_type,
        "inputs": r.inputs,
        "result": r.result,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }

@app.post("/calc/bmi", response_model=BMIResponse)
async def bmi_endpoint(bmi: BMIRequest, db: Session = Depends(get_db)):
    result = calculate_bmi(
        age_years=bmi.age_years,
        gender=bmi.gender,
        weight_kg=bmi.weight_kg,
        height_cm=bmi.height_cm
    )

    inputs = bmi.model_dump()
    username = inputs.pop("username", None)

    _maybe_save_record(db, username, "bmi", inputs, result)
    return result

@app.post("/calc/body-fat", response_model=BodyFatResponse)
async def body_fat_endpoint(body_fat: BodyFatRequest, db: Session = Depends(get_db)):
    result = calculate_body_fat(
        age_years=body_fat.age_years,
        gender=body_fat.gender,
        weight_kg=body_fat.weight_kg,
        height_cm=body_fat.height_cm,
        neck_cm=body_fat.neck_cm,
        waist_cm=body_fat.waist_cm,
        hip_cm=body_fat.hip_cm
    )
    inputs = body_fat.model_dump()
    username = inputs.pop("username", None)

    _maybe_save_record(db, username, "body-fat", inputs, result)
    return result

@app.post("/calc/calorie", response_model=CalorieResponse)
async def calorie_endpoint(calorie: CalorieRequest, db: Session = Depends(get_db)):
    result = calculate_calories(
        age_years=calorie.age_years,
        gender=calorie.gender,
        weight_kg=calorie.weight_kg,
        height_cm=calorie.height_cm,
        activity_factor=calorie.activity_factor
    )
    inputs = calorie.model_dump()
    username = inputs.pop("username", None)

    _maybe_save_record(db, username, "calorie", inputs, result)
    return result

@app.post("/calc/bmr", response_model=BMRResponse)
async def bmr_endpoint(bmr: BMRRequest, db: Session = Depends(get_db)):
    result = calculate_bmr(
        age_years=bmr.age_years,
        gender=bmr.gender,
        weight_kg=bmr.weight_kg,
        height_cm=bmr.height_cm
    )
    inputs = bmr.model_dump()
    username = inputs.pop("username", None)

    _maybe_save_record(db, username, "bmr", inputs, result)
    return result

@app.post("/calc/ideal-weight", response_model=IdealWeightResponse)
async def ideal_weight_endpoint(ideal_weight: IdealWeightRequest, db: Session = Depends(get_db)):
    result = calculate_ideal_weight(
        age_years=ideal_weight.age_years,
        gender=ideal_weight.gender,
        height_cm=ideal_weight.height_cm
    )
    inputs = ideal_weight.model_dump()
    username = inputs.pop("username", None)

    _maybe_save_record(db, username, "ideal-weight", inputs, result)
    return result

@app.get("/calc/history")
def list_history(
    username: Optional[str] = Query(None, description="username to list history for"),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0
):
    if not username:
        return []
    
    user = crud.get_user_by_username(db, username)
    if not user:
        return []
    
    records = crud.list_calc_records_by_user(db=db, user_id=user.id, limit=limit, offset=offset)

    def to_dict(r: models.CalculationRecord):
        return {
            "id": r.id,
            "calc_type": r.calc_type,
            "inputs": r.inputs,
            "result": r.result,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
    
    return [to_dict(r) for r in records]

@app.get("/calc/history/{record_id}")
def get_history_record(
    record_id: int,
    username: str = Query(..., description="Username who owns this record"),
    db: Session = Depends(get_db),
):
    """
    Get a single calculation record by id for a given username.
    """
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    record = crud.get_calc_record(db, record_id)
    if not record or record.user_id != user.id:
        # Either record does not exist or does not belong to this user
        raise HTTPException(status_code=404, detail="Record not found")

    return record_to_dict(record)

@app.patch("/calc/history/{record_id}")
def update_history_record(
    record_id: int,
    payload: HistoryUpdateRequest,
    db: Session = Depends(get_db),
):
    """
    Update a calculation record's inputs and/or result for the given username.
    """
    user = crud.get_user_by_username(db, payload.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = crud.update_calc_record(
        db=db,
        record_id=record_id,
        inputs=payload.inputs,
        result=payload.result,
        user_id=user.id,
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Record not found or not owned by user")

    return record_to_dict(updated)

@app.delete("/calc/history/{record_id}")
def delete_history_record(
    record_id: int,
    username: str = Query(..., description="Username who owns this record"),
    db: Session = Depends(get_db),
):
    """
    Delete a calculation record for a given username.
    """
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = crud.delete_calc_record(
        db=db,
        record_id=record_id,
        user_id=user.id,
    )

    if not success:
        raise HTTPException(status_code=404, detail="Record not found or not owned by user")

    return {"detail": "Record deleted successfully"}

"""
I need a modern, responsive web UI for a Health Metrics Calculator app. It should have a clean, professional look (like calculator.net) and support the following calculators as tabs or sections:

BMI Calculator (inputs: age, gender, weight, height)
Body Fat Calculator (inputs: age, gender, weight, height, neck, waist, hip)
Calorie Calculator (inputs: age, gender, weight, height, activity level)
BMR Calculator (inputs: age, gender, weight, height)
Ideal Weight Calculator (inputs: age, gender, height)
Each calculator should have its own form, a submit button, and a result display area. Use clear labels, good spacing, and visually appealing buttons. The design should work well on desktop and mobile.

Please generate the HTML, CSS, and any necessary JavaScript for the UI only (no backend logic). Use unique IDs for forms and result boxes so I can connect them to my backend later.
"""

"""
To run the code:

1. "python -m http.server 8080 --directory frontend"

2. "uvicorn main:app --reload"

3. Open "http://localhost:8080"
"""