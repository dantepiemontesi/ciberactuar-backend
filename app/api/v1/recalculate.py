"""
CiberActuar — Recalculate API Endpoint
POST /api/v1/recalculate — Recalculates risk after fixing vulnerabilities
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging

from app.models.actuarial import CyberActuarialModel, calculate_cyber_score
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)
actuarial_model = CyberActuarialModel(
    simulations=settings.MONTE_CARLO_SIMULATIONS,
    coverage_amount=settings.DEFAULT_COVERAGE_AMOUNT,
    loss_ratio=settings.LOSS_RATIO,
)


class RecalculateRequest(BaseModel):
    domain: str
    fixed_vulnerabilities: List[str]
    original_score: int = 50


class RecalculateResponse(BaseModel):
    newScore: int
    newPremium: float
    newExpectedLoss: float
    improvement: int


@router.post("/recalculate", response_model=RecalculateResponse)
async def recalculate_risk(request: RecalculateRequest):
    """
    Recalculate risk score and premium after fixing vulnerabilities.
    """
    logger.info(f"Recalculating risk for {request.domain}, fixed: {request.fixed_vulnerabilities}")
    
    try:
        # Score improvement per fixed vulnerability type
        score_improvements = {
            "rdp-open": 20,
            "no-dmarc": 10,
            "ssl-expiring": 8,
            "no-2fa": 5,
            "weak-headers": 3,
        }
        
        total_improvement = sum(
            score_improvements.get(vuln_id, 5) 
            for vuln_id in request.fixed_vulnerabilities
        )
        
        new_score = min(100, request.original_score + total_improvement)
        
        # Run new actuarial calculation
        result = actuarial_model.run_monte_carlo(new_score, sector="general")
        
        return RecalculateResponse(
            newScore=new_score,
            newPremium=result.recommended_premium,
            newExpectedLoss=result.expected_annual_loss,
            improvement=total_improvement,
        )
    except Exception as e:
        logger.error(f"Recalculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
