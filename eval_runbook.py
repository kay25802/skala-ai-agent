
from agent.runbook_rag import search_runbook

# 기존 graph.py의 키워드 규칙과 동일
RULES = [
    ("latency", "high-latency"),
    ("pool", "high-latency"),
    ("cpu", "cpu-spike"),
    ("memory", "memory-leak"),
    ("heap", "memory-leak"),
    ("timeout", "network-timeout"),
    ("network", "network-timeout"),
    ("disk", "disk-full"),
    ("down", "db-down"),
]


def old_search(text):
    text = text.lower()
    for keyword, incident_type in RULES:
        if keyword in text:
            return incident_type
    return "db-down"


# 정답이 지정된 테스트 데이터
# 복합 증상은 핵심 장애를 정답으로 가정
test_cases = [
    ("CPU utilization is 98%", "cpu-spike"),
    ("Memory usage continuously increasing", "memory-leak"),
    ("Network connection timeout", "network-timeout"),
    ("Disk space nearly full", "disk-full"),
    ("Database is down", "db-down"),
    ("Request latency is very high", "high-latency"),
    ("CPU 99%, latency increased", "cpu-spike"),
    ("Server response is extremely slow", "high-latency"),
    ("Out of memory error", "memory-leak"),
    ("Storage capacity exhausted", "disk-full"),
]


def evaluate(search_fn):
    correct = 0

    for query, expected in test_cases:
        predicted = search_fn(query)
        is_correct = predicted == expected
        correct += is_correct

        print(
            f"[{'O' if is_correct else 'X'}] "
            f"{query} -> {predicted} "
            f"(정답: {expected})"
        )

    return correct / len(test_cases)


print("=== Before: 키워드 검색 ===")
before = evaluate(old_search)

print("\n=== After: RAG 검색 ===")
after = evaluate(search_runbook)

print("\n=== 최종 비교 ===")
print(f"Before 정확도: {before:.1%}")
print(f"After 정확도:  {after:.1%}")
print(f"정확도 변화:   {(after-before)*100:+.1f}%p")
