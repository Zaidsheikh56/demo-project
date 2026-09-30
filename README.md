# Shaadi CRM

Customer management app for a wedding-planning business: track leads/clients,
their event details (type, date, venue, budget), payments received, and notes.

- **Frontend:** Angular 18 (standalone components)
- **Backend:** Python (FastAPI) + SQLAlchemy + Alembic
- **Database:** PostgreSQL
- **Deploy target:** Backend + Postgres on Kubernetes (EKS); Angular on AWS S3 + CloudFront

```
shaadi-crm/
├── backend/          FastAPI app, models, Alembic migrations
├── frontend/          Angular app
├── k8s/               Kubernetes manifests (namespace, postgres, backend, ingress)
├── deploy/            Deployment scripts for ECR/EKS and S3/CloudFront
└── docker-compose.yml Local dev environment
```

## 1. Local development

```bash
# Backend + Postgres
docker compose up --build
# API available at http://localhost:8000, docs at http://localhost:8000/docs

# Frontend (separate terminal)
cd frontend
npm install
npm start
# App available at http://localhost:4200
```

The frontend's `environment.ts` already points at `http://localhost:8000/api/v1`.

## 2. Backend + Postgres → Kubernetes (EKS)

One-time setup:
1. Create an EKS cluster (via `eksctl` or the console) with a node group and a
   default `gp3` StorageClass.
2. Install the [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/)
   if you want the Ingress in `24-backend-ingress.yaml` to provision an ALB.
3. Request/import an ACM certificate for your API domain and put its ARN in
   `k8s/24-backend-ingress.yaml`.
4. Edit `k8s/10-postgres-secret.yaml` and `k8s/20-backend-secret.yaml` with a
   real password (or, better, create the secrets imperatively with `kubectl
   create secret` instead of committing them).
5. Point `k8s/21-backend-configmap.yaml`'s `CORS_ORIGINS` at your CloudFront
   domain.

Every deploy after that:

```bash
cd deploy
./build-push-ecr.sh <aws-account-id> <region> <eks-cluster-name>
```

This builds the backend image, pushes it to ECR, applies all manifests, runs
the Alembic migration as a Kubernetes Job, then rolls the backend Deployment.

Check status:
```bash
kubectl get pods -n shaadi-crm
kubectl get ingress -n shaadi-crm   # shows the ALB hostname
```

## 3. Angular frontend → AWS S3 + CloudFront

One-time setup:
1. Create an S3 bucket (block all public access — CloudFront will read via
   Origin Access Control, not a public bucket policy).
2. Create a CloudFront distribution with that bucket as origin (S3 origin
   type, Origin Access Control), default root object `index.html`, and a
   custom error response mapping 403/404 → `/index.html` (200) so Angular's
   client-side routing works on refresh/deep links.
3. Apply `deploy/s3-bucket-policy.json` to the bucket after filling in your
   bucket name, account id, and distribution id.
4. Before building, update `frontend/src/environments/environment.prod.ts`
   with your real API domain (the ALB/Ingress hostname from step 2 above).

Every deploy after that:

```bash
cd deploy
./deploy-frontend-s3.sh <s3-bucket-name> <cloudfront-distribution-id>
```

## 4. Environment variables reference

**Backend** (`backend/.env` locally, or the `backend-secret` / `backend-config`
K8s objects in production):

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy connection string to Postgres |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins |
| `ENVIRONMENT` | `development` / `production` |

**Frontend** (`src/environments/*.ts`, baked in at build time):

| File | Purpose |
|---|---|
| `environment.ts` | Used by `ng serve` (local dev) |
| `environment.prod.ts` | Used by `ng build --configuration production` |

## 5. API summary

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/customers` | List customers (`?search=&status=`) |
| POST | `/api/v1/customers` | Create customer |
| GET | `/api/v1/customers/{id}` | Get customer + payments + notes |
| PUT | `/api/v1/customers/{id}` | Update customer |
| DELETE | `/api/v1/customers/{id}` | Delete customer |
| POST | `/api/v1/customers/{id}/payments` | Record a payment |
| POST | `/api/v1/customers/{id}/notes` | Add a note |
| GET | `/health` | Health check |

Full interactive docs at `/docs` (Swagger) once the backend is running.

## 6. What's not included (add before real production use)

- Authentication/authorization (currently the API is open — add JWT/OAuth
  before exposing it publicly)
- Rate limiting and request logging/observability
- Automated tests
- CI/CD pipeline (the `deploy/` scripts are manual-run; wire them into
  GitHub Actions/CodePipeline when ready)
