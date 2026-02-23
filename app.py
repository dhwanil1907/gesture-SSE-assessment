from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any, Dict, List
import re

app = FastAPI(title="Decision Engine Prototype", version="0.1")

# --- tiny "policy" you can edit easily ---
VERTICAL_KEYWORDS = {
    "ecommerce": ["shop", "store", "cart", "checkout", "sku", "inventory", "product"],
    "saas": ["subscription", "platform", "api", "dashboard", "trial", "workspace", "seat"],
    "fintech": ["loan", "credit", "bank", "wallet", "payments", "investment", "trading"],
    "health": ["clinic", "patient", "appointment", "provider", "medical", "treatment"],
}

DEFAULT_CAMPAIGN = {
    "ecommerce": "Conversion Boost Campaign",
    "saas": "Free Trial Acquisition Campaign",
    "fintech": "Trust & Education Campaign",
    "health": "Appointment Booking Campaign",
}

FOLLOW_UPS = {
    "ecommerce": [
        "What’s your average order value (AOV)?",
        "Are you optimizing for new customers or repeats?",
    ],
    "saas": [
        "What’s your trial-to-paid conversion rate?",
        "Who is the buyer vs the end user?",
    ],
    "fintech": [
        "Any compliance / regulatory constraints on messaging?",
        "What’s the biggest trust barrier today?",
    ],
    "health": [
        "New patients or follow-ups?",
        "Do you accept insurance?",
    ],
}


class DecideRequest(BaseModel):
    text: str
    context: Dict[str, Any] = Field(default_factory=dict)


class DecideResponse(BaseModel):
    vertical: str
    recommended_campaign: str
    confidence_score: float
    reasoning: List[str]
    next_questions_to_ask: List[str]


def _norm(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


def _count_hits(text: str, keywords: List[str]) -> int:
    hits = 0
    for kw in keywords:
        if re.search(rf"\b{re.escape(kw)}\b", text):
            hits += 1
    return hits


def decide(text: str, context: Dict[str, Any]) -> Dict[str, Any]:
    reasoning: List[str] = []
    t = _norm(text)
    reasoning.append("Normalized input text.")

    # 1) score each vertical by keyword hits
    scores: Dict[str, int] = {}
    for vertical, kws in VERTICAL_KEYWORDS.items():
        c = _count_hits(t, kws)
        scores[vertical] = c
        if c:
            reasoning.append(f"Matched {c} keyword(s) for '{vertical}'.")

    # 2) optional light context hint (soft nudge, not a hard override)
    hint = str(context.get("vertical_hint") or context.get("industry") or "").lower().strip()
    if hint in scores:
        scores[hint] += 1
        reasoning.append(f"Used context hint '{hint}' as a small boost (+1).")

    # 3) pick winner (fallback if nothing matched)
    winner = max(scores, key=scores.get)
    win_score = scores[winner]
    if win_score == 0:
        winner = "saas"
        win_score = 0
        reasoning.append("No keyword matches found; defaulted to 'saas'.")

    campaign = DEFAULT_CAMPAIGN.get(winner, "Generic Awareness Campaign")

    # 4) simple confidence (explainable + predictable)
    if win_score <= 0:
        confidence = 0.40
        reasoning.append("Low evidence => confidence set to 0.40.")
    elif win_score == 1:
        confidence = 0.60
        reasoning.append("1 match => confidence set to 0.60.")
    elif win_score == 2:
        confidence = 0.75
        reasoning.append("2 matches => confidence set to 0.75.")
    else:
        confidence = 0.90
        reasoning.append("3+ matches => confidence set to 0.90.")

    questions = list(FOLLOW_UPS.get(winner, []))

    # ask for missing basics
    if "goal" not in context:
        questions.insert(0, "What’s your primary goal (acquisition, activation, retention, revenue)?")
    if "geo" not in context:
        questions.append("Which market/geo are you targeting?")

    return {
        "vertical": winner,
        "recommended_campaign": campaign,
        "confidence_score": confidence,
        "reasoning": reasoning,
        "next_questions_to_ask": questions[:6],
    }


@app.post("/decide", response_model=DecideResponse)
def decide_route(req: DecideRequest):
    return decide(req.text, req.context)