# Posts WebSocket Service

A high-performance Go-based WebSocket service providing real-time post updates and notifications to connected clients.

## 🎯 Purpose

This service handles real-time communication with clients, broadcasting new post notifications instantly when posts are created. It consumes messages from RabbitMQ and pushes updates to WebSocket-connected clients.

## 🛠️ Technology Stack

- **Language**: Go 1.19+
- **WebSocket**: Native Go WebSocket implementation
- **Message Queue**: RabbitMQ (AMQP)
- **Database**: PostgreSQL (read operations)
- **Driver**: pq (PostgreSQL driver)

## 📋 Features

- Real-time WebSocket connections
- RabbitMQ message consumption
- Live post broadcasting to connected clients
- Concurrent connection handling
- Efficient message distribution
- Database integration for post data enrichment

## 🏗️ Architecture

```
posts-websocket/
├── main.go           # Main application and message consumer
├── websocket.go      # WebSocket connection management
├── go.mod            # Go module dependencies
├── go.sum            # Dependency checksums
├── Dockerfile        # Container image definition
└── .env              # Environment configuration
```

## 🔧 Configuration

The service requires the following environment variables:

```env
AMQP_URL=amqp://user:password@host:port/
QUEUE_NAME=<rabbitmq-queue-name>
DATABASE_URL=postgresql://user:password@host:port/database
```

Create a `.env` file with your configuration values.

## 🚀 Running the Service

### Local Development

1. **Install dependencies**
   ```bash
   go mod download
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Ensure dependencies are running**
   - PostgreSQL
   - RabbitMQ

4. **Run the service**
   ```bash
   go run .
   ```

The service will start on port `8080` by default.

### Docker

```bash
docker build -t posts-websocket-service .
docker run -p 8080:8080 --env-file .env posts-websocket-service
```

### Kubernetes

```bash
kubectl apply -f ../infra/k8s/services/posts-websocket/
```

## 🔌 WebSocket Connection

Clients can connect to the WebSocket endpoint:

```
ws://host:8080/
```

### Message Format

Messages are broadcast in JSON format:

```json
{
  "action": "created",
  "payload": {
    "id": 123,
    "description": "Post content",
    "created_at": "2024-01-01T00:00:00Z",
    "user": {
      "id": 456,
      "username": "username"
    },
    "is_liked": false,
    "image_urls": ["url1", "url2"],
    "likes_count": 0
  }
}
```

## 🏗️ System Flow

1. **Message Reception**: Service consumes messages from RabbitMQ queue
2. **Data Enrichment**: Queries PostgreSQL for complete post data
3. **Broadcasting**: Sends enriched post data to all connected WebSocket clients
4. **Periodic Processing**: Processes messages every 5 seconds in batches

## 🚀 Performance Features

- **Concurrent Connections**: Handles multiple WebSocket connections simultaneously
- **Efficient Goroutines**: Separate goroutines for HTTP server, message consumption, and broadcasting
- **Connection Pooling**: Database connection pooling for optimal performance
- **Message Buffering**: Channel-based buffering for smooth message flow
- **Batch Processing**: Periodic message processing to optimize throughput

## 🔄 Integration

This service integrates with:
- **Posts Service** - Receives post creation events via RabbitMQ
- **PostgreSQL** - Retrieves complete post data with joins
- **WebSocket Clients** - Frontend applications, mobile apps

## 🧪 Testing

```bash
# Run tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Run tests with race detection
go test -race ./...
```

## 📊 Connection Management

- Maintains registry of active WebSocket connections
- Handles connection upgrades from HTTP
- Graceful connection cleanup on client disconnect
- Broadcast to all connected clients simultaneously

## 🐛 Troubleshooting

**Issue**: WebSocket connection refused
- Verify service is running on port 8080
- Check firewall rules
- Ensure proper CORS configuration

**Issue**: No messages received
- Verify RabbitMQ connection
- Check queue name configuration
- Ensure posts service is publishing messages

**Issue**: Database query fails
- Verify DATABASE_URL is correct
- Check database connectivity
- Ensure required tables exist

**Issue**: High memory usage
- Monitor number of concurrent connections
- Check message buffer size
- Review goroutine leaks

## 📈 Scalability

- Horizontal scaling supported with load balancer
- Stateless design (no session storage)
- Efficient goroutine-based concurrency
- Connection handling optimized for high throughput

## 📊 Monitoring

Key metrics to monitor:
- Active WebSocket connections
- Message processing rate
- Database query latency
- RabbitMQ queue depth
- Goroutine count
- Memory usage

## 🔮 Future Enhancements

- User-specific message filtering
- Message persistence for offline clients
- Connection authentication
- Rate limiting per connection
- Message acknowledgment
- Compression for large payloads

## 📝 Notes

This service demonstrates:
- Real-time communication patterns
- Event-driven architecture
- Go concurrency patterns
- Integration of WebSocket, message queue, and database

The Go language was chosen for this service due to its excellent concurrency support, high performance, and efficient WebSocket handling capabilities.
