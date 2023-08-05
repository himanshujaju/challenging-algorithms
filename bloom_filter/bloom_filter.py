from typing import List
from dataclasses import dataclass

@dataclass
class HashParams:
    base: int
    modulo: int

class BloomFilter:
    def __init__(self, bits: int):
        self._bits = bits
        self._markers = [False for _ in range(bits)]
        self._hashes = [
            HashParams(31, 1000000007),
            HashParams(43, 1000000009)
        ]

    def insert(self, item: str) -> None:
        positions = self._getHashes(item)
        for pos in positions:
            self._markers[pos] = True

    def contains(self, item: str) -> bool:
        positions = self._getHashes(item)
        for pos in positions:
            if not self._markers[pos]:
                return False

        return True

    def _getHashes(self, item: str) -> List[int]:
        ret = []
        for params in self._hashes:
            ret.append(self._getHash(item, params))
        return ret

    def _getHash(self, item: str, param: HashParams) -> int:
        ret = 0
        for i in item:
            ret = ret * param.base + ord(i)
            ret %= param.modulo
        return ret % self._bits