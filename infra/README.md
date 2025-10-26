# Infrastructure Configuration

This directory contains all infrastructure-as-code (IaC) configurations for deploying and managing the microservices platform.

## 📁 Structure

```
infra/
├── k8s/              # Kubernetes configurations
│   ├── base/         # Base Kubernetes resources
│   ├── services/     # Service-specific deployments
│   └── shared/       # Shared resources (ingress, etc.)
├── terraform/        # Infrastructure provisioning
│   ├── modules/      # Reusable Terraform modules
│   └── environments/ # Environment-specific configurations
└── deployment.yaml   # Example deployment configuration
```

## 🎯 Overview

The infrastructure is designed with the following principles:
- **Infrastructure as Code**: All infrastructure is version-controlled
- **Environment Parity**: Consistent configurations across environments
- **Modularity**: Reusable components and configurations
- **Scalability**: Support for horizontal scaling
- **Security**: Secrets management and network policies
- **Observability**: Built-in monitoring and logging support

## 🚀 Kubernetes (k8s/)

### Base Resources

Located in `k8s/base/`, these are foundational resources required by the platform:

- **Namespace**: Logical isolation for the application
- **PostgreSQL**: Stateful database deployment
- **Redis**: Caching and session storage
- **Secrets**: Encrypted configuration values
- **Ingress**: External traffic routing

### Service Deployments

Located in `k8s/services/`, each microservice has its own deployment configuration:

- Deployment specifications
- Service definitions
- ConfigMaps
- Resource limits and requests
- Health checks and readiness probes
- Horizontal Pod Autoscaling (HPA)

### Shared Resources

Located in `k8s/shared/`, these are platform-wide resources:

- Ingress controllers
- Network policies
- Service mesh configurations
- Monitoring stack

## 🏗️ Terraform (terraform/)

### Modules

Reusable Terraform modules for:
- VPC and networking
- Kubernetes cluster provisioning
- Database instances
- Object storage buckets
- Load balancers
- DNS configuration
- Monitoring and logging infrastructure

### Environments

Environment-specific configurations:
- Development
- Staging
- Production

Each environment has its own:
- Variable definitions
- State backend configuration
- Resource sizing
- Security policies

## 🚀 Deployment Guide

### Prerequisites

- `kubectl` CLI tool
- Access to Kubernetes cluster
- Terraform 1.0+
- Cloud provider CLI (if using cloud provider)

### Initial Setup with Terraform

1. **Navigate to desired environment**
   ```bash
   cd terraform/environments/<environment>
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Review planned changes**
   ```bash
   terraform plan
   ```

4. **Apply infrastructure**
   ```bash
   terraform apply
   ```

### Kubernetes Deployment

1. **Set up kubectl context**
   ```bash
   kubectl config use-context <your-cluster>
   ```

2. **Create namespace and base resources**
   ```bash
   kubectl apply -k k8s/base/
   ```

3. **Verify base resources**
   ```bash
   kubectl get all -n <namespace>
   ```

4. **Deploy services**
   ```bash
   kubectl apply -k k8s/services/
   ```

5. **Check deployment status**
   ```bash
   kubectl get pods -n <namespace>
   kubectl get services -n <namespace>
   ```

### Configuration Management

#### Secrets

Create Kubernetes secrets for sensitive data:

```bash
kubectl create secret generic jwt-secret \
  --from-literal=JWT_SECRET_KEY=your-secret-key \
  -n <namespace>

kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URI=postgresql://... \
  -n <namespace>
```

#### ConfigMaps

Create ConfigMaps for non-sensitive configuration:

```bash
kubectl create configmap app-config \
  --from-literal=ENVIRONMENT=production \
  --from-literal=LOG_LEVEL=info \
  -n <namespace>
```

## 🔧 Service Configuration

### Init Container Pattern

The platform uses init containers for secure token generation:

```yaml
initContainers:
  - name: jwt-generator
    image: jwt-generator:latest
    env:
      - name: SERVICE_NAME
        value: "service-name"
      - name: OUTPUT_PATH
        value: "/token/token.jwt"
    envFrom:
      - secretRef:
          name: jwt-secret
    volumeMounts:
      - name: token
        mountPath: /token
