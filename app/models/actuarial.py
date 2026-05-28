"""
CiberActuar — Actuarial Models
Implements Poisson frequency model + Monte Carlo loss simulation
"""
import numpy as np
from scipy import stats
from typing import List, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ActuarialResult:
    expected_annual_loss: float
    recommended_premium: float
    coverage_amount: float
    monte_carlo_data: List[dict]
    confidence_interval_95: Tuple[float, float]
    probability_of_loss: float


class CyberActuarialModel:
    """
    Actuarial model for cybersecurity risk using:
    - Poisson distribution for attack frequency
    - Log-normal distribution for loss severity
    - Monte Carlo simulation for loss scenarios
    """

    def __init__(
        self,
        simulations: int = 10_000,
        coverage_amount: float = 100_000.0,
        loss_ratio: float = 0.60,
    ):
        self.simulations = simulations
        self.coverage_amount = coverage_amount
        self.loss_ratio = loss_ratio

    def calculate_poisson_lambda(self, cyber_score: int, sector: str = "general") -> float:
        """
        Calculate Poisson lambda (expected attacks/year) based on cyber score.
        Lower score = higher frequency.
        """
        # Base lambda by sector
        sector_lambdas = {
            "retail": 0.45,
            "healthcare": 0.55,
            "finance": 0.65,
            "manufacturing": 0.35,
            "general": 0.40,
        }
        base_lambda = sector_lambdas.get(sector, 0.40)

        # Adjust by cyber score (0-100, higher = safer)
        score_factor = 1 + (1 - cyber_score / 100) * 2
        
        return base_lambda * score_factor

    def calculate_loss_parameters(self, cyber_score: int) -> Tuple[float, float]:
        """
        Calculate log-normal distribution parameters for loss severity.
        Returns (mu, sigma) for log-normal distribution.
        """
        # Base loss: companies with lower scores face higher losses
        base_loss = 10_000 + (100 - cyber_score) * 500
        
        # Convert to log-normal parameters
        sigma = 1.2
        mu = np.log(base_loss) - (sigma ** 2) / 2
        
        return mu, sigma

    def run_monte_carlo(self, cyber_score: int, sector: str = "general") -> ActuarialResult:
        """
        Run Monte Carlo simulation to generate loss distribution.
        """
        np.random.seed(42)  # Reproducibility

        lam = self.calculate_poisson_lambda(cyber_score, sector)
        mu, sigma = self.calculate_loss_parameters(cyber_score)

        # Simulate annual losses
        annual_losses = []
        for _ in range(self.simulations):
            # Number of attacks this year (Poisson)
            n_attacks = np.random.poisson(lam)
            
            if n_attacks == 0:
                annual_losses.append(0.0)
            else:
                # Loss per attack (log-normal)
                attack_losses = np.random.lognormal(mu, sigma, n_attacks)
                # Cap losses at coverage amount
                total_loss = min(float(np.sum(attack_losses)), self.coverage_amount)
                annual_losses.append(total_loss)

        annual_losses_array = np.array(annual_losses)

        # Calculate statistics
        expected_loss = float(np.mean(annual_losses_array))
        ci_lower = float(np.percentile(annual_losses_array, 2.5))
        ci_upper = float(np.percentile(annual_losses_array, 97.5))
        prob_loss = float(np.mean(annual_losses_array > 0))

        # Calculate premium
        premium_annual = expected_loss / self.loss_ratio
        premium_monthly = round(premium_annual / 12, 2)

CiberActuar — Actuarial Models
Implements Poisson frequency model + Monte Carlo loss simulation
"""
import numpy as np
from scipy import stats
from typing import List, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ActuarialResult:
    expected_annual_loss: float
    recommended_premium: float
    coverage_amount: float
    monte_carlo_data: List[dict]
    confidence_interval_95: Tuple[float, float]
    probability_of_loss: float


class CyberActuarialModel:
    """
    Actuarial model for cybersecurity risk using:
    - Poisson distribution for attack frequency
    - Log-normal distribution for loss severity
    - Monte Carlo simulation for loss scenarios
    """

    def __init__(self, simulations: int = 10000, coverage_amount: float = 100000.0, loss_ratio: float = 0.60):
        self.simulations = simulations
        self.coverage_amount = coverage_amount
        self.loss_ratio = loss_ratio

    def calculate_poisson_lambda(self, cyber_score: int, sector: str = "general") -> float:
        sector_lambdas = {"retail": 0.45, "healthcare": 0.55, "finance": 0.65, "general": 0.40}
        base_lambda = sector_lambdas.get(sector, 0.40)
        score_factor = 1 + (1 - cyber_score / 100) * 2
        return base_lambda * score_factor

    def calculate_loss_parameters(self, cyber_score: int) -> Tuple[float, float]:
        base_loss = 10000 + (100 - cyber_score) * 500
        sigma = 1.2
        mu = np.log(base_loss) - (sigma ** 2) / 2
        return mu, sigma

    def run_monte_carlo(self, cyber_score: int, sector: str = "general") -> ActuarialResult:
        np.random.seed(42)
        lam = self.calculate_poisson_lambda(cyber_score, sector)
        mu, sigma = self.calculate_loss_parameters(cyber_score)

        annual_losses = []
        for _ in range(self.simulations):
            n_attacks = np.random.poisson(lam)
            if n_attacks == 0:
                annual_losses.append(0.0)
            else:
                attack_losses = np.random.lognormal(mu, sigma, n_attacks)
                total_loss = min(float(np.sum(attack_losses)), self.coverage_amount)
                annual_losses.append(total_loss)

        annual_losses_array = np.array(annual_losses)
        expected_loss = float(np.mean(annual_losses_array))
        ci_lower = float(np.percentile(annual_losses_array, 2.5))
        ci_upper = float(np.percentile(annual_losses_array, 97.5))
        prob_loss = float(np.mean(annual_losses_array > 0))
        premium_monthly = round(expected_loss / self.loss_ratio / 12, 2)

        hist_counts, hist_bins = np.histogram(annual_losses_array, bins=20)
        monte_carlo_data = [
            {"loss": float(hist_bins[i]), "probability": float(hist_counts[i] / len(annual_losses_array))}
            for i in range(len(hist_counts))
        ]

        return ActuarialResult(
            expected_annual_loss=round(expected_loss, 2),
            recommended_premium=max(int(premium_monthly), 10),
            coverage_amount=self.coverage_amount,
            monte_carlo_data=monte_carlo_data,
            confidence_interval_95=(ci_lower, ci_upper),
            probability_of_loss=round(prob_loss, 3),
        )


def calculate_cyber_score(vulnerabilities: list) -> int:
    if not vulnerabilities:
        return 85
    deductions = {"critical": 25, "high": 15, "medium": 7, "low": 3}
    total_deduction = sum(deductions.get(v.get("severity", "low"), 0) for v in vulnerabilities)
    return max(0, min(100, 100 - total_deduction))
