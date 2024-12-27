
import environ

env = environ.Env()
environ.Env.read_env()


services = {
    'auth' : str(env('AUTH_SERVICE_URL')) + '/auth',
    'user' : str(env('USER_SERVICE_URL')) + '/user',
    'notification' : str(env('NOTIFICATION_SERVICE_URL')) + '/notification',
    'catalog' : str(env('CATALOG_SERVICE_URL')) + '/catalog',
    'recomendations' : str(env('RECOMENDATIONS_SERVICE_URL')) + '/recomendations'
}