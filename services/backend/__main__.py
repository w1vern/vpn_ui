
import uvicorn

from shared.config import env_config

if __name__ == "__main__":
    uvicorn.run(
        "services.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=env_config.backend.workers
    )