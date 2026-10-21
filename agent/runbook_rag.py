
from pathlib import Path
from functools import lru_cache

from sentence_transformers import SentenceTransformer, util

RUNBOOK_DIR = Path(__file__).resolve().parent.parent / "data" / "runbooks"


@lru_cache(maxsize=1)
def load_runbooks():
    # 한국어와 영어를 지원하는 임베딩 모델
    model = SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    files = sorted(RUNBOOK_DIR.glob("*.md"))
    names = [f.stem for f in files]
    documents = [f.read_text(encoding="utf-8") for f in files]

    # Runbook 내용을 벡터로 변환
    embeddings = model.encode(
        documents, convert_to_tensor=True
    )

    return model, names, embeddings


def search_runbook(text: str) -> str:
    model, names, embeddings = load_runbooks()

    # 사용자 장애 상황을 벡터로 변환
    query_embedding = model.encode(
        text, convert_to_tensor=True
    )

    # 코사인 유사도가 가장 높은 Runbook 선택
    scores = util.cos_sim(query_embedding, embeddings)[0]
    best_index = scores.argmax().item()

    return names[best_index]
