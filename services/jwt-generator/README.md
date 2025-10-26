# JWT Generator Service

A lightweight, security-focused Rust service for generating JWT tokens used in service-to-service authentication within the microservices architecture.

## 🎯 Purpose

This service generates JWT tokens for inter-service communication. It runs as a Kubernetes init container, creating authentication tokens before main services start, enabling secure service-to-service authentication without exposing secret keys to application containers.

## 🛠️ Technology Stack

- **Language**: Rust (Edition 2024)
- **JWT Library**: jsonwebtoken 8.x
- **Serialization**: Serde 1.0
- **Time Management**: Chrono 0.4

## 📋 Features

- Fast and secure JWT token generation
- Minimal resource footprint
- Command-line interface
- File-based output for init container usage
- Configurable token claims
- High security through Rust's memory safety

## 🏗️ Architecture

```
jwt-generator/
├── src/
│   └── main.rs       # Main application logic
├── Cargo.toml        # Rust dependencies and metadata
├── Cargo.lock        # Dependency lock file
├── Dockerfile        # Container image definition
└── target/           # Build artifacts
```

## 🔧 Configuration

The service accepts the following environment variables:

```env
SERVICE_NAME=<name-of-service-requesting-token>
OUTPUT_PATH=<path-to-write-token-file>
JWT_SECRET_KEY=<secret-key-for-signing>
```

### Command Line Usage

```bash
jwt-generator --service-name <name> --output-path <path>
```

## 🚀 Running the Service

### Local Development

1. **Install Rust**
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

2. **Build the project**
   ```bash
   cargo build --release
   ```

3. **Run the binary**
   ```bash
   JWT_SECRET_KEY=your-secret cargo run -- --service-name myservice --output-path /tmp/token.jwt
   ```

### Docker

```bash
docker build -t jwt-generator .
docker run -e JWT_SECRET_KEY=secret -e SERVICE_NAME=myservice -e OUTPUT_PATH=/token/token.jwt jwt-generator
```

### Kubernetes Init Container

This is the primary use case for this service:

```yaml
initContainers:
  - name: jwt-generator
    image: jwt-generator:latest
    env:
      - name: SERVICE_NAME
        value: "my-service"
      - name: OUTPUT_PATH
        value: "/token/token.jwt"
    envFrom:
      - secretRef:
          name: jwt-secret
    volumeMounts:
      - name: token
        mountPath: /token
```

The main container can then read the token from the shared volume.

## 🔒 Security Features

- **Memory Safety**: Rust's ownership system prevents memory vulnerabilities
- **No Runtime**: Compiled binary with minimal attack surface
- **Ephemeral Execution**: Runs once and exits, no persistent process
- **Secret Isolation**: JWT secret never persists in main application containers
- **Secure Token Storage**: Token written to ephemeral volume, not environment variables

## 🎯 Use Case: Init Container Pattern

### Problem Solved
- Prevents exposing JWT secret keys to application containers
- Generates tokens on-demand during pod initialization
- Keeps secrets isolated in Kubernetes secret store
- Main applications only receive pre-generated tokens

### Flow
1. Pod starts with init container running jwt-generator
2. Init container reads JWT_SECRET_KEY from Kubernetes secret
3. Generates token and writes to shared volume
4. Init container exits
5. Main container starts with access to generated token
6. JWT_SECRET_KEY never exposed to main container

## 📊 Token Structure

Generated tokens include standard JWT claims:
- `iss` (Issuer): Identifies the token generator
- `sub` (Subject): Service name requesting the token
- `iat` (Issued At): Token generation timestamp
- `exp` (Expiration): Token expiration time

## 🚀 Performance

- **Startup Time**: <100ms typical execution
- **Memory Usage**: ~2-5MB runtime memory
- **Binary Size**: Small footprint (~5-10MB)
- **CPU Usage**: Minimal, single-threaded execution

## 🧪 Testing

```bash
# Run unit tests
cargo test

# Run tests with output
cargo test -- --nocapture

# Run with coverage
cargo tarpaulin --out Html
```

## 🔄 Integration

This service integrates with:
- **Kubernetes** - Runs as init container
- **All Microservices** - Provides authentication tokens
- **Kubernetes Secrets** - Reads JWT secret key

## 🐛 Troubleshooting

**Issue**: Init container fails to start
- Verify JWT_SECRET_KEY is present in secret
- Check volume mount configuration
- Review pod logs: `kubectl logs <pod-name> -c jwt-generator`

**Issue**: Token file not found in main container
- Verify volume mount paths match
- Check init container completed successfully
- Ensure OUTPUT_PATH is correct

**Issue**: Token validation fails
- Verify JWT_SECRET_KEY matches across services
- Check token expiration time
- Validate token format and claims

## 📈 Benefits of Rust

- **Performance**: Compiled to native code, near-C performance
- **Safety**: Memory safety without garbage collection
- **Reliability**: Strong type system catches errors at compile time
- **Security**: Prevents common vulnerabilities like buffer overflows
- **Size**: Small binary size ideal for containers

## 🔮 Future Enhancements

- Support for multiple signing algorithms
- Configurable token expiration
- Token refresh mechanism
- Support for additional JWT claims
- Token validation endpoint

## 📝 Notes

This service demonstrates:
- Rust for security-critical operations
- Kubernetes init container pattern
- Secret management best practices
- Separation of concerns in security

The Rust language was chosen for this service due to its:
- Superior memory safety guarantees
- Zero-cost abstractions
- Minimal runtime overhead
- Strong cryptographic library support
- Security-first design philosophy

## 📚 Dependencies

```toml
[dependencies]
jsonwebtoken = "8"                        # JWT creation and validation
serde = { version = "1.0", features = ["derive"] }  # Serialization
chrono = "0.4"                            # Timestamp handling
```

All dependencies are carefully selected for security, performance, and minimal footprint.
