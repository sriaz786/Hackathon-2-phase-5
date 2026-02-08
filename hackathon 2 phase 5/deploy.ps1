# deploy.ps1
Write-Host "Starting Phase 5 Deployment to Minikube..." -ForegroundColor Green

# 1. Check Minikube Status
$minikubeStatus = minikube status --format='{{.Host}}'
if ($minikubeStatus -ne "Running") {
    Write-Host "Minikube is not running. Attempting to start..." -ForegroundColor Yellow
    minikube start --cpus 4 --memory 3072

    Write-Host "Minikube Started." -ForegroundColor Green
}

# 1.1 Enable Ingress Addon (Critical for app.local)
Write-Host "Enabling Ingress Controller..."
minikube addons enable ingress

# 2. Configure Docker Environment
Write-Host "Configuring Docker environment..."
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# 3. Build Images
Write-Host "Building Backend Image..." -ForegroundColor Cyan
docker build -t backend:v1 ./backend

Write-Host "Building Frontend Image..." -ForegroundColor Cyan
docker build -t frontend:v1 ./frontend

# 4. Initialize Dapr on Kubernetes
Write-Host "Initializing Dapr on Kubernetes..." -ForegroundColor Cyan
dapr init -k

# 5. Infrastructure Deployment
Write-Host "Deploying Infrastructure (Redpanda, Postgres)..." -ForegroundColor Cyan
kubectl apply -f k8s/redpanda.yaml
kubectl apply -f k8s/postgres.yaml

# Wait for infrastructure (basic sleep, better would be kubectl wait)
Write-Host "Waiting for infrastructure to startup (30s)..."
Start-Sleep -Seconds 30

# 6. Apply Dapr Components
Write-Host "Deploying Dapr Components..." -ForegroundColor Cyan
kubectl apply -f k8s/components/pubsub.yaml
kubectl apply -f k8s/components/statestore.yaml
kubectl apply -f k8s/components/binding.yaml

Write-Host "Deploying Application Manifests..." -ForegroundColor Cyan
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "Verify with: kubectl get pods"
Write-Host "Access at: http://app.local (Ensure 'minikube ip' is added to hosts file)"
