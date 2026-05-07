PlayMetrics 🎮📊

ML-powered web application that predicts commercial success probability for video game projects using real Steam dataset data.

What is PlayMetrics?
PlayMetrics helps game developers and analysts evaluate the commercial potential of a video game project before launch, by processing historical Steam data across 124,000+ titles and applying machine learning models to surface actionable predictions.
Given a set of inputs — genre tags, release date, expected peak players, and pricing — the app returns a success probability score and a list of 10 comparable titles with similar profiles.

Features

🔮 Success prediction — Dual-model pipeline (Linear Regression + KNN) with less than 5% error on validation sets
🎯 Similar title engine — Returns 10 comparable games per query based on feature similarity
👤 User authentication — Full registration, login, and personalized dashboards
📊 Data pipeline — End-to-end processing from raw Steam dataset to model inference
🐳 Dockerized — Containerized for consistent local and production environments

Tech Stack
LayerTechnologyBackendPython, FlaskML Modelsscikit-learn (Linear Regression, KNN)DatabaseSQLiteFrontendHTML, CSS, JavaScriptData Processingpandas, feature engineeringDevOpsDocker

Project Structure
PlayMetrics/
└── PlayMetrics 0.4/
    ├── app/
    │   ├── models/        # ML model definitions and training
    │   ├── routes/        # Flask route handlers
    │   ├── templates/     # HTML templates
    │   └── static/        # CSS and JS assets
    ├── data/              # Steam dataset
    ├── Dockerfile
    └── requirements.txt

Getting Started
Prerequisites

Python 3.10+
Docker (optional but recommended)

Run locally

# Clone the repository
git clone https://github.com/AlexisJMoranDev/PlayMetrics.git
cd PlayMetrics/PlayMetrics\ 0.4

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

Then open http://localhost:5000 in your browser.

Run with Docker
bashdocker build -t playmetrics .
docker run -p 5000:5000 playmetrics

How It Works

User inputs game parameters: tags, release date, expected peak players, and pricing
The Linear Regression model calculates a commercial success probability score
The KNN similarity engine finds the 10 most comparable titles in the Steam dataset
Results are displayed on a personalized dashboard with historical context

License
This project was developed as a final academic project at CUCEI — Universidad de Guadalajara.
