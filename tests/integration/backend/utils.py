
from httpx import Response


def check_response(
    path: str,
    request_type: str,
    response: Response,
    good_status_code: int = 200,
    raise_anyway: bool = False
) -> None:
    if response.status_code != good_status_code or raise_anyway:
        raise Exception(
            f"{request_type} {path} failed. response: {response.json()}")
