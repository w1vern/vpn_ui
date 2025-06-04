import functools
import inspect



class RequestContext:
    def __init__(self) -> None:
        self.dependencies = {}
        self.cached = {}

    def set_depend(self, annotation, depend):
        self.dependencies[annotation] = depend


class Container:
    def __init__(self) -> None:
        self.dependencies = {}
        self.requests = []

    def set_depend(self, annotation, depend):
        self.dependencies[annotation] = depend

    def inject(self, func):
        @functools.wraps(func)
        async def wrapper(rq_context: RequestContext | None = None):
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
