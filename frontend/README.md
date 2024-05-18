### 本地部署

安装 dart-sass, Node.js >= 20, 随后clone本项目

```shell
cd BannerDiff-Frontend
pnpm install
pnpm dev
```

随后可访问.

若要和后端联调，则需要安装反向代理程序 (比如Nginx, Caddy等)，然后配置

- / -> 前端(vite)
- /api/{anything} -> 后端

示例Nginx配置

```
server {
    listen 8080;
    listen [::]:8080;

    location ~ ^/api/(.+) {
        proxy_pass http://localhost:5000/$1;

        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://localhost:5173/;
    }
}
```