```

### Volume Sharing

Main containers access tokens via shared volumes:

```yaml
volumes:
  - name: token
    emptyDir: {}

containers:
  - name: main-service
    volumeMounts:
      - name: token
        mountPath: /token
        readOnly: true
```

## 📊 Resource Management

### Resource Requests and Limits

Each service should define:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Horizontal Pod Autoscaling

Configure HPA for automatic scaling:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: service-name
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## 🔒 Security Best Practices

1. **Secret Management**
   - Use Kubernetes secrets for sensitive data
   - Consider external secret management (Vault, AWS Secrets Manager)
   - Rotate secrets regularly

2. **Network Policies**
   - Implement network segmentation
   - Restrict inter-service communication
   - Define ingress and egress rules

3. **RBAC**
   - Use role-based access control
   - Apply principle of least privilege
   - Regular access audits

4. **Pod Security**
   - Run containers as non-root
   - Use read-only root filesystems where possible
   - Implement pod security policies

## 📈 Monitoring and Observability

### Health Checks

Configure liveness and readiness probes:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Logging

- Centralized logging with ELK stack or similar
- Structured logging in JSON format
- Log aggregation at cluster level

### Metrics

- Prometheus for metrics collection
- Grafana for visualization
- Custom application metrics
- Infrastructure metrics

## 🔄 CI/CD Integration

The infrastructure supports automated deployments:

1. **Build Phase**
   - Docker image builds
   - Image scanning
   - Tag with version/commit

2. **Test Phase**
   - Integration tests
   - Security scanning
   - Infrastructure validation

3. **Deploy Phase**
   - Terraform apply (infrastructure changes)
   - kubectl apply (service updates)
   - Rolling updates for zero-downtime

## 🐛 Troubleshooting

### Pod Not Starting

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -c <init-container-name> -n <namespace>
```

### Service Not Accessible

```bash
kubectl get svc -n <namespace>
kubectl describe svc <service-name> -n <namespace>
kubectl get endpoints <service-name> -n <namespace>
```

### Database Connection Issues

```bash
kubectl get pods -l app=postgres -n <namespace>
kubectl exec -it <pod-name> -n <namespace> -- psql -U <user>
```

### Resource Constraints

```bash
kubectl top nodes
kubectl top pods -n <namespace>
kubectl describe node <node-name>
```

## 📊 Scaling Operations

### Manual Scaling

```bash
kubectl scale deployment <deployment-name> --replicas=5 -n <namespace>
```

### Cluster Scaling

- Modify Terraform configuration for node count
- Apply changes with `terraform apply`
- Kubernetes will redistribute pods

## 🔄 Updates and Rollbacks

### Rolling Update

```bash
kubectl set image deployment/<deployment-name> \
  <container-name>=<new-image> -n <namespace>
```

### Rollback

```bash
kubectl rollout undo deployment/<deployment-name> -n <namespace>
kubectl rollout history deployment/<deployment-name> -n <namespace>
```

## 📝 Best Practices

1. **Version Control**: All infrastructure code in Git
2. **State Management**: Use remote state for Terraform
3. **Environment Isolation**: Separate namespaces/clusters per environment
4. **Documentation**: Keep infrastructure documentation updated
5. **Testing**: Test infrastructure changes in non-production first
6. **Backup**: Regular backups of stateful resources
7. **Monitoring**: Comprehensive monitoring of all components
8. **Security**: Regular security audits and updates

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Terraform Documentation](https://www.terraform.io/docs/)
- [Container Best Practices](https://cloud.google.com/architecture/best-practices-for-building-containers)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)

## 🔮 Future Enhancements

- Service mesh implementation (Istio/Linkerd)
- Advanced monitoring with distributed tracing
- GitOps workflow (ArgoCD/Flux)
- Multi-cluster deployment
- Disaster recovery automation
- Cost optimization strategies
