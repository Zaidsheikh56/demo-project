#!/usr/bin/env bash
# Builds the Angular app and syncs it to S3, then invalidates CloudFront.
#
# Prereqs: node/npm, aws cli configured, an S3 bucket + CloudFront
#   distribution already created (see deploy/s3-bucket-policy.json and
#   README.md for one-time setup).
#
# Usage: ./deploy-frontend-s3.sh <s3-bucket-name> <cloudfront-distribution-id>
set -euo pipefail

BUCKET="${1:?Usage: deploy-frontend-s3.sh <bucket-name> <cloudfront-distribution-id>}"
DIST_ID="${2:?cloudfront distribution id required}"

cd ../frontend

echo "==> Installing dependencies"
npm install

echo "==> Building Angular app (production)"
npm run build

echo "==> Syncing dist/ to s3://${BUCKET}"
aws s3 sync dist/shaadi-crm-frontend/browser "s3://${BUCKET}" --delete

echo "==> Invalidating CloudFront cache"
aws cloudfront create-invalidation --distribution-id "$DIST_ID" --paths "/*"

echo "==> Done. Frontend deployed to s3://${BUCKET}, served via CloudFront ${DIST_ID}"
