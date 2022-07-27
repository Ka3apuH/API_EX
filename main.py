import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from JsonLog.costom_logging import CustomizeLogger
from routers import parse_xml_file

config_path = Path(__file__).parent / 'JsonLog' / "logging_config.json"


def create_app() -> FastAPI:
    app_ = FastAPI(title='PERCo_API', debug=bool(os.getenv("DEBUG", False)))
    logger = CustomizeLogger.make_logger(config_path)
    app_.logger = logger
    return app_


app = create_app()

app.include_router(parse_xml_file.router)

@app.on_event("startup")
async def startup() -> None:
    pass


@app.on_event("shutdown")
async def shutdown() -> None:
    pass

if __name__ == '__main__':
    uvicorn.run("main:app",
                host=os.getenv("HOST"),
                port=int(os.getenv("PORT")),
                workers=int(os.getenv("WORKERS")),
                reload=True,
                access_log=True)
