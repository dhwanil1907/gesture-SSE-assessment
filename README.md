````markdown
# Decision Engine Prototype

A lightweight decision engine built with FastAPI that classifies a business into a vertical and recommends a campaign strategy using simple, explainable rules.

---

## Overview

This project implements a small API that takes:

- A short business description (`text`)
- Optional structured context (e.g. `industry`, `goal`, `geo`)

It returns:

- Predicted vertical (ecommerce, saas, fintech, health)
- Recommended campaign
- Confidence score
- Transparent reasoning for the decision
- Follow-up questions to gather missing information

The system is deterministic and fully explainable. Every output can be traced directly to keyword matches and scoring logic.

---

## Why I Chose This Approach

Out of the three options, I chose to build a decision engine API because it allowed me to demonstrate:

- Structured system design
- Deterministic scoring logic
- Clean API contracts and schemas
- Explainability over black-box behavior
- Extensibility without unnecessary complexity

Rather than building something overly complex, I focused on clarity and system thinking. The goal was to show how I approach designing scalable decision logic that can evolve over time.

---

## How It Works

The engine follows a simple pipeline:

1. Normalize the input text  
2. Count keyword matches for each vertical  
3. Apply a small context-based boost (if provided)  
4. Select the highest scoring vertical  
5. Assign confidence based on match strength  
6. Return a structured response with reasoning  

Confidence is determined by the number of matched signals, making behavior predictable and easy to test.

---

## API Endpoint

### `POST /decide`

**Request Body**
```json
{
  "text": "We want to improve checkout conversion and reduce cart abandonment",
  "context": {}
}
````

**Response**

```json
{
  "vertical": "ecommerce",
  "recommended_campaign": "Conversion Boost Campaign",
  "confidence_score": 0.9,
  "reasoning": [
    "Normalized input text.",
    "Matched 3 keyword(s) for 'ecommerce'.",
    "3+ matches => confidence set to 0.90."
  ],
  "next_questions_to_ask": [
    "What’s your primary goal (acquisition, activation, retention, revenue)?",
    "What’s your average order value (AOV)?",
    "Are you optimizing for new customers or repeats?",
    "Which market/geo are you targeting?"
  ]
}
```

---

## How to Run

From inside the project directory:

```bash
uvicorn app:app --reload --port 8001
```

Then open:

```
http://127.0.0.1:8001/docs
```

Use the Swagger UI to test the endpoint interactively.

---

## Future Improvements

If extended further, I would:

* Introduce weighted scoring (not all keywords equal)
* Improve tie-breaking and ambiguity handling
* Log decisions for evaluation and feedback loops
* Replace keyword matching with embedding-based semantic classification
* Add experimentation support for campaign optimization

---

## Design Philosophy

This prototype prioritizes:

* Clarity
* Explainability
* Determinism
* Clean API structure
* Extensibility