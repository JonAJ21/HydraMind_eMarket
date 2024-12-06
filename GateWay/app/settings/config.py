
import environ

env = environ.Env()
environ.Env.read_env()


services = {
    'auth' : str(env('AUTH_SERVICE_URL')) + '/auth',
    'user' : str(env('USER_SERVICE_URL')) + '/user'
}
