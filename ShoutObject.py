from dataclasses import dataclass

@dataclass
class ShoutObject:
    character: str
    _onyomi: list[str] | None
    _kunyomi: list[str] | None
    yomi: str | None


    @property
    def onyomi_string(self) -> str | None:
        return "・".join(self._onyomi) if self._onyomi else None


    @property
    def kunyomi_string(self) -> str:
        return "・".join(self._kunyomi) if self._kunyomi else None
