# Fluent


# Using Fluent using the aiogram3.x bot as an example:

Initialization in the main file:
```python
from Fluent.dispenser import FluentDispenser

l10n_dispenser = FluentDispenser(configuration_dict={
    "default_language": 'ru',
    "path_locales": 'locales',
    "prefix_keyboard": 'test_keyboards'
})

L10nMiddleware(dispenser=l10n_dispenser, lang='ru')
```

Creating middleware:
```python
from Fluent.dispenser import FluentDispenser, FLL

class L10nMiddleware(BaseMiddleware):
    def __init__(self, dispenser: FluentDispenser, lang: str):
        self.lang = lang
        self.dispenser = dispenser

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["l10n"]: FLL = self.dispenser.get_localization(self.lang)

        return await handler(event, data)
```

Use in handlers:
```python
async def posting(message: Message, l10n: FLL):
        await message.answer(
            text=l10n.format_value(msg_id='what-is-python')
        )
```

Creating filtering on Fluent buttons:
```python
router.message.register(my_handler, FLL.get_keyboard_localization("button-name-in-Fluent"))
```