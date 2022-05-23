from cerberus import Validator
from bin.logger import logger


def equal_schema(response, schema):
    v = Validator()
    result = v.validate(response, schema)
    if not result:
        logger.info(v.errors)
    assert result, v.errors
