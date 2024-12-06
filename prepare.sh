
mkdir ./AuthService/app/certs

openssl genrsa -out ./AuthService/app/certs/jwt-private.pem 2048
openssl rsa -in ./AuthService/app/certs/jwt-private.pem -outform PEM -pubout -out ./AuthService/app/certs/jwt-public.pem

cp ./AuthService/docker-compose/.env.example ./AuthService/docker-compose/.env
cp ./DataBase/docker-compose/.env.example ./DataBase/docker-compose/.env