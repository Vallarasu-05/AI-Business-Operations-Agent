def accuracy(correct: int, total: int) -> float:
    return round(correct / total, 3) if total else 0.0


def recall_at_k(retrieved: list[str], relevant: set[str]) -> float:
    return len(set(retrieved) & relevant) / len(relevant) if relevant else 0.0


def precision_at_k(retrieved: list[str], relevant: set[str]) -> float:
    return len(set(retrieved) & relevant) / len(retrieved) if retrieved else 0.0
