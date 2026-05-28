"""
CiberActuar — Quote API Endpoint
GET /api/v1/quote/{domain} — Returns insurance quote for a domain
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class QuoteResponse(BaseModel):
    domain: str
    premium: float
    coverage: float
    monthly_payment: float
    annual_payment: float
    deductible: float


@router.get("/quote/{domain}", response_model=QuoteResponse)
async def get_quote(domain: str):
    """
    Get the insurance quote for a previously scanned domain.
    """
    logger.info(f"Generating quote for domain: {domain}")
    
    # In production, fetch from Redis cache
    # For now, return calculated quote
    base_premium = 45.0
    coverage = 100_000.0
    
    return QuoteResponse(
        domain=domain,
        premium=base_premium,
        coverage=coverage,
        monthly_payment=base_premium,
        annual_payment=base_premium * 12 * 0.9,  # 10% annual discount
        deductible=coverage * 0.05,  # 5% deductible
    )
