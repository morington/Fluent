import logging
from typing import Optional
from pathlib import Path

from fluent.runtime import FluentLocalization, FluentResourceLoader

from .configuration import extract_data, ConfigurationModel

logger = logging.getLogger()


class FLL(FluentLocalization):
    def __init__(self, prefix_keyboard: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix_keyboard = prefix_keyboard

    def get_keyboard_localization(self, msg: str) -> Optional[str]:
        for bundle in self._bundles():
            keyboard_localization: dict[Optional[str], Optional[str]] = {
                bundle.format_pattern(bundle.get_message(key).value)[0]: key
                for key in bundle._messages.keys()
                if self.prefix_keyboard in key
            }
            return keyboard_localization.get(msg, None)
        return None


class FluentDispenser:
    def __init__(self, configuration_dict: dict):
        configuration: ConfigurationModel = extract_data(input_dict=configuration_dict)

        locales_dir: Path = Path(__file__).parent.joinpath(configuration.path_locales)
        self.__loader = FluentResourceLoader(str(locales_dir) + "/{locale}")
        self.__default_language = configuration.default_language
        self.languages = dict()

        dirs_names = set()
        default_language_dir = None
        for item in locales_dir.iterdir():
            dirs_names.add(item.name)
            if item.name == self.__default_language:
                default_language_dir = item

        if not default_language_dir:
            raise ValueError("FluentDispenser: default language directory not found")

        ftl_files_list = [item.name for item in default_language_dir.iterdir() if item.suffix == ".ftl"]

        for name in dirs_names:
            if name == self.__default_language:
                self.languages[name] = FLL(
                    configuration.prefix_keyboard,
                    [self.__default_language], ftl_files_list, self.__loader
                )
            else:
                self.languages[name] = FLL(
                    configuration.prefix_keyboard,
                    [name, self.__default_language], ftl_files_list, self.__loader
                )

    @property
    def default_locale(self) -> FLL:
        return self.languages[self.__default_language]

    @property
    def available_languages(self) -> list[str]:
        return list(self.languages.keys())

    def get_localization(self, language_code: str) -> FLL:
        localization: FLL = self.languages.get(language_code, self.default_locale)
        if language_code not in localization.locales:
            logger.warning(f"Language `{language_code}` not found")
        return localization
