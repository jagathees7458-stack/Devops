"""
Application Routes
"""
from flask import Blueprint, jsonify, render_template_string

main_bp = Blueprint("main", __name__)

# ── Home page HTML template ───────────────────────────────────────────────────
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>DevOps CI/CD Demo App</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #e0e0e0;
    }
    .card {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 16px;
      padding: 48px 56px;
      max-width: 640px;
      width: 90%;
      text-align: center;
      backdrop-filter: blur(10px);
    }
    .badge {
      display: inline-block;
      background: #00b4d8;
      color: #000;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      padding: 4px 12px;
      border-radius: 20px;
      margin-bottom: 24px;
      text-transform: uppercase;
    }
    h1 { font-size: 2rem; margin-bottom: 12px; color: #fff; }
    p  { font-size: 1rem; line-height: 1.7; color: #aaa; margin-bottom: 28px; }
    .pipeline {
      display: flex;
      justify-content: center;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 32px;
    }
    .step {
      background: rgba(0,180,216,0.15);
      border: 1px solid #00b4d8;
      border-radius: 8px;
      padding: 6px 14px;
      font-size: 13px;
      color: #00b4d8;
    }
    .arrow { color: #555; align-self: center; }
    .links a {
      display: inline-block;
      margin: 6px;
      padding: 10px 24px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
      font-size: 14px;
      transition: opacity 0.2s;
    }
    .links a:hover { opacity: 0.8; }
    .btn-primary { background: #00b4d8; color: #000; }
    .btn-outline {
      background: transparent;
      border: 1px solid #00b4d8;
      color: #00b4d8;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">🚀 CI/CD Pipeline Demo</div>
    <h1>Hello, DevOps! 👋</h1>
    <p>
      This app is automatically <strong>tested</strong>, <strong>built into a Docker image</strong>,
      and <strong>deployed</strong> every time code is pushed to GitHub —
      powered by <strong>GitHub Actions</strong>.
    </p>

    <div class="pipeline">
      <span class="step">📝 Code Push</span>
      <span class="arrow">→</span>
      <span class="step">🧪 Test</span>
      <span class="arrow">→</span>
      <span class="step">🐳 Docker Build</span>
      <span class="arrow">→</span>
      <span class="step">📦 Registry Push</span>
      <span class="arrow">→</span>
      <span class="step">🌐 Deploy</span>
    </div>

    <div class="links">
      <a class="btn-primary" href="/health">Health Check</a>
      <a class="btn-outline" href="https://github.com" target="_blank">View on GitHub</a>
    </div>
  </div>
</body>
</html>
"""


@main_bp.route("/")
def home():
    """Home page — shows a visual overview of the CI/CD pipeline."""
    return render_template_string(HOME_HTML)


@main_bp.route("/health")
def health():
    """
    Health check endpoint.
    Used by CI pipelines, load balancers, and container orchestrators
    to verify the application is running correctly.
    Returns HTTP 200 with JSON body.
    """
    return jsonify({"status": "ok", "service": "devops-demo-app"}), 200
