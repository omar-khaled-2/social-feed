# Posts Service

A Flask-based microservice handling content creation, management, media uploads, and social interactions (likes, comments) for the platform.

## 🎯 Purpose

This service manages all post-related operations including content creation, image uploads to object storage, like functionality, and post retrieval. It integrates with message queues for real-time notifications.

## 🛠️ Technology Stack

- **Framework**: Flask
- **Database ORM**: SQLAlchemy
- **Object Storage**: MinIO (S3-compatible)
- **Message Queue**: RabbitMQ
- **Authentication**: JWT validation
- **Database**: PostgreSQL
- **Language**: Python 3.9+

## 📋 Features

- Post creation with multi-image upload support
- S3-compatible object storage integration
- Like/unlike functionality
- Post retrieval and filtering
- Event publishing to message queue
- Image URL generation and management
- User post associations

## 🏗️ Architecture

```
posts/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── config.py                # Configuration management
│   ├── db.py                    # Database setup
│   ├── models/
│   │   ├── post.py             # Post data model
│   │   ├── likes.py            # Likes data model
│   │   └── user.py             # User reference model
│   ├── schemas/
│   │   ├── post.py             # Post schemas
│   │   └── user.py             # User schemas
│   ├── lib/
│   │   └── s3.py               # S3/MinIO client
│   └── controllers/
│       └── post_controller.py  # HTTP handlers
└── run.py                       # Application entry point
```

## 🔧 Configuration

The service requires the following environment variables:

```env
JWT_SECRET_KEY=<your-jwt-secret>
DATABASE_URI=postgresql://user:password@host:port/database
POST_IMAGES_BUCKET=<s3-bucket-name>
MINIO_ENDPOINT=<minio-endpoint>
MINIO_ACCESS_KEY=<access-key>
MINIO_SECRET_KEY=<secret-key>
AMQP_URI=amqp://user:password@host:port/
CREATED_POSTS_QUEUE_NAME=<queue-name>
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

3. **Ensure dependencies are running**
   - PostgreSQL
   - MinIO/S3
   - RabbitMQ

4. **Run the service**
   ```bash
   python run.py
   ```

### Docker

```bash
docker build -t posts-service .
docker run -p 5000:5000 --env-file .env posts-service
```

### Kubernetes

```bash
kubectl apply -f ../infra/k8s/services/posts/
```

## 🔒 Security Features

- JWT token validation for authenticated requests
- Secure S3 credential management
- Input validation and sanitization
- SQL injection protection through ORM
- Secure file upload handling

## 📊 Database Schema

The service manages:
- **Posts**: Content, descriptions, timestamps, owner references
- **Likes**: User-post relationships for likes
- **Image Keys**: S3 object keys associated with posts
- **Users**: Cached user data for performance

## 🎨 Image Handling

- Multi-image upload support per post
- Images stored in S3-compatible object storage (MinIO)
- Automatic URL generation for image retrieval
- Image keys stored in database for reference
- Efficient batch image processing

## 📨 Event-Driven Architecture

- Publishes post creation events to RabbitMQ
- Enables real-time notifications via WebSocket service
- Asynchronous message processing
- Decoupled service communication

## 🔄 Integration

This service integrates with:
- **Auth Service** - JWT token validation
- **User Service** - User information retrieval
- **Posts WebSocket Service** - Real-time post notifications via RabbitMQ
- **MinIO/S3** - Image storage
- **RabbitMQ** - Event publishing

## 🚀 Performance Optimizations

- Efficient database queries with joins
- Image upload processing
- Connection pooling for database and S3
- Async message queue publishing
- Optimized query patterns for post retrieval

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

- Stateless service design
- Horizontal scaling capability
- Object storage for media files (not in database)
- Message queue for async processing
- Database query optimization

## 🐛 Troubleshooting

**Issue**: Image upload fails
- Verify MinIO/S3 credentials
- Check bucket exists and is accessible
- Verify network connectivity to storage
- Check file size limits

**Issue**: Message queue connection fails
- Verify AMQP_URI is correct
- Check RabbitMQ is running
- Verify queue exists
- Check network connectivity

**Issue**: Slow post retrieval
- Review database indexes
- Check query patterns
- Monitor database connections
- Consider caching strategies

## 📊 Monitoring

Key metrics to monitor:
- Post creation rate
- Image upload success rate
- Database query performance
- Message queue publish rate
- Storage usage
- Error rates

## 🔮 Future Enhancements

- Video upload support
- Image compression and optimization
- Advanced post filtering and search
- Post analytics
- Content moderation

## 📝 Notes

This service demonstrates:
- Integration with object storage systems
- Event-driven architecture patterns
- Multi-resource management (database + storage + queue)
- Scalable media handling

Designed for deployment in a Kubernetes environment with proper secret management and service mesh configuration.
