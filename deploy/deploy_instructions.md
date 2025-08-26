# Deploy to Cloud Run
1. Set project and region:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud config set run/region us-central1
   ```
2. Build & push image:
   ```bash
   gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/tariff-impact-analysis
   ```
3. Deploy:
   ```bash
   gcloud run deploy tariff-impact-analysis --image gcr.io/$GOOGLE_CLOUD_PROJECT/tariff-impact-analysis --platform managed --allow-unauthenticated --set-env-vars NEO4J_URI=...,GCP_BUCKET=...
   ```
4. Monitor logs via Cloud Run console or `gcloud logging`.
