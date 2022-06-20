from dataclasses import dataclass

@dataclass
class ShoutObject:
    _character: str
    _onyomi: list[str] | None
    _kunyomi: list[str] | None
    _yomi: str | None

    @property
    def character(self) -> str:
        return self._character

    @property
    def onyomi_string(self) -> str | None:
        return "・".join(self._onyomi) if self._onyomi else None

    @property
    def kunyomi_string(self) -> str:
        return "・".join(self._kunyomi) if self._kunyomi else None

    @property
    def yomi(self) -> str:
        return self._yomi