from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


class AutoSchemaMixin:
    """
    Автоматически добавляет path-параметры и теги в OpenAPI-схему.
    Просто наследуй класс и укажи tags = ["..."] при необходимости.
    """

    # Можно переопределить в наследнике
    tags: list[str] = []
    params: dict[str, str] = {}

    @classmethod
    def _build_openapi_params(cls, params):
        return [
            OpenApiParameter(
                name,
                OpenApiTypes.INT,
                OpenApiParameter.PATH,
                description=desc,
            )
            for name, desc in cls.params.items()
        ]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        extend_schema(
            parameters=cls._build_openapi_params(cls.params),
            tags=cls.tags or [cls.__name__],
        )(cls)
