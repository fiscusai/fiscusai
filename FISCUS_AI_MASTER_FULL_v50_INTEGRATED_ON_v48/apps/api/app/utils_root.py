from typing import List, Tuple, Any

def paginate(items: List[Any], page: int = 1, page_size: int = 20) -> Tuple[List[Any], int]:
    if page < 1: page = 1
    if page_size < 1: page_size = 20
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], total
