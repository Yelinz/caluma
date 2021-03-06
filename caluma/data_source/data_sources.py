import logging

logger = logging.getLogger(__name__)


class BaseDataSource:
    """Basic data source class to be extended by any data source implementation.

    The `get_data`-method should return an iterable. This iterable can contain strings,
    ints, floats and also iterables. Those contained iterables can consist of maximally
    two items. The first will be used for the option name, the second one for it's
    value. If only one value is provided, this value will also be used as choice name.

    Examples:
        [['my-option', {"en": "english description", "de": "deutsche Beschreibung"}, ...]
        [['my-option', "my description"], ...]
        ['my-option', ...]
        [['my-option'], ...]

    Properties:
        info: Informational string about this data source
        default: default value to return if execution of `get_data()` fails.
                 If this is `None`, the Exception won't be handled. Defaults to None.
        validate: boolean that indicates if answers should be validated against the
                  current response from `get_data()`. Defaults to `True`.

    A custom data source class could look like this:
    ```
    >>> from caluma.data_source.data_sources import BaseDataSource
    ... from caluma.data_source.utils import data_source_cache
    ... import requests
    ...
    ...
    ... class CustomDataSource(BaseDataSource):
    ...     info = 'User choices from "someapi"'
    ...
    ...     @data_source_cache(timeout=3600)
    ...     def get_data(self, info, answer_value=None):
    ...         response = requests.get(
    ...             f"https://someapi/?user={info.context.request.user.username}"
    ...         )
    ...         return [result["value"] for result in response.json()["results"]]
    ```

    """

    info = None
    default = None
    validate = True

    def __init__(self):
        pass

    def get_data(self, info, answer_value=None):  # pragma: no cover
        raise NotImplementedError()

    def try_get_data_with_fallback(self, info, answer_value=None):
        try:
            new_data = self.get_data(info, answer_value)
        except Exception as e:
            logger.exception(
                f"Executing {type(self).__name__}.get_data() failed:"
                f"{e}\n Using default data."
            )
            if self.default is None:
                raise e
            return self.default
        return new_data
