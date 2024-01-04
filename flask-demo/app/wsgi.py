from app import create_app
from environs import Env

app = create_app()

if __name__ == '__main__':
    env = Env()
    env.read_env()
    port = env.str('PORT') if env.str('PORT') else 9000
    app.run(port=port, host='0.0.0.0')