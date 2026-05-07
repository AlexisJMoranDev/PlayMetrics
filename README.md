# PlayMetrics 🎮📊

> ML-powered web application that predicts commercial success probability for video game projects using real Steam dataset data.

---

## What is PlayMetrics?

PlayMetrics helps game developers and analysts evaluate the commercial potential of a video game project **before launch**, by processing historical Steam data across 124,000+ titles and applying machine learning models to surface actionable predictions.

Given a set of inputs — genre tags, release date, expected peak players, and pricing — the app returns a **success probability score** and a list of **10 comparable titles** with similar profiles.

---

## Features

- 🔮 **Success prediction** — Dual-model pipeline (Linear Regression + KNN) with less than 5% error on validation sets
- 🎯 **Similar title engine** — Returns 10 comparable games per query based on feature similarity
- 👤 **User authentication** — Full registration, login, and personalized dashboards
- 📊 **Data pipeline** — End-to-end processing from raw Steam dataset to model inference
- 🐳 **Dockerized** — Containerized for consistent local and production environments

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML Models | scikit-learn (Linear Regression, KNN) |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Data Processing | pandas, feature engineering |
| DevOps | Docker |

---

## Project Structure

```
PlayMetrics 0.4/
├── data/                  # Steam dataset (CSV)
├── instance/              # SQLite database instance
├── models/                # ML model definitions and trained artifacts
├── PlayMetrics/           # Main application package
│   ├── static/
│   │   ├── CSS/           # Stylesheets
│   │   ├── JS/            # Client-side scripts
│   │   ├── Image/         # Static images
│   │   └── avatars/       # User profile avatars
│   └── templates/         # HTML templates (Jinja2)
└── Dockerfile
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional but recommended)

### Run locally

```bash
# Clone the repository
git clone https://github.com/AlexisJMoranDev/PlayMetrics.git
cd PlayMetrics/PlayMetrics\ 0.4

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

### Run with Docker

```bash
docker build -t playmetrics .
docker run -p 5000:5000 playmetrics
```

---

## How It Works

1. User inputs game parameters: tags, release date, expected peak players, and pricing
2. The **Linear Regression model** calculates a commercial success probability score
3. The **KNN similarity engine** finds the 10 most comparable titles in the Steam dataset
4. Results are displayed on a personalized dashboard with historical context

---

## Dataset

- Source: Steam game dataset
- Size: 124,000+ titles
- Features used: genre tags, release date, peak concurrent players, revenue indicators

---

## Author

**Fernando Alexis Jiménez Morán**
Programming Engineering — Universidad de Guadalajara (CUCEI)
📧 alexisjmorandev@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/fernandojimenezti) | [GitHub](https://github.com/AlexisJMoranDev)

---

## License

This project was developed as a final academic project at CUCEI — Universidad de Guadalajara.
