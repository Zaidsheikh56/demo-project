#!/usr/bin/env bash
# Builds the backend Docker image, pushes it to ECR, applies the migration
# Job, then rolls out the backend Deployment on EKS.
#
# Prereqs: aws cli configured, docker, kubectl pointed at your EKS cluster
#   (aws eks update-kubeconfig --name <cluster-name> --region <region>)
#
# Usage: ./build-push-ecr.sh <aws-account-id> <region> <cluster-name> [tag]
set -euo pipefail

ACCOUNT_ID="${1:?Usage: build-push-ecr.sh <account-id> <region> <cluster-name> [tag]}"
REGION="${2:?region required}"
CLUSTER_NAME="${3:?cluster name required}"
TAG="${4:-latest}"

REPO_NAME="shaadi-crm-backend"
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}"

echo "==> Ensuring ECR repo exists"
aws ecr describe-repositories --repository-names "$REPO_NAME" --region "$REGION" \
  >/dev/null 2>&1 || aws ecr create-repository --repository-name "$REPO_NAME" --region "$REGION"

echo "==> Logging in to ECR"
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

echo "==> Building backend image"
docker build -t "${ECR_URI}:${TAG}" ../backend

echo "==> Pushing image"
docker push "${ECR_URI}:${TAG}"

echo "==> Pointing kubectl at cluster ${CLUSTER_NAME}"
aws eks update-kubeconfig --name "$CLUSTER_NAME" --region "$REGION"

echo "==> Applying base manifests (namespace, secrets, configmaps, postgres)"
kubectl apply -f ../k8s/00-namespace.yaml
kubectl apply -f ../k8s/10-postgres-secret.yaml
kubectl apply -f ../k8s/11-postgres-pvc.yaml
kubectl apply -f ../k8s/12-postgres-deployment.yaml
kubectl apply -f ../k8s/13-postgres-service.yaml
kubectl apply -f ../k8s/21-backend-configmap.yaml
kubectl apply -f ../k8s/20-backend-secret.yaml

echo "==> Substituting image URI into deployment/migration manifests"
sed "s#<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/shaadi-crm-backend:latest#${ECR_URI}:${TAG}#" \
  ../k8s/22-backend-deployment.yaml | kubectl apply -f -
sed "s#<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/shaadi-crm-backend:latest#${ECR_URI}:${TAG}#" \
  ../k8s/25-migration-job.yaml > /tmp/migration-job.yaml
kubectl delete job db-migrate -n shaadi-crm --ignore-not-found
kubectl apply -f /tmp/migration-job.yaml
kubectl wait --for=condition=complete job/db-migrate -n shaadi-crm --timeout=180s

kubectl apply -f ../k8s/23-backend-service.yaml
kubectl apply -f ../k8s/24-backend-ingress.yaml

echo "==> Rolling out backend"
kubectl rollout restart deployment/backend -n shaadi-crm
kubectl rollout status deployment/backend -n shaadi-crm

echo "==> Done. Backend image: ${ECR_URI}:${TAG}"
