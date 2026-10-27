# 🚀 Automated CI/CD Pipeline — DevOps Project

A complete beginner-to-intermediate DevOps project demonstrating a fully automated
CI/CD pipeline using **GitHub Actions**, **Docker**, and **Docker Hub**.

Every time you push code to `main`, the pipeline automatically:
1. ✅ Runs all tests
2. 🐳 Builds a Docker image
3. 📦 Pushes the image to Docker Hub
4. 🌐 Deploys the application

---

## 📐 Architecture

```
Developer writes code
        │
        ▼
  git push → GitHub
        │
        ▼
 GitHub Actions triggers
        │
   ┌────┴─────────────────────────────────────┐
   │                                          │
   ▼                                          │
JOB 1: 🧪 Run Tests                          │
   pytest tests/ -v                           │
   │                                          │
   │  (if tests pass AND branch = main)       │
   ▼                                          │
JOB 2: 🐳 Build & Push Docker Image          │
   docker build → push to Docker Hub          │
   │                                          │
   ▼                                          │
JOB 3: 🚀 Deploy                             │
   docker pull → docker compose up -d         │
   │                                          │
   └──────────────────────────────────────────┘
        │
        ▼
  Application is live 🌐
```

---

## 🗂️ Project Structure

```
Devops_project/
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── main.py            # Entry point (dev server / gunicorn target)
│   └── routes.py          # GET / and GET /health endpoints
├── tests/
│   ├── __init__.py
│   └── test_app.py        # pytest unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # ← The CI/CD pipeline definition
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Orchestration for local dev & deployment
├── requirements.txt       # Python dependencies
├── .dockerignore
├── .gitignore
└── README.md
```

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.11+
- Docker Desktop (optional, for local container testing)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/devops-demo-app.git
cd devops-demo-app
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application locally
```bash
python app/main.py
```
Open your browser at **http://localhost:5000**

### 5. Run tests locally
```bash
pytest tests/ -v
```

Expected output:
```
tests/test_app.py::TestHomePage::test_home_returns_200        PASSED
tests/test_app.py::TestHomePage::test_home_returns_html       PASSED
tests/test_app.py::TestHomePage::test_home_contains_title     PASSED
tests/test_app.py::TestHomePage::test_home_contains_pipeline_steps PASSED
tests/test_app.py::TestHealthEndpoint::test_health_returns_200     PASSED
tests/test_app.py::TestHealthEndpoint::test_health_returns_json    PASSED
tests/test_app.py::TestHealthEndpoint::test_health_status_ok       PASSED
tests/test_app.py::TestHealthEndpoint::test_health_contains_service_name PASSED
tests/test_app.py::TestNotFound::test_unknown_route_returns_404    PASSED

9 passed in 0.XXs
```

---

## 🐳 Docker — Local Build & Run

```bash
# Build the image
docker build -t devops-demo-app .

# Run the container
docker run -p 5000:5000 devops-demo-app

# Or use Docker Compose (recommended)
docker compose up --build
```

---

## ⚙️ Setting Up the CI/CD Pipeline

### Step 1 — Create a GitHub Repository
Push this project to a new GitHub repository:
```bash
git init
git add .
git commit -m "Initial commit: Add Flask app, tests, Docker, and CI/CD workflow"
git remote add origin https://github.com/<your-username>/devops-demo-app.git
git branch -M main
git push -u origin main
```

### Step 2 — Create a Docker Hub Access Token
1. Log in to [hub.docker.com](https://hub.docker.com)
2. Go to **Account Settings → Security → New Access Token**
3. Give it a name like `github-actions` and copy the token

### Step 3 — Add GitHub Secrets
In your GitHub repository:
1. Go to **Settings → Secrets and variables → Actions → New repository secret**
2. Add these two secrets:

| Secret Name          | Value                            |
|----------------------|----------------------------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username         |
| `DOCKERHUB_TOKEN`    | The access token from Step 2     |

### Step 4 — Push Code to Trigger the Pipeline
```bash
# Make any small change, then push
echo "# trigger" >> README.md
git add .
git commit -m "Trigger CI/CD pipeline"
git push origin main
```

Go to the **Actions** tab in GitHub to watch all 3 jobs run! 🎉

---

## 🔍 Monitoring the Pipeline

In GitHub, go to **Actions** → click the latest workflow run to see:

| Job | What it does |
|-----|-------------|
| 🧪 **Run Tests** | Runs `pytest` — fails fast if any test fails |
| 🐳 **Build & Push Docker Image** | Builds the image and pushes to Docker Hub with `latest` and `sha-<commit>` tags |
| 🚀 **Deploy** | Prints the deploy command (upgrade to real SSH deploy with a server) |

---

## 📦 Pulling the Published Image

After a successful pipeline run, anyone can run your app with:
```bash
docker pull <your-dockerhub-username>/devops-demo-app:latest
docker run -p 5000:5000 <your-dockerhub-username>/devops-demo-app:latest
```

---

## 🔗 API Endpoints

| Endpoint | Method | Response |
|----------|--------|----------|
| `/`      | GET    | HTML home page with pipeline overview |
| `/health`| GET    | `{"status": "ok", "service": "devops-demo-app"}` |

---

## 🚀 Upgrading to Real Deployment

To deploy to a real server (VPS, EC2, etc.), replace the `deploy` job in
`.github/workflows/ci-cd.yml` with:

```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@v1.0.3
  with:
    host:     ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USER }}
    key:      ${{ secrets.DEPLOY_SSH_KEY }}
    script: |
      docker pull ${{ secrets.DOCKERHUB_USERNAME }}/devops-demo-app:latest
      docker compose -f /opt/devops-app/docker-compose.yml up -d
```

Add `DEPLOY_HOST`, `DEPLOY_USER`, and `DEPLOY_SSH_KEY` to your GitHub Secrets.

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| **Python / Flask** | Web application framework |
| **gunicorn** | Production WSGI server |
| **pytest** | Unit testing |
| **Docker** | Containerization |
| **Docker Hub** | Container registry |
| **GitHub Actions** | CI/CD automation |
| **Docker Compose** | Multi-container orchestration |

---

## 📚 Learning Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Get Started](https://docs.docker.com/get-started/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
