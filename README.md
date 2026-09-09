# EduMatch AI - Smart Education Recommendation System

An intelligent, explainable recommendation system that matches students with the most suitable educational resources based on subject interests, learning goals, and proficiency levels.

---

## 📁 Repository Structure

```
smart-education/
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── StudentForm.jsx           # Student profile input form
│       │   ├── ResourceCard.jsx          # Resource card with match score & tags
│       │   └── RecommendationList.jsx    # Ranked recommendations list
│       └── App.jsx
├── backend/
│   ├── main.py                           # FastAPI application entrypoint with CORS
│   ├── routes/
│   │   └── recommendation.py             # REST API endpoints for recommendations
│   └── database/
│       └── resources.json                # Curated catalog of educational resources
├── engine/
│   ├── scoring.py                        # Multi-factor relevance scoring algorithm
│   ├── recommender.py                    # Pipeline orchestration, filtering & ranking
│   └── explanation.py                    # Explainable AI (XAI) reason generator
├── requirements.txt                      # Python dependencies
└── README.md
```

---

## ⚡ Architecture & Flow

```
[ Frontend (React UI) ]
         │
         ▼  HTTP POST /api/recommendations (StudentProfile JSON)
[ Backend (FastAPI - backend/main.py) ]
         │
         ▼  recommend_resources(student)
[ Engine (engine/recommender.py) ]
   ├── Loads candidate items from backend/database/resources.json
   ├── Computes match metrics via engine/scoring.py
   ├── Generates explainable rationale via engine/explanation.py
   └── Returns ranked results to Backend -> Frontend
```

---

## 🚀 Quick Start (Backend)

### 1. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Run the Backend Server

```bash
uvicorn backend.main:app --reload --port 8000
```
Or directly:
```bash
python -m backend.main
```

The API will start at:
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Alternative ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 📡 API Endpoints

### 1. Get Personalized Recommendations
- **Method**: `POST`
- **Path**: `/api/recommendations`
- **Request Body**:
  ```json
  {
    "name": "Alex",
    "subject": "Python",
    "level": "Beginner",
    "goal": "Exam Preparation",
    "top_n": 4
  }
  ```
- **Response Sample**:
  ```json
  {
    "success": true,
    "data": {
      "student": {
        "name": "Alex",
        "subject": "Python",
        "level": "Beginner",
        "goal": "Exam Preparation"
      },
      "total_candidates": 17,
      "matched_count": 4,
      "returned_count": 4,
      "recommendations": [
        {
          "id": "res-py-002",
          "title": "Python Crash Course: Hands-on Interactive Practice",
          "subject": "Python",
          "level": "Beginner",
          "type": "Interactive Practice",
          "score": 99.7,
          "explanation": {
            "summary": "Hi Alex, this interactive practice is a 99.7% match...",
            "reasons": [
              "Directly covers your target subject 'Python'.",
              "Calibrated specifically for Beginner proficiency.",
              "Optimized for your objective: 'Exam Preparation'."
            ],
            "badges": ["Subject Match: Python", "Level: Beginner", "Goal: Exam Preparation", "Top Rated: 4.9★"],
            "match_percentage": "99%"
          }
        }
      ]
    }
  }
  ```

### 2. Get All Resources (with filtering)
- **Method**: `GET`
- **Path**: `/api/resources?subject=Python&level=Beginner`

### 3. Get Metadata (Dropdown values)
- **Method**: `GET`
- **Path**: `/api/meta`
  Returns all distinct subjects, levels, goals, and resource types for frontend select controls.
