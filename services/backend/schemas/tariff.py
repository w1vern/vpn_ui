
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from shared.database import UNSET, Tariff, Unset


class TariffSchema(BaseModel):
    id: UUID
    name: str
    description: str
    duration: int
    price: float
    price_of_traffic_reset: float
    traffic: int
    with_access: bool
    with_unavailable_inbounds: bool
    is_special: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_db(cls, tariff: Tariff) -> 'TariffSchema':
        return cls(
            id=tariff.id,
            name=tariff.name,
            description=tariff.description,
            duration=tariff.duration.seconds,
            price=tariff.price,
            price_of_traffic_reset=tariff.price_of_traffic_reset,
            traffic=tariff.traffic,
            with_access=tariff.with_access,
            with_unavailable_inbounds=tariff.with_unavailable_inbounds,
            is_special=tariff.is_special
        )


class CreateTariffSchema(BaseModel):
    name: str
    duration: int
    description: str
    price: float
    price_of_traffic_reset: float
    traffic: int
    with_access: bool
    with_unavailable_inbounds: bool
    is_special: bool

class EditTariffSchema(BaseModel):
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    duration: int | Unset = UNSET
    price: float | Unset = UNSET
    price_of_traffic_reset: float | Unset = UNSET
    traffic: int | Unset = UNSET
    with_access: bool | Unset = UNSET
    with_unavailable_inbounds: bool | Unset = UNSET
    is_special: bool | Unset = UNSET
