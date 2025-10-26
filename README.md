# Social Media Microservices Platform

A scalable, production-ready social media platform built with a microservices architecture, featuring real-time updates, cloud-native deployment, and modern DevOps practices.

## 🏗️ Architecture

This project demonstrates enterprise-level microservices architecture with the following components:

### Microservices
- **Authentication Service** - JWT-based authentication and authorization (Python/Flask)
- **User Service** - User profile management and operations (Python/Flask)
- **Posts Service** - Content creation, management, and interactions (Python/Flask)
- **Posts WebSocket Service** - Real-time post updates and notifications (Go)
- **JWT Generator Service** - Service-to-service authentication token generation (Rust)

### Infrastructure
- **Container Orchestration** - Kubernetes (K8s) with custom configurations
- **Infrastructure as Code** - Terraform for cloud resource provisioning
- **Message Queue** - RabbitMQ for asynchronous communication
- **Database** - PostgreSQL for persistent data storage
- **Cache** - Redis for session management and caching
- **Object Storage** - MinIO/S3 for media file storage

## 🎯 Key Features

- **Microservices Architecture** - Loosely coupled, independently deployable services
- **Real-time Communication** - WebSocket support for instant updates
- **Service Mesh** - Inter-service communication with JWT-based authentication
- **Cloud Native** - Containerized with Docker, orchestrated with Kubernetes
- **Infrastructure as Code** - Terraform modules for reproducible infrastructure
- **Message-Driven** - Event-driven architecture using RabbitMQ
- **Scalable Storage** - S3-compatible object storage for media files
- **High Performance** - Redis caching layer for optimized response times

## 🛠️ Technology Stack

### Backend Services
- **Python/Flask** - Core API services with SQLAlchemy ORM
- **Go** - High-performance WebSocket service
- **Rust** - Secure JWT token generation service

### Infrastructure & DevOps
- **Docker** - Containerization
- **Kubernetes** - Container orchestration
- **Terraform** - Infrastructure provisioning
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **RabbitMQ** - Message broker
- **MinIO** - Object storage

## 📁 Project Structure

```
.
├── services/
│   ├── auth/              # Authentication service (Python/Flask)
│   ├── user/              # User management service (Python/Flask)
│   ├── posts/             # Posts management service (Python/Flask)
│   ├── posts-websocket/   # Real-time updates service (Go)
│   └── jwt-generator/     # JWT token generation (Rust)
├── infra/
│   ├── k8s/              # Kubernetes configurations
│   │   ├── base/         # Base K8s resources
│   │   ├── services/     # Service-specific configurations
│   │   └── shared/       # Shared resources
│   └── terraform/        # Infrastructure as Code
│       ├── modules/      # Reusable Terraform modules
│       └── environments/ # Environment-specific configs
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (local or cloud)
- Terraform (for infrastructure provisioning)
- kubectl CLI tool
- Python 3.9+
- Go 1.19+
- Rust 1.70+ (Cargo)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Set up environment variables**
   
   Create `.env` files in each service directory with required configurations:
   - JWT_SECRET_KEY
   - DATABASE_URI
   - REDIS_URL
   - MINIO credentials
   - RabbitMQ connection strings

3. **Build and run services**
   ```bash
   # Build Docker images for all services
   docker compose build

   # Start all services
   docker compose up -d
   ```

4. **Initialize databases**
   ```bash
   # Database migrations will run automatically on service startup
   ```

### Kubernetes Deployment

1. **Provision infrastructure with Terraform**
   ```bash
   cd infra/terraform/environments/<environment>
   terraform init
   terraform plan
   terraform apply
   ```

2. **Deploy to Kubernetes**
   ```bash
   # Apply base configurations
   kubectl apply -k infra/k8s/base/

   # Deploy services
   kubectl apply -k infra/k8s/services/
   ```

3. **Verify deployment**
   ```bash
   kubectl get pods
   kubectl get services
   ```

## 🏛️ Architecture Decisions

### Microservices Pattern
Each service is independently deployable and scalable, following the single responsibility principle. Services communicate through well-defined APIs and message queues.

### Service-to-Service Authentication
The Rust-based JWT generator service runs as a Kubernetes init container, generating secure tokens for inter-service communication without exposing sensitive keys.

### Event-Driven Architecture
RabbitMQ enables asynchronous communication between services, particularly for real-time notifications when new posts are created.

### Polyglot Architecture
Different languages are chosen based on service requirements:
- Python for rapid development and rich ecosystem
- Go for high-performance concurrent operations
- Rust for security-critical token generation

## 📊 Scalability

- **Horizontal Scaling** - Services can be replicated across multiple pods
- **Database Replication** - PostgreSQL supports read replicas
- **Cache Layer** - Redis reduces database load
- **Message Queue** - Decouples services for better resilience
- **Object Storage** - S3-compatible storage scales independently

## 🔒 Security Features

- JWT-based authentication with secure token generation
- Service-to-service authentication using API tokens
- Kubernetes secrets management
- Environment-based configuration
- SQL injection protection through ORM

## 🧪 Testing

```bash
# Run tests for Python services
cd services/<service-name>
pytest

# Run tests for Go service
cd services/posts-websocket
go test ./...

# Run tests for Rust service
cd services/jwt-generator
cargo test
```

## 📈 Monitoring & Observability

The platform is designed to integrate with:
- Prometheus for metrics collection
- Grafana for visualization
- ELK stack for log aggregation
- Kubernetes health checks and readiness probes

## 🤝 Contributing

This project follows standard Git workflow practices:
1. Create a feature branch
2. Make your changes
3. Submit a pull request

## 📝 License

This project is available for portfolio demonstration purposes.

---

**Note**: This is a demonstration project showcasing microservices architecture, cloud-native deployment, and DevOps best practices.
