import logging

from pydantic import BaseModel, ValidationError


logger = logging.getLogger(__name__)


class ExtractValidationError(Exception):
    def __init__(self, type_error: str, missing_key: str):
        super().__init__(f"Configuration data could not be retrieved! {type_error} - `{missing_key}`")


class ConfigurationModel(BaseModel):
    default_language: str
    path_locales: str
    prefix_keyboard: str


def extract_data(
        input_dict: dict
) -> ConfigurationModel:
    try:
        model = ConfigurationModel(**input_dict)
    except ValidationError as e:
        error = e.errors()[0]
        logger.error(error)
        raise ExtractValidationError(error['msg'], error['loc'][0])
    else:
        return model
