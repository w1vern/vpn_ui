
import json
from importlib import resources

from .enums import LanguageCodes, MessageKey

with resources.files(__package__).joinpath("repository.json").open("r", encoding="utf-8") as f:
    CATALOG: dict[str, dict[str, str]] = json.load(f)


class I18nMessage():
    def __init__(self, message_key: MessageKey, **kwargs) -> None:
        self.message_key = message_key
        self.kwargs = kwargs

    def render(self, language_code: LanguageCodes, **kwargs) -> str:
        kwargs.update(self.kwargs)
        string = CATALOG[self.message_key.value][language_code.value]
        return string.format(**kwargs)
