

from dataclasses import dataclass, field
from typing import List

from domain.entities.base import BaseEntity


@dataclass
class Category(BaseEntity):
    category_name: str
    
    sub_category_ids: List[str] = field(
        default_factory=list,
        kw_only=True
    )
    
    parent_category: str = ''
    
    
    