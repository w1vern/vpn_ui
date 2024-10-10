import functools
import inspect
from telebot.types import Message
from app.database.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import *
from app.database.repositories import *



class RequestContext:
    def __init__(self) -> None:
        self.dependencies = {}
        self.cached = {}

    def set_depend(self, annotation, depend):
        self.dependencies[annotation] = depend

def request_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        rq = RequestContext()
        rq.set_depend(Message, args[0])
        return func(rq)
    return wrapper


class Container:
    def __init__(self) -> None:
        self.dependencies = {}
        self.requests = []

    def set_depend(self, annotation, depend):
        self.dependencies[annotation] = depend

    def inject(self, func):
        @functools.wraps(func)
        async def wrapper(rq_context: RequestContext = None):
            kwargs = {}
            if rq_context is None:
                rq_context = RequestContext()
            open_generators = []
            for arg, annot in func.__annotations__.items():
                if annot in rq_context.cached:
                    kwargs[arg] = rq_context.cached[annot]
                    continue
                depend = rq_context.dependencies.get(
                    annot, None) or self.dependencies.get(annot, None)
                if depend is None:
                    continue
                if inspect.isfunction(depend):
                    if "rq_context" in depend.__annotations__:
                        depend_result = depend(rq_context)
                    else:
                        depend_result = depend()
                    if inspect.iscoroutine(depend_result):
                        depend_result = await depend_result
                    if hasattr(depend_result, "__anext__"):
                        kwargs[arg] = await depend_result.__anext__()
                        open_generators.append((annot, depend_result))
                    else:
                        kwargs[arg] = depend_result
                else:
                    kwargs[arg] = depend
                rq_context.cached[annot] = kwargs[arg]
            res = await func(**kwargs)
            for annot, i in open_generators:
                try:
                    await i.__anext__()
                except StopAsyncIteration:
                    pass
                del rq_context.cached[annot]
            return res
        wrapper.__annotations__["rq_context"] = RequestContext
        return wrapper
    
def inject(di):
     def decorator(func):
            return request_decorator(di.inject(func))
     return decorator

di = Container()

@di.inject
async def get_user(session: AsyncSession, message: Message):
    ur = UserRepository(session)
    user = await ur.get_by_telegram_id(message.from_user.id)
    if user is None:
        user = await ur.create(telegram_id=message.from_user.id,
              telegram_username=message.from_user.username)
        await session.commit()
    return user

di.set_depend(AsyncSession, get_db_session)
di.set_depend(User, get_user)