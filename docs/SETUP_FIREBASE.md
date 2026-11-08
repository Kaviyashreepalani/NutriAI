# Setting up NutriAI with Firebase (Configuration B / C)

This guide walks you through setting up NutriAI with Firebase for Authentication and optional Firebase Storage, while maintaining PostgreSQL for relational clinical data.

---

## 1. Create a Firebase Project
1. Visit the [Firebase Console](https://console.firebase.google.com/).
2. Click **Add project**, name it `nutriai-app`.
3. Enable **Firebase Authentication**:
   - Go to **Build** -> **Authentication** -> **Get Started**.
   - Under **Sign-in method**, enable **Email/Password**.

---

## 2. Obtain Firebase Admin SDK Service Account
1. In Firebase Console, go to **Project Settings** (gear icon) -> **Service accounts**.
2. Select **Python**, and click **Generate new private key**.
3. Save the JSON file securely (e.g. `backend/firebase-service-account.json` - ensure it is in `.gitignore`).
4. Alternatively, encode the JSON as a single-line string for environment deployment.

---

## 3. Configure Environment Variables
In `.env`:
```env
AUTH_PROVIDER=firebase
FIREBASE_PROJECT_ID=nutriai-app
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
# Or inline JSON:
# FIREBASE_SERVICE_ACCOUNT_JSON={"type": "service_account", ...}

# If using Firebase Storage (Config C):
STORAGE_PROVIDER=firebase
FIREBASE_STORAGE_BUCKET=nutriai-app.appspot.com
```

---

## 4. Firebase Storage Security Rules
If using Firebase Storage for report uploads, apply the following rules:
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /reports/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId
                         && request.resource.size < 10 * 1024 * 1024
                         && request.resource.contentType.matches('application/pdf|image/(jpeg|png)');
    }
  }
}
```
> **Note**: Clinical lab values, assessments, orders, and formulations are strictly stored in PostgreSQL, never in Firestore.

