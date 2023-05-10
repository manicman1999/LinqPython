from __future__ import annotations
from collections import defaultdict
import random
from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, TypeVar, Union

T = TypeVar('T')
R = TypeVar('R')

def identity(inp: Any) -> Any:
        return inp

class LinqList(List[T]):

    def select(self, key_func: Callable[[T], R]) -> LinqList[R]:
        return LinqList(map(key_func, self))

    def order_by(self, *key_funcs: Callable[[T], Any]) -> LinqList[T]:
        def combined_key_func(item: T) -> tuple:
            return tuple(key_func(item) for key_func in key_funcs)
        
        return LinqList(sorted(self, key=combined_key_func))

    def sum_of(self, key_func: Callable[[T], Union[int, float]] = identity) -> Union[float, int]:
        return sum(key_func(item) for item in self)

    def where(self, key_func: Callable[[T], bool]) -> LinqList[T]:
        return LinqList(filter(key_func, self))
    
    def count(self, key_func: Callable[[T], bool] = identity) -> int:
        return len(list(filter(key_func, self)))
    
    def distinct(self, key_func: Callable[[T], Any] = identity) -> LinqList[T]:
        unique_keys = set()
        distinct_items = LinqList()

        for item in self:
            key = key_func(item)
            if key not in unique_keys:
                unique_keys.add(key)
                distinct_items.append(item)

        return distinct_items
    
    def distinct_count(self, key_func: Callable[[T], R] = identity) -> Dict[R, int]:
        distinct_counts: Dict[R, int] = {}

        for item in self:
            key = key_func(item)
            distinct_counts[key] = distinct_counts.get(key, 0) + 1

        return distinct_counts
    
    def first(self, key_func: Callable[[T], bool], default: Optional[T] = None) -> Optional[T]:
        filtered = self.where(key_func)
        return default if filtered.count() == 0 else filtered[0]
    
    def last(self, key_func: Callable[[T], bool], default: Optional[T] = None) -> Optional[T]:
        filtered = self.where(key_func)
        return default if filtered.count() == 0 else filtered[-1]
    
    def skip(self, amount: int) -> LinqList[T]:
        return LinqList(self[amount:])
    
    def shift(self, amount: int) -> LinqList[T]:
        return LinqList(self[amount:] + self[:amount])
    
    def take(self, amount: int) -> LinqList[T]:
        return LinqList(self[:amount])
    
    def group_by(self, key_func: Callable[[T], R]) -> Dict[R, LinqList[T]]:
        result = defaultdict(LinqList)
        for item in self:
            key = key_func(item)
            result[key].append(item)
        return result
