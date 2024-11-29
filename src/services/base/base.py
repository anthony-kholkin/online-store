import math
from typing import Any, Sequence

from db.models import BaseModel


class BaseService:
    @staticmethod
    def get_pagination_result(objects: Sequence[BaseModel], page: int, size: int, total: int) -> dict[str, Any]:
        return {
            "items": list(objects),
            "page": page,
            "size": size,
            "pages": math.ceil(total / size),
            "total": total,
        }
