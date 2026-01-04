
import json
from importlib import resources

import html

from shared.database import LanguageCodes

from .enums import MessageKey


with (resources
      .files(__package__)
      .joinpath("repository.json")
      .open("r", encoding="utf-8")
      ) as f:
    CATALOG: dict[str, dict[str, str]] = json.load(f)


class I18nMessage():
    def __init__(
        self,
        message_key: MessageKey,
        **kwargs: object
    ) -> None:
        self.message_key = message_key
        self.kwargs = kwargs

    def render(
        self,
        language_code: LanguageCodes,
        **kwargs: object
    ) -> str:
        final_kwargs = {**self.kwargs, **kwargs}
        safe_kwargs = {
            k: html.escape(str(v)) for k, v in final_kwargs.items()
        }
        string = CATALOG[self.message_key.value][language_code.value]
        return string.format(**safe_kwargs)
