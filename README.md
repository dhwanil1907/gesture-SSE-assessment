# Decision Engine Prototype

## Overview

I made a lightweight FastAPI-based decision engine that classifies a business description into a vertical and recommends a marketing campaign.

It accepts structured input and returns:

* Predicted vertical
* Recommended campaign
* Confidence score
* Clear reasoning
* Follow-up questions

The focus is on simplicity, clarity, and explainability.

---

## Why This Approach

I chose a **rule-based system** for this prototype because it:

* Is deterministic and easy to debug
* Provides transparent reasoning
* Avoids unnecessary ML complexity
* Is simple to extend

FastAPI was selected for its:

* Built-in validation (Pydantic)
* Automatic API documentation
* Clean and production-ready structure

This keeps the system lightweight while still architecturally sound.

---

## How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
python -m uvicorn app:app --reload --port 8001
```

Open in browser:

```
http://127.0.0.1:8001/docs
```

---

## Example Request

```json
{
  "text": "We launched a subscription platform with an API and a free trial",
  "context": {
    "goal": "acquisition",
    "geo": "US"
  }
}
```

---

## What Comes Next

If extended beyond prototype stage:

* Replace keyword rules with embeddings or ML classification
* Add more verticals and contextual weighting
* Store decisions in a database
* Add authentication and rate limiting
* Add automated tests and containerization

---

## Summary

This prototype demonstrates:

* Clean API design
* Explainable decision logic
* Structured, extensible architecture

It is intentionally simple, but designed to scale into a more intelligent decision system.
