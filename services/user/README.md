# User Service

A Flask-based microservice responsible for user profile management, user data operations, and user-related business logic.

## 🎯 Purpose

This service manages all user-related operations including profile creation, updates, retrieval, and user data management. It serves as the central user data repository for the platform.

## 🛠️ Technology Stack

- **Framework**: Flask
- **Database ORM**: SQLAlchemy
- **Cache**: Redis
- **Authentication**: JWT validation
- **Database**: PostgreSQL
- **Language**: Python 3.9+

## 📋 Features

- User profile management (CRUD operations)
- User data validation and sanitization
- Caching layer for improved performance
- JWT-based authentication
- Service-to-service API token validation
- RESTful API design

## 🏗️ Architecture

```
user/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── config.py                # Configuration management
│   ├── db.py                    # Database setup
│   ├── utils.py                 # Utility functions
│   ├── models/
│   │   └── user.py             # User data model
│   ├── schemas/
│   │   └── user_schema.py      # Request/response schemas
│   ├── services/
│   │   └── user_service.py     # Business logic
│   └── controllers/
│       └── user_controller.py  # HTTP handlers
└── run.py                       # Application entry point
```

## 🔧 Configuration

The service requires the following environment variables:

```env
JWT_SECRET_KEY=<your-jwt-secret>
DATABASE_URI=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/db
ALLOWED_API_TOKENS=token1,token2,token3
PORT=<service-port>
DEBUG=False
```

## 🚀 Running the Service

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the service**
   ```bash
   python run.py
   ```

### Docker

```bash
docker build -t user-service .
docker run -p 5000:5000 --env-file .env user-service
```

### Kubernetes

```bash
kubectl apply -f ../infra/k8s/services/user/
```

## 🔒 Security Features

- JWT token validation for user requests
- API token validation for service-to-service calls
- Input validation using schemas
- SQL injection protection through ORM
- Secure data access patterns

## 📊 Database Schema

The service manages user data with comprehensive profile information:
- User identification and credentials
- Profile information
- User metadata and timestamps
- Relationship data

## 🚀 Performance Optimizations

- **Redis Caching** - Frequently accessed user data is cached
- **Connection Pooling** - Efficient database connection management
- **Query Optimization** - Indexed queries and efficient data retrieval
- **Stateless Design** - Enables horizontal scaling

## 🔄 Integration

This service integrates with:
- **Auth Service** - Validates JWT tokens
- **Posts Service** - Provides user information for posts
- **Other Services** - Central user data repository

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run integration tests
pytest tests/integration/
```

## 📈 Scalability

- Stateless service design allows horizontal scaling
- Redis cache reduces database load
- Connection pooling for efficient resource usage
- Can be replicated across multiple pods in Kubernetes

## 🐛 Troubleshooting

**Issue**: Redis connection fails
- Verify REDIS_URL is correct
- Check if Redis server is running
- Test network connectivity

**Issue**: Database queries are slow
- Check database indexes
- Review query patterns
- Monitor connection pool usage

**Issue**: Cache inconsistency
- Verify cache invalidation logic
- Check Redis memory limits
- Review cache TTL settings

## 📊 Monitoring

Key metrics to monitor:
- Request latency
- Cache hit/miss ratio
- Database query performance
- Error rates
- Active connections

## 📝 Notes

This service is designed as part of a microservices architecture and should be deployed with proper service discovery, health checks, and monitoring in place.
