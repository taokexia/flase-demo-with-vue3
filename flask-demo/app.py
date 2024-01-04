from app.wsgi import app
import app.models as models
from environs import Env

db = models.db
migrate = models.migrate

if __name__ == '__main__':
    env = Env()
    env.read_env()
    port = env.str('PORT') if env.str('PORT') else 9000
    app.run(port=port, host='0.0.0.0')