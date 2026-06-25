# 部署指南

本文档详细介绍如何在不同环境中部署 NAS Monitor Panel。

## 目录

- [环境要求](#环境要求)
- [手动部署](#手动部署)
- [Docker 部署](#docker-部署)
- [Systemd 服务](#systemd-服务)
- [Nginx 反向代理](#nginx-反向代理)
- [HTTPS 配置](#https-配置)
- [常见问题](#常见问题)

---

## 环境要求

### 硬件要求

- CPU: 1 核心以上
- 内存: 256MB 以上
- 磁盘: 100MB 以上可用空间

### 软件要求

| 软件 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Python | 3.8 | 3.10+ |
| Node.js | 16 | 18+ |
| pip | 20.0 | 最新 |
| npm | 7 | 9+ |

---

## 手动部署

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/nas-monitor-panel.git
cd nas-monitor-panel
```

### 2. 配置

```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml`：

```yaml
host: 0.0.0.0        # 监听地址，0.0.0.0 表示所有接口
port: 8902            # 监听端口
title: NAS Monitor Panel  # 面板标题
refresh_interval: 5   # 刷新间隔（秒）
data_dir: /var/lib/nas-monitor/data  # 数据目录
ws_enabled: true      # 启用 WebSocket
```

### 3. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

建议使用虚拟环境：

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 4. 构建前端

```bash
cd ../frontend
npm install
npm run build
```

### 5. 启动服务

```bash
cd ../backend
python main.py
```

服务将在 http://localhost:8902 启动。

---

## Docker 部署

### 使用 Dockerfile

#### 1. 构建镜像

```bash
docker build -t nas-monitor-panel .
```

#### 2. 运行容器

```bash
docker run -d \
  --name nas-monitor \
  --restart unless-stopped \
  -p 8902:8902 \
  -v /data/nas-monitor:/app/data \
  -e TZ=Asia/Shanghai \
  nas-monitor-panel
```

### 使用 Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  nas-monitor:
    build: .
    container_name: nas-monitor
    restart: unless-stopped
    ports:
      - "8902:8902"
    volumes:
      - /data/nas-monitor:/app/data
    environment:
      - TZ=Asia/Shanghai
```

启动：

```bash
docker-compose up -d
```

停止：

```bash
docker-compose down
```

---

## Systemd 服务

### 创建服务文件

```bash
sudo nano /etc/systemd/system/nas-monitor.service
```

### 服务配置

```ini
[Unit]
Description=NAS Monitor Panel
Documentation=https://github.com/yourusername/nas-monitor-panel
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=nas-monitor
Group=nas-monitor
WorkingDirectory=/opt/nas-monitor-panel/backend
ExecStart=/opt/nas-monitor-panel/backend/venv/bin/python main.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# 安全设置
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/data/nas-monitor

# 环境变量
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### 管理服务

```bash
# 创建用户
sudo useradd -r -s /bin/false nas-monitor

# 设置目录权限
sudo mkdir -p /data/nas-monitor
sudo chown nas-monitor:nas-monitor /data/nas-monitor

# 重载配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start nas-monitor

# 设置开机自启
sudo systemctl enable nas-monitor

# 查看状态
sudo systemctl status nas-monitor

# 查看日志
sudo journalctl -u nas-monitor -f
```

---

## Nginx 反向代理

### 安装 Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

### 配置反向代理

```bash
sudo nano /etc/nginx/conf.d/nas-monitor.conf
```

### HTTP 配置

```nginx
upstream nas_monitor {
    server 127.0.0.1:8902;
}

server {
    listen 80;
    server_name monitor.example.com;

    location / {
        proxy_pass http://nas_monitor;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 测试并重启

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## HTTPS 配置

### 使用 Let's Encrypt

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d monitor.example.com

# 自动续期
sudo certbot renew --dry-run
```

### 手动配置 SSL

```nginx
server {
    listen 443 ssl http2;
    server_name monitor.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://127.0.0.1:8902;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name monitor.example.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 常见问题

### 端口被占用

```bash
# 查看占用端口的进程
sudo lsof -i :8902

# 修改 config.yaml 中的 port 配置
```

### 权限问题

```bash
# 确保数据目录存在且有写权限
sudo mkdir -p /path/to/data
sudo chown -R nas-monitor:nas-monitor /path/to/data
```

### 防火墙配置

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 8902/tcp

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=8902/tcp
sudo firewall-cmd --reload
```

### 查看日志

```bash
# 手动部署
# 日志输出到终端

# Systemd
sudo journalctl -u nas-monitor -f

# Docker
docker logs -f nas-monitor
```

### 性能优化

1. **调整刷新间隔** - 增加 `refresh_interval` 值可降低系统负载
2. **限制进程数量** - API 支持 `limit` 参数限制返回的进程数量
3. **使用 SSD** - 如果存储监控频繁，建议使用 SSD 存储数据目录

---

## 更新部署

### 手动更新

```bash
cd /path/to/nas-monitor-panel
git pull

# 重新构建前端
cd frontend
npm install
npm run build

# 重启服务
sudo systemctl restart nas-monitor
```

### Docker 更新

```bash
docker-compose pull
docker-compose up -d
```

---

## 监控面板截图

部署完成后，您将看到如下界面：

![系统信息](../docs/screenshot-system.png)
![硬件状态](../docs/screenshot-hardware.png)
![网络监控](../docs/screenshot-network.png)
