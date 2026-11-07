import math
from typing import Sequence
from app.shared.constants import MINIMUM_PRICE_OBSERVATIONS

class Scoring:
    @staticmethod
    def normalize_score(s: float, min:float, max: float) -> float:
        if max == min:
            return 0.0
        normalized = (s - min) / (max - min)
        return max(0.0, min(1.0, normalized))

    @staticmethod
    def calc_percent_change(now: float, prev: float) -> float:
        if prev <= 0:
            return 0.0
        return ((prev - now) / prev) * 100

    @staticmethod
    def history(history: Sequence[float], now: float) -> float:
        if not history:
            return 0.0
        avg = sum(history) / len(history)
        return Scoring.calc_percent_change(now, avg)

    @staticmethod
    def calc_weight_score(weights: Sequence[float], ss: Sequence[float]) -> float:
        if len(weights) != len(ss):
            raise ValueError("weights and scores must have the same length")
        w = sum(weights)
        if w <= 0:
            return 0.0
        wsum = sum(w * s for w, s in zip(weights, ss))
        return wsum / w

    @staticmethod
    def calc_bughet_utilization(budget: float, now_spend: float) -> float:
        if budget <= 0:
            return 1.0 if now_spend > 0 else 0.0
        return max(0.0, now_spend / budget)

    @staticmethod
    def calc_confidence(history: Sequence[float], min_obs: int = MINIMUM_PRICE_OBSERVATIONS) -> float:
        if not history or len(history) < min_obs:
            return 0.0
        
        count = len(history)
        sample_factor = min(1.0, count / max(1, min_obs))
        avg = sum(history) / count
        if avg <= 0:
            return 0.0
        
        std_dev = math.sqrt(sum((x - avg) ** 2 for x in history) / count)
        coefficient_of_variation = std_dev / avg if avg != 0 else 0.0
        stability_factor = max(0.0, 1.0 - coefficient_of_variation)
        
        return max(0.0, min(1.0, sample_factor * stability_factor))

    @staticmethod
    def availability_score(available: Sequence[bool]) -> float:
        if not available:
            return 0.0
        available_count = sum(1 for available in available if available)
        return available_count / len(available)