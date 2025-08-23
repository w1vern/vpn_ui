
from uuid import UUID

from aiogram.types import CallbackQuery, Message
from fast_depends import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    PanelServerRepository,
    ServerRepository,
    TransactionRepository,
    User,
    UserRepository,
    session_manager
)
from shared.infrastructure import setup_logger, CodeToTG

from .exceptions import (
    MessageUserIsNoneException,
    MessageUsernameIsNoneException,
    SendFeedbackToAdminException,
    UserNotFoundException
)
from .models import MainMessage, UserInfo
from .redis import RedisType, get_redis_client
from .states import MyState

logger = setup_logger(__name__)


async def get_user_repo(session: AsyncSession = Depends(session_manager.session)
                        ) -> UserRepository:
    return UserRepository(session)


async def get_server_repo(session: AsyncSession = Depends(session_manager.session)
                          ) -> ServerRepository:
    return ServerRepository(session)


async def get_panel_server_repo(session: AsyncSession = Depends(session_manager.session)
                                ) -> PanelServerRepository:
    return PanelServerRepository(session)


async def get_transaction_repo(session: AsyncSession = Depends(session_manager.session)
                               ) -> TransactionRepository:
    return TransactionRepository(session)


async def get_user_info(message: Message | None = None,
                        callback_query: CallbackQuery | None = None,
                        # data: CodeToTG | None = None,
                        id: int | None = None
                        ) -> UserInfo:
    # if data is not None:
    #    return UserInfo(data.tg_id, "")
    if id is not None:
        return UserInfo(id, "")
    if message is not None:
        tmp = message
    elif callback_query is not None:
        tmp = callback_query
    else:
        raise SendFeedbackToAdminException()
    if not tmp.from_user:
        raise MessageUserIsNoneException()
    if not tmp.from_user.username:
        raise MessageUsernameIsNoneException()
    return UserInfo(tmp.from_user.id,
                    tmp.from_user.username)


async def get_request_data(message: Message | None = None,
                           callback_query: CallbackQuery | None = None
                           ) -> str:
    if message is None:
        if not callback_query is None:
            data = callback_query.data
        else:
            # raise SendFeedbackToAdminException()
            return ""
    else:
        data = message.text
    if data is None:
        raise SendFeedbackToAdminException()
    return data


async def create_user(user_info: UserInfo = Depends(get_user_info),
                      ur: UserRepository = Depends(get_user_repo)
                      ) -> User:

    user = await ur.get_by_telegram_id(user_info.id)
    if user:
        return user
    user = await ur.create(user_info.id,
                           user_info.username,
                           UUID(int=0))
    return user


async def get_user(user_info: UserInfo = Depends(get_user_info),
                   ur: UserRepository = Depends(get_user_repo)
                   ) -> User:
    user = await ur.get_by_telegram_id(user_info.id)
    if user:
        if user.telegram_username != user_info.username:
            await ur.update_telegram_username(user, user_info.username)
        return user
    raise UserNotFoundException()


async def get_state(user_info: UserInfo = Depends(get_user_info),
                    redis: Redis = Depends(get_redis_client)
                    ) -> MyState:
    state = await redis.get(f"{RedisType.state.value}:{user_info.id}")
    return MyState.from_str(state)


async def get_main_message(user_info: UserInfo = Depends(get_user_info),
                           redis: Redis = Depends(get_redis_client)
                           ) -> MainMessage:
    main_message = await redis.get(f"{RedisType.main_message.value}:{user_info.id}")
    if main_message is None:
        raise SendFeedbackToAdminException()
    return MainMessage.from_str(main_message)
