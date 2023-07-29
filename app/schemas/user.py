from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема просмотра юзера."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема создания юзера."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема измениния юзера."""
    pass
