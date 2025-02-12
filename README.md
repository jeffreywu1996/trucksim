# Truck Fleet Monitor

A real-time truck fleet monitoring system that tracks location, status, and performance metrics of multiple trucks simultaneously.

## Features

- Real-time truck location tracking on an interactive map
- Live fleet statistics (total trucks, average speed, fuel levels, etc.)
- Individual truck status monitoring
- Historical data tracking
- Search functionality for specific trucks
- WebSocket-based real-time updates

## Tech Stack

- Frontend:
  - React
  - Mapbox GL JS
  - WebSocket client
  - CSS3 with Flexbox/Grid

- Backend:
  - FastAPI (Python)
  - WebSocket server
  - SQLAlchemy ORM
  - Alembic migrations

- Database:
  - TimescaleDB (PostgreSQL with time-series extension)
  - Redis for real-time data caching

- Infrastructure:
  - Docker
  - Docker Compose

## Prerequisites

- Docker and Docker Compose
- Mapbox API token
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/truck-fleet-monitor.git
cd truck-fleet-monitor
```

2. Copy the example environment file and update it with your credentials:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Build and start the services:
```bash
make dev
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Directory Structure
```
.
├── frontend/          # React frontend application
├── backend/           # FastAPI backend application
├── simulator/         # Truck simulation service
├── docker-compose.yml # Docker services configuration
└── Makefile          # Development commands
```

### Available Make Commands
- `make dev`: Start development environment
- `make build`: Build all services
- `make clean`: Clean up containers and volumes
- `make test`: Run tests
- `make lint`: Run linters

## API Documentation

The API documentation is available at `/docs` when the backend is running. It includes:
- WebSocket endpoints
- REST endpoints
- Data models
- Authentication methods

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
