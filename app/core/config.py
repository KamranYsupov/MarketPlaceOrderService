from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта"""

    project_name: str = Field(title='Название проекта')
    api_v1_prefix: str = Field(title='Префикс первой версии API', default='/api/v1')
    auth_users_service_api_v1_url: str = Field(
        title='AuthUsersService API URL',
        default='http://127.0.0.1:8000/api/v1',
    )
    product_service_api_v1_url: str = Field(
        title='ProductSellerService API URL',
        default='http://127.0.0.1:9000/api/v1',
    )
    graphql_prefix: str = Field(title='GraphQL prefix', default='/graphql')

    # region Настройки БД
    db_user: str = Field(title='Пользователь БД')
    db_password: str = Field(title='Пароль БД')
    db_host: str = Field(title='Хост БД')
    db_port: int = Field(title='Порт ДБ', default='5432')
    db_name: str = Field(title='Название БД')
    metadata_naming_convention: dict[str, str] = Field(
        default={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s'
        })

    sqlite_default_url: str = Field(
        default='sqlite+aiosqlite:///./db.sqlite3'
    )

    # endregion

    container_wiring_modules: list = Field(
        title='Модули контейнера',
        default=[
            'app.api.v1.endpoints.order',
            'app.api.v1.deps',
            'app.db.models.order',
        ]
    )

    @property
    def db_url(self) -> str:
        return self.sqlite_default_url

    class Config:
        env_file = '.env'


settings = Settings()
