# NAS Monitor Panel

English | [中文](README.md)

A lightweight, modern NAS system monitoring panel that provides real-time system status, hardware monitoring, network statistics, and process management.

![NAS Monitor Panel](docs/screenshot.png)

## Features

- **System Information** - OS version, architecture, uptime, hostname
- **Hardware Monitoring** - CPU usage (overall/per-core), memory usage, temperature monitoring
- **Network Monitoring** - Network interface status, IP addresses, real-time upload/download speed
- **Storage Monitoring** - Disk partition usage, read/write statistics
- **Process Management** - Process list, CPU/memory usage, network connection status
- **Real-time Updates** - Configurable auto-refresh interval (default: 5 seconds)
- **Responsive Design** - Perfect adaptation for desktop and mobile devices
- **Dark Theme** - Modern dark UI design

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - High-performance async web framework
- **psutil** - System monitoring library
- **Uvicorn** - ASGI server

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript superset
- **Pinia** - Vue state management
- **Vite** - Next-generation frontend build tool

## Project Structure

```
nas-monitor-panel/
├── backend/                 # Backend code
│   ├── config.py           # Configuration management
│   ├── main.py             # FastAPI application entry
│   ├── requirements.txt    # Python dependencies
│   ├── routers/            # API routes
│   │   ├── system.py       # System information
│   │   ├── hardware.py     # Hardware status
│   │   ├── network.py      # Network status
│   │   ├── process.py      # Process management
│   │   └── storage.py      # Storage information
│   └── services/           # Business logic
│       └── collector.py    # Data collector
├── frontend/               # Frontend code
│   ├── src/
│   │   ├── App.vue         # Main application component
│   │   ├── components/     # Vue components
│   │   ├── stores/         # Pinia state management
│   │   └── utils/          # Utility functions
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── docs/                   # Documentation
├── docker/                 # Docker configuration
├── config.example.yaml     # Configuration example
└── README.md               # Project documentation
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nas-monitor-panel.git
cd nas-monitor-panel
```

#### 2. Configure the Project

Copy the example configuration and modify:

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` and set the data directory:

```yaml
host: 0.0.0.0
port: 8902
title: NAS Monitor Panel
refresh_interval: 5
data_dir: /path/to/your/data  # Change to your data directory
ws_enabled: true
```

#### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 4. Install Frontend Dependencies and Build

```bash
cd ../frontend
npm install
npm run build
```

#### 5. Start the Service

```bash
cd ../backend
python main.py
```

Visit http://localhost:8902 to use the panel.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/system/info` | GET | Get system information |
| `/api/system/uptime` | GET | Get system uptime |
| `/api/hardware/cpu` | GET | Get CPU information |
| `/api/hardware/memory` | GET | Get memory information |
| `/api/hardware/temperature` | GET | Get temperature information |
| `/api/network/interfaces` | GET | Get network interfaces |
| `/api/network/io` | GET | Get network IO statistics |
| `/api/process/list` | GET | Get process list |
| `/api/process/connections` | GET | Get network connections |
| `/api/storage/partitions` | GET | Get disk partitions |
| `/api/storage/io` | GET | Get storage IO statistics |

For detailed API documentation, see [docs/api.md](docs/api.md)

## Deployment

For detailed deployment instructions, see [docs/deployment.md](docs/deployment.md)

### Docker Deployment (Recommended)

```bash
# Build image
docker build -t nas-monitor-panel .

# Run container
docker run -d \
  --name nas-monitor \
  -p 8902:8902 \
  -v /path/to/data:/app/data \
  nas-monitor-panel
```

### Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/nas-monitor.service
```

```ini
[Unit]
Description=NAS Monitor Panel
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/nas-monitor-panel/backend
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable nas-monitor
sudo systemctl start nas-monitor
```

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `host` | `0.0.0.0` | Listen address |
| `port` | `8902` | Listen port |
| `title` | `NAS Monitor Panel` | Panel title |
| `refresh_interval` | `5` | Refresh interval (seconds) |
| `data_dir` | - | Data storage directory |
| `ws_enabled` | `true` | Enable WebSocket |

## Development Guide

### Local Development

```bash
# Backend development
cd backend
pip install -r requirements.txt
python main.py

# Frontend development (in another terminal)
cd frontend
npm install
npm run dev
```

The frontend dev server will start at http://localhost:5173 and automatically proxy API requests to the backend.

### Building Frontend

```bash
cd frontend
npm run build
```

Build output will be in the `frontend/dist/` directory.

## FAQ

### Q: Temperature monitoring shows "unavailable"?

A: Temperature monitoring requires system support. It may not be available in certain container environments or virtual machines.

### Q: How to change the port?

A: Edit the `port` configuration in `config.yaml`.

### Q: How to enable auto-start on boot?

A: See the Systemd configuration section in the deployment guide.

## Contributing

Issues and Pull Requests are welcome!

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## License

MIT License - See [LICENSE](LICENSE) file for details

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [psutil](https://github.com/giampaolo/psutil)
