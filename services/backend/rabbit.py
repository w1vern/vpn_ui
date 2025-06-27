

from faststream.rabbit import (
    RabbitBroker,
    fastapi,
)

from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    tg_code_queue,
)

router = fastapi.RabbitRouter(RABBIT_URL)


def get_broker() -> RabbitBroker:
    return router.broker


async def send_tg_code(data: CodeToTG, broker: RabbitBroker) -> None:
    print(data)
    await broker.publish(data, tg_code_queue)
