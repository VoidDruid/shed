from pydantic import BaseSettings

__lang_name__ = 'shed'
__lang_extension__ = 'sd'

# TODO: .rc file and it's location, use env vars for customization


class Settings(BaseSettings):
    pass


settings = BaseSettings()
