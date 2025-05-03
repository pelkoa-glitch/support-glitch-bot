from dataclasses import asdict, dataclass
import json

@dataclass(frozen=True, eq=False)
class ApplicationException(Exception):
    @property
    def meta(self) -> dict:
        return asdict(self)

    @property
    def message(self) -> str:
        return 'Произошла ошибка в работе приложения'


@dataclass(frozen=True, eq=False)
class BaseWebException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def response_json(self) -> dict:
        return json.loads(self.response_content)

    @property
    def error_text(self) -> str:
        return self.response_json.get('detail', {}).get('error', '')
