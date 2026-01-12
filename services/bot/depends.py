
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    LanguageCodes,
    ServerInboundRepository,
    ServerRepository,
    TariffRepository,
    TransactionRepository,
    User,
    UserRepository,
    session_manager
)
from shared.infrastructure import setup_logger

from .buttons import main_menu_keyboard
from .exceptions import (
    MessageUserIsNoneException,
    SendFeedbackToAdminException,
    UserNotFoundException
)
from .i18n import I18nMessage, MessageKey
from .models import MainMessage, UserInfo
from .redis import RedisType, get_redis_client

logger = setup_logger(__name__)


async def get_session(
    session: AsyncSession | None = None
) -> AsyncSession:
    logger.debug('get_session called')
    if session is None:
        return await session_manager.session().__anext__()
    return session


def get_user_repo(
    session: AsyncSession = Depends(get_session)
) -> UserRepository:
    logger.debug('get_user_repo called')
    return UserRepository(session)


def get_tariff_repo(
    session: AsyncSession = Depends(get_session)
) -> TariffRepository:
    return TariffRepository(session)


def get_server_repo(
    session: AsyncSession = Depends(get_session)
) -> ServerRepository:
    return ServerRepository(session)


def get_server_inbound_repo(
    session: AsyncSession = Depends(get_session)
) -> ServerInboundRepository:
    return ServerInboundRepository(session)


def get_transaction_repo(
    session: AsyncSession = Depends(get_session)
) -> TransactionRepository:
    return TransactionRepository(session)


def get_user_info(
    message: Message | None = None,
    callback_query: CallbackQuery | None = None,
    user_info: UserInfo | None = None
) -> UserInfo:
    if user_info is not None:
        return user_info
    if message is not None:
        tmp = message
    elif callback_query is not None:
        tmp = callback_query
    else:
        raise SendFeedbackToAdminException()
    if not tmp.from_user:
        raise MessageUserIsNoneException()
    if tmp.from_user.username:
        username = tmp.from_user.username
    else:
        username = ""
    if tmp.from_user.language_code:
        lang_code = LanguageCodes(tmp.from_user.language_code)
    else:
        lang_code = LanguageCodes.en
    return UserInfo(
        id=tmp.from_user.id,
        username=username,
        lang_code=lang_code
    )


def get_request_data(
    message: Message | None = None,
    callback_query: CallbackQuery | None = None
) -> str:
    if message is None:
        if not callback_query is None:
            data = callback_query.data
        else:
            return ""
    else:
        data = message.text
    if data is None:
        raise SendFeedbackToAdminException()
    return data


async def get_user(
    user_info: UserInfo = Depends(get_user_info),
    ur: UserRepository = Depends(get_user_repo)
) -> User:
    user = await ur.get_by_telegram_id(user_info.id)
    if user:
        if user.telegram_username != user_info.username:
            await ur.update_telegram_username(user, user_info.username)
        return user
    raise UserNotFoundException()


async def get_main_message(
    user_info: UserInfo = Depends(get_user_info),
    redis: Redis = Depends(get_redis_client)
) -> MainMessage:
    main_message = await redis.get(f"{RedisType.main_message.value}:{user_info.id}")
    if main_message is None:
        main_message = MainMessage(
            text=[I18nMessage(MessageKey.main_menu).render(
                user_info.lang_code)],
            notifications=[],
            buttons=main_menu_keyboard()
        )
        await redis.set(
            name=f"{RedisType.main_message.value}:{user_info.id}",
            value=main_message.to_str()
        )
        return main_message
    return MainMessage.from_str(main_message)
