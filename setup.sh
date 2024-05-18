# bash

docker-compose down;

basepath=$(realpath $(dirname $0));

# build frontend

cd $basepath/frontend;
pnpm install;
pnpm build;

cd $basepath;
rm -rf ./static;
mv ./frontend/dist ./static;

# build backend image
#cd $basepath/backend;
#git reset --hard;
#git pull;


cd $basepath

docker-compose up -d --build;

