# Authentication Service

A Flask-based authentication service providing JWT token generation, validation, and user authentication for the microservices platform.

## 🎯 Purpose

This service handles all authentication-related operations, including user login, token generation, and token validation. It serves as the entry point for user authentication in the platform.

## 🛠️ Technology Stack

- **Framework**: Flask
- **Database ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL
- **Language**: Python 3.9+

## 📋 Features

- User authentication with JWT tokens
- Token generation and validation
- Secure password handling
- Session management
- User credential verification

## 🏗️ Architecture

```
auth/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── config.py             # Configuration management
│   ├── db.py                 # Database setup
│   ├── models/
│   │   └── user.py          # User data model
│   └── controllers/
│       └── auth_controller.py # Authentication logic
└── run.py                    # Application entry point
```

## 🔧 Configuration

The service requires the following environment variables:

```env
JWT_SECRET_KEY=<your-jwt-secret>
DATABASE_URI=postgresql://user:password@host:port/database
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
docker build -t auth-service .
docker run -p 5000:5000 --env-file .env auth-service
```

### Kubernetes

```bash
kubectl apply -f ../infra/k8s/services/auth/
```

## 🔒 Security Considerations

- JWT tokens are signed with a secure secret key
- Passwords are never stored in plain text
- Token expiration is enforced
- Secure communication between services
- Input validation on all endpoints

## 📊 Database Schema

The service manages user authentication data with the following key entities:
- User credentials
- Authentication timestamps
- Token metadata

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

## 🔄 Integration

This service integrates with:
- **User Service** - Retrieves user profile information
- **All Services** - Provides authentication tokens for API access

## 📈 Performance

- Stateless authentication using JWT
- No session storage required
- Horizontal scaling capability
- Efficient database queries with SQLAlchemy

## 🐛 Troubleshooting

**Issue**: Database connection fails
- Verify DATABASE_URI is correct
- Check if PostgreSQL is running
- Ensure network connectivity

**Issue**: JWT validation fails
- Verify JWT_SECRET_KEY matches across services
- Check token expiration time
- Validate token format

## 📝 Notes

This service is designed to be deployed as part of a Kubernetes cluster with proper secret management and service mesh configuration.
