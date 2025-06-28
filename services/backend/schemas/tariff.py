

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from shared.database import Tariff


class TariffSchema(BaseModel):
    id: UUID
    name: str
    duration: int
    price: float
    price_of_traffic_reset: float
    traffic: int
    is_special: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_db(cls, tariff: Tariff) -> 'TariffSchema':
        return cls(
            id=tariff.id,
            name=tariff.name,
            duration=tariff.duration.seconds,
            price=tariff.price,
            price_of_traffic_reset=tariff.price_of_traffic_reset,
            traffic=tariff.traffic,
            is_special=tariff.is_special
        )


class CreateTariffSchema(BaseModel):
    name: str
    duration: int
    price: float
    price_of_traffic_reset: float
    traffic: int
    is_special: bool

class EditTariffSchema(BaseModel):
    name: str | None = None
    duration: int | None = None
    price: float | None = None
    price_of_traffic_reset: float | None = None
    traffic: int | None = None

