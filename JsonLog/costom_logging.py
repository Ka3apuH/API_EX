import json
import logging
import sys
from pathlib import Path
from typing import List

from loguru import logger,_Logger


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):

        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.bind(request_id='app'). \
            opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage())


class CustomizeLogger:

    @classmethod
    def make_logger(cls, config_path: Path) -> _Logger:

        config = cls.load_logging_config(config_path)
        logging_config = config['loggers']

        logger = cls.customize_logging(
            logging_config
        )

        return logger

    @classmethod
    def customize_logging(cls, list_log_seting: List[dict]):

        logger.remove()
        for log_seting in list_log_seting:
            logger.add(
                sink=sys.stdout,
                enqueue=True,
                catch=True,
                backtrace=False,
                diagnose=False,
                level=log_seting.get('level').upper(),
                format=log_seting.get('format')
            )
#curl -X GET http://localhost:8000/api/users
            logger.add(
                sink=Path(__file__).absolute().parents[1] / 'logs' / log_seting.get('filename'),
                rotation=log_seting.get('rotation'),
                enqueue=True,
                backtrace=False,
                diagnose=False,
                compression="zip",
                serialize=True,
                retention=log_seting.get('retention'),
                level=log_seting.get('level').upper(),
                format=log_seting.get('format'),
                catch=True
            )

        logging.basicConfig(handlers=[InterceptHandler()], level=0)

        for _log in [logging.getLogger(name) for name in logging.root.manager.loggerDict]:
            _log.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
