# Exit on error
set -e

# Ensure we deploy to the correct GCP project
gcloud config set project adaptivelearning-449114

echo "Building backend Docker image..."
docker build -t gcr.io/adaptivelearning-449114/adaptivelearning-backend ./backend

echo "Pushing backend image to Google Container Registry..."
docker push gcr.io/adaptivelearning-449114/adaptivelearning-backend

echo "Deploying backend to Google Cloud Run..."
gcloud run deploy adaptivelearning-backend \
  --project adaptivelearning-449114 \
  --image gcr.io/adaptivelearning-449114/adaptivelearning-backend \
  --min-instances=1 \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated

echo "Backend deployment complete!"

echo "Building Vue frontend..."
npm --prefix frontend run build

echo "Building Docker image..."
docker build -t gcr.io/adaptivelearning-449114/adaptivelearning-frontend ./frontend

echo "Pushing to Google Container Registry..."
docker push gcr.io/adaptivelearning-449114/adaptivelearning-frontend

echo "Deploying to Google Cloud Run..."
gcloud run deploy adaptivelearning-frontend \
  --project adaptivelearning-449114 \
  --image gcr.io/adaptivelearning-449114/adaptivelearning-frontend \
  --min-instances=1 \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated

echo "Deployment complete!"
