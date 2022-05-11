from config import Config


class Utils():
    def check_password(password: str, config: Config) -> bool:
        return password == config.password
