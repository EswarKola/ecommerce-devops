# CloudCart E-Commerce DevOps Starter

Sample app: React/Vite frontend served by Nginx, Flask API, and PostgreSQL on Amazon RDS.

## AWS prerequisites
1. Create ECR repositories named `ecommerce-frontend` and `ecommerce-backend`.
2. Create an EKS cluster and configure Jenkins IAM access to ECR and EKS.
3. Create RDS PostgreSQL in private subnets. Allow TCP/5432 only from the backend's security group/network path.
4. Create a Kubernetes secret in namespace `ecommerce` with keys `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.
5. Create Jenkins string credentials `aws-account-id` and `db-host`. `db-host` is the RDS endpoint hostname only.
6. Install/configure AWS CLI, Docker, kubectl, Python 3, Node.js/npm on the Jenkins agent. Prefer an EC2 instance profile over long-lived AWS access keys.
7. Change `AWS_REGION` and `EKS_CLUSTER_NAME` in `Jenkinsfile`. This sample deploys only when the branch is `main`.

## PostgreSQL setup
Apply `database/schema.sql` once to the RDS database using an approved, secure SQL client/migration process. Never put passwords in Git. The backend expects this schema to exist.

## Kubernetes secret example
After creating the `ecommerce` namespace, create the secret interactively or through a secrets manager integration. Example command (avoid typing a real password into shell history):
`kubectl create secret generic ecommerce-db-secret -n ecommerce --from-literal=DB_NAME=ecommerce --from-literal=DB_USER=ecommerce_user --from-literal=DB_PASSWORD='REPLACE_WITH_SECRET'`

Kubernetes Secrets are not automatically a full secrets-management solution. Restrict RBAC, enable EKS secret encryption, and consider AWS Secrets Manager with the Secrets Store CSI Driver for production.

## Important notes
- The Jenkins pipeline stops before image publishing/deployment if backend tests or frontend build fail.
- This starter is for learning and needs environment-specific review before use.
- Ensure the Jenkins IAM role is authorized in EKS and has least-privilege ECR push permissions.
- The optional `k8s/frontend-loadbalancer.yaml` creates a billable AWS load balancer; apply it only when ready to expose the site. Production should use HTTPS/TLS, normally with an ALB and certificate.
- `sslmode=require` encrypts DB traffic but does not fully verify server identity. Production should use CA validation with `verify-full`.
- Set up CloudWatch logging/alarms, image scanning, resource quotas, network policies, tested rollback, and autoscaling before production.
- For local development, install dependencies in `backend/` and run tests with `pytest -q`; build the frontend with `cd frontend && npm install && npm run build`.
