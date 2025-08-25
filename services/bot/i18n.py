
import abc


class BaseMessage(abc.ABC):
    ...


class ToMainMenuMessage(BaseMessage):
    values = {
        "en": "Main menu",
        "ru": "Главное меню"
    }

    def get(self, language: str) -> str:
        return self.values[language]


class BalanceMessage(BaseMessage):
    values = {
        "en": "Balance: {balance}",
        "ru": "Баланс: {balance}"
    }

    @classmethod
    def get(cls, language: str, balance: float) -> str:
        template = cls.values.get(language, cls.values["en"])
        return template.format(balance=balance)
