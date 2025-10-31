
import uvicorn

from shared.config import BootLevel, env_config

if __name__ == "__main__":
    uvicorn.run(
        "services.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if env_config.boot_level == BootLevel.DEBUG else False,
        workers=env_config.backend.workers
    )