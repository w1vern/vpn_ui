
from fastapi.responses import JSONResponse


class SuccessResponse(JSONResponse):
    def __init__(self,
                 status_code: int = 200,
                 message: str = "OK"
                 ) -> None:
        super().__init__(
            status_code=status_code,
            content={"message": message}
        )
