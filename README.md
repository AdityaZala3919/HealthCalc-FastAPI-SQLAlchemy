# Health Metrics Calculator

A professional health metrics tracking application with a calculator.net-style frontend and FastAPI backend.

## Features

- **BMI Calculator** - Calculate Body Mass Index and category
- **Body Fat Calculator** - US Navy Method body fat percentage
- **Calorie Calculator** - Daily calorie needs based on activity level
- **BMR Calculator** - Basal Metabolic Rate calculation
- **Ideal Weight Calculator** - Healthy weight range estimation

## Quick Start

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 2. Start the Backend

From the `HealthMetricsTracking` folder:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 3. Open the Frontend

Simply open `frontend/index.html` in your browser, or use a local server:

```bash
cd frontend
python -m http.server 8080
```

Then visit `http://localhost:8080` in your browser.

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /calc/bmi` - Calculate BMI
- `POST /calc/body-fat` - Calculate body fat percentage
- `POST /calc/calorie` - Calculate daily calorie needs
- `POST /calc/bmr` - Calculate Basal Metabolic Rate
- `POST /calc/ideal-weight` - Calculate ideal weight range

## Project Structure

```
HealthMetricsTracking/
├── main.py              # FastAPI application & endpoints
├── calculators.py       # Health calculation functions
├── database.py          # Database configuration (placeholder)
├── models.py            # Data models (placeholder)
├── requirements.txt     # Python dependencies
└── frontend/
    ├── index.html       # Main HTML structure
    ├── styles.css       # Modern gradient styling
    └── main.js          # API integration & interactivity
```

## Notes

- Gender field: `true` = Male, `false` = Female
- All measurements in metric units (kg, cm)
- Frontend features smooth animations and responsive design
- CORS enabled for local development
