
mkdir ./AuthService/app/certs

openssl genrsa -out ./AuthService/app/certs/jwt-private.pem 2048
openssl rsa -in ./AuthService/app/certs/jwt-private.pem -outform PEM -pubout -out ./AuthService/app/certs/jwt-public.pem

cp ./AuthService/docker-compose/.env.example ./AuthService/docker-compose/.env
cp ./NotificationService/docker-compose/.env.example ./NotificationService/docker-compose/.env
cp ./DataBase/docker-compose/.env.example ./DataBase/docker-compose/.env
cp ./UserService/docker-compose/.env.example ./UserService/docker-compose/.env
cp ./GateWay/docker-compose/.env.example ./GateWay/docker-compose/.env
cp ./CatalogService/docker-compose/.env.example ./CatalogService/docker-compose/.env
cp ./GUI/docker-compose/.env.example ./GUI/docker-compose/.env
cp ./PaymentService/docker-compose/.env.example ./PaymentService/docker-compose/.env

