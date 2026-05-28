"""
CiberActuar — Scan API Endpoint
POST /api/v1/scan — Scans a domain and returns risk assessment
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, validator
import re
import asyncio
import random
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


class ScanRequest(BaseModel):
    domain: str

    @validator("domain")
    def validate_domain(cls, v):
        v = v.strip().lower()
        v = re.sub(r"^https?://", "", v)
        v = re.sub(r"/.*$", "", v)
        if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", v):
            raise ValueError("Invalid domain format")
        return v


class VulnerabilityResponse(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    port: int | None
    impact: float
    premiumReduction: float
    fixed: bool


class MonteCarloPoint(BaseModel):
    loss: float
    probability: float


class ScanResponse(BaseModel):
    domain: str
    cyberScore: int
    expectedAnnualLoss: float
    recommendedPremium: float
    coverageAmount: float
    vulnerabilities: list[VulnerabilityResponse]
    monteCarloData: list[MonteCarloPoint]
    sectorComparison: int


async def perform_security_scan(domain: str) -> list[dict]:
    """
    Simulate security scanning for the domain.
    In production, this would use nmap, DNS lookups, SSL checks, etc.
    """
    await asyncio.sleep(1.5)  # Simulate scan time
    
    vulnerabilities = []
    
    # Simulate random vulnerability discovery
    potential_vulns = [
        {
            "id": "rdp-open",
            "title": "Puerto RDP 3389 expuesto",
            "description": "El escritorio remoto está abierto al público, permitiendo ataques de fuerza bruta.",
            "severity": "critical",
            "port": 3389,
            "impact": 15000,
            "premiumReduction": 8,
        },
        {
            "id": "no-dmarc",
            "title": "Sin protección DMARC en correo",
            "description": "Tu dominio no tiene DMARC configurado, permitiendo suplantación de identidad por email.",
            "severity": "high",
            "port": None,
            "impact": 8000,
            "premiumReduction": 5,
        },
        {
            "id": "ssl-expiring",
            "title": "Certificado SSL próximo a vencer",
            "description": "El certificado SSL vence en menos de 30 días, dejando las comunicaciones en riesgo.",
            "severity": "high",
            "port": 443,
            "impact": 5000,
            "premiumReduction": 4,
        },
        {
            "id": "no-2fa",
            "title": "Sin autenticación de dos factores",
            "description": "El panel administrativo no requiere 2FA.",
            "severity": "medium",
            "port": None,
            "impact": 3000,
            "premiumReduction": 3,
        },
        {
            "id": "weak-headers",
            "title": "Headers de seguridad HTTP faltantes",
            "description": "Faltan Content-Security-Policy y X-Frame-Options.",
            "severity": "low",
            "port": None,
            "impact": 1000,
            "premiumReduction": 1,
        },
    ]
    
    # Randomly include some vulnerabilities
    for vuln in potential_vulns:
        if random.random() > 0.3:  # 70% chance each vuln is found
            vulnerabilities.append({**vuln, "fixed": False})
    
    return vulnerabilities


@router.post("/scan", response_model=ScanResponse)
async def scan_domain(request: ScanRequest):
    """
    Scan a domain for cybersecurity vulnerabilities and calculate risk score.
    """
    logger.info(f"Starting scan for domain: {request.domain}")
    
    try:
        # Perform security scan
        vulnerabilities = await perform_security_scan(request.domain)
        
        # Calculate cyber score
        cyber_score = calculate_cyber_score(vulnerabilities)
        
        # Run actuarial model
        actuarial_result = actuarial_model.run_monte_carlo(cyber_score, sector="general")
        
        # Calculate sector comparison (mock: random 40-80% more vulnerable)
        sector_comparison = random.randint(40, 80)
        
        return ScanResponse(
            domain=request.domain,
            cyberScore=cyber_score,
            expectedAnnualLoss=actuarial_result.expected_annual_loss,
            recommendedPremium=actuarial_result.recommended_premium,
            coverageAmount=actuarial_result.coverage_amount,
            vulnerabilities=[VulnerabilityResponse(**v) for v in vulnerabilities],
            monteCarloData=[MonteCarloPoint(**p) for p in actuarial_result.monte_carlo_data],
            sectorComparison=sector_comparison,
        )
    except Exception as e:
        logger.error(f"Scan failed for {request.domain}: {e}")
              raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")
