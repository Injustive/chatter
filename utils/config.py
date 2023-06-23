DB_USER = "postgres"
DB_PASSWORD = "alex290900"
DB_DRIVER = "postgresql+asyncpg"
DB_HOST = "localhost"
DB_NAME = "chattele"
DB_DSN = "{}://{}:{}@{}/{}".format(DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

SERVER_HOST = "localhost"
SERVER_PORT = "24123"

JWT_SECRET = 'my_secret'
JWT_ACCESS_TTL = 60 * 30
JWT_REFRESH_TTL = 3600 * 24 * 60
