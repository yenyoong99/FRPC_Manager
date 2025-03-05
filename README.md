# FRP Manager

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-green.svg)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

FRP Manager is a web-based management platform for FRP (Fast Reverse Proxy) that simplifies the process of managing multiple proxy configurations across different projects. It provides an intuitive interface for handling port forwarding, network tunneling, and access control.

## ✨ Features

- 🚀 Easy-to-use web interface for FRP management
- 🔐 Token-based authentication for secure proxy access
- 🌐 Multi-project support with isolated configurations
- 🔄 Dynamic port allocation and management
- 📊 Real-time status monitoring
- 🛡️ Access control and permission management
- 🐳 Docker support for quick deployment
- 💻 Cross-platform compatibility

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vue.js 3
- **Database**: SQLAlchemy
- **Proxy Tool**: frpc.exe
- **Containerization**: Docker

## 🚀 Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yenyoong99/frp-manager.git
cd frp-manager
```

2. Start the application using Docker Compose:
```bash
docker-compose up -d
```

3. Access the web interface at `http://localhost:8080`

Default Admin Account:

username: admin
password: admin123456

## 📝 Configuration

### Environment Variables

```env
DATABASE_URL=sqlite:///./frp.db
SECRET_KEY=your-secret-key
FRP_BINARY_PATH=/path/to/frpc
```

### FRP Configuration

The system automatically generates FRP configurations based on your settings. Each project gets its own configuration file with:

- Unique ports
- Custom authentication tokens
- Specific server endpoints
- Access control rules

## 🔧 Usage

1. **Login to Dashboard**: Access the web interface and login with your credentials
2. **Create New Proxy**: Fill in the required details:
   - Client Name
   - Server IP
   - Server Port
   - Remote Port
   - Access Token
3. **Manage Proxies**: Start, stop, or modify existing proxy configurations
4. **Monitor Status**: Check the running status and logs of your proxy servers

## 📱 Client Configuration

### Setting Up FRP Client

1. **Download FRP Client**
   - Download the appropriate FRP client version for your operating system from [FRP releases](https://github.com/fatedier/frp/releases)
   - Extract the downloaded package to get `frpc.exe` (Windows) or `frpc` (Linux/Mac)

2. **Configure FRP Client**
   Create a `frpc.ini` file in the same directory as your frpc executable:
   ```ini
   [common]
   server_addr = <your_server_ip>
   server_port = <server_port>
   token = <your_access_token>

   [your_service_name]
   type = tcp
   local_ip = 127.0.0.1
   local_port = <your_local_port>
   remote_port = <assigned_remote_port>
   ```

3. **Start the Client**
   - **Windows**: 
     ```batch
     frpc.exe -c frpc.ini
     ```
   - **Linux/Mac**:
     ```bash
     ./frpc -c ./frpc.ini
     ```

### Example Configurations

1. **Web Application**
   ```ini
   [web_app]
   type = tcp
   local_port = 3000
   remote_port = 8001
   ```

2. **Database Service**
   ```ini
   [database]
   type = tcp
   local_port = 5432
   remote_port = 8002
   ```

3. **Game Server**
   ```ini
   [game_server]
   type = tcp
   local_port = 27015
   remote_port = 8003
   ```

### Usage Tips

1. **Port Forwarding**
   - Make sure your local service is running before starting FRP client
   - Verify the local port is correctly set in `frpc.ini`
   - Ensure remote port matches the one assigned in FRP Manager

2. **Security**
   - Keep your access token secure
   - Use unique tokens for different services
   - Regularly update your FRP client version

3. **Troubleshooting**
   - Check if local service is running
   - Verify network connectivity
   - Ensure ports are not blocked by firewall
   - Review FRP client logs for errors

4. **Best Practices**
   - Use descriptive service names
   - Document port mappings
   - Monitor bandwidth usage
   - Set up automatic client startup

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FRP Project](https://github.com/fatedier/frp)
- FastAPI Team
- Vue.js Team
````
