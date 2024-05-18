# Installation Guide

## Prerequisities

-   Docker deamon
-   docker-compose

-   Python 3.10
-   pipreqs (if needed)

-   Node.js [^1]
-   pnpm (recommended, but yarn or other package managers should work) [^2]
-   dart-sass (for compiling scss)


[^1]: Do not run `apt install nodejs` under Ubuntu, as it will install an outdated version of Node.js. Use the [official version manager](https://github.com/nvm-sh/nvm) tool instead. 

[^2]: Vallina npm is not recommended. Get yourself a handy package manager.

## Installation

Windows系统建议安装docker desktop，方便管理

git clone https://github.com/Yuntian12345/banner_diffusion_docker.git

cd banner_diffusion_docker

git submodule init

git submodule update --init --remote --merge --recursive

git submodule update --remote --merge（如果不是第一次下载，可以用此命令来更新submodule）

建议每次都以bash方式运行：
bash setup.sh


打开http://localhost:8080/  以查看页面
