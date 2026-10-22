import chromadb

_client = None


def get_chroma():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path="./chroma_data")
    return _client


def search_policy(credit_sum: float, n_results: int = 3) -> list[str]:
    collection = get_chroma().get_collection(name="company_policy")
    query = (
        f"Правила выдачи кредита при сумме {credit_sum} рублей. "
        f"Какое решение принимает политика по этой сумме?"
    )
    results = collection.query(query_texts=[query], n_results=n_results)
    return (results.get("documents") or [[]])[0]
