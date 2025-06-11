# 🌿 CleanTech – AQI Prediction Web App

**CleanTech** is a smart and interactive web application that predicts **Air Quality Index (AQI)** using Machine Learning. This project was developed as part of our college mini project (PBL) to raise environmental awareness and promote safe living practices.

---

## 📌 Table of Contents

- [🌍 Overview](#-overview)
- [📁 Project Structure](#-project-structure)
- [✨ Features](#-features)
- [⚙️ Tech Stack](#-tech-stack)
- [🚀 How to Run](#-how-to-run)
- [🖼️ Demo Screenshots](#-demo-screenshots)
- [👩‍💻 Team Members](#-team-members)
- [📬 Contact](#-contact)

---

## 🌍 Overview

The CleanTech platform is designed to:
- Predict air quality based on real-time or given data.
- Provide health-based safety suggestions.
- Display environment-based animations/videos based on AQI levels.
- Spread awareness about the effects of air pollution.

---

## 📁 Project Structure

CleanTech/
├── frontend/
│ ├── index.html
│ ├── script.js
│ ├── styles.css (if available)
│ └── media/
│ ├── environment-bg.jpg
│ ├── environment.mp4
│ ├── fresh-air.mp4
│ ├── mask.mp4
│ ├── pollution.mp4
│ ├── pollution1.mp4
│ └── walking.mp4
│
├── backend/
│ ├── app.py
│ ├── predict_aqi.py
│ ├── models/
│ │ ├── xgb_air_quality_model.pkl
│ │ └── xgb_scaler.pkl
│ └── air-quality-ml/
│ ├── add_aqi.py
│ ├── load_data.py
│ ├── train_model.py
│ ├── air_data.xlsx
│ ├── predicted_air_data.xlsx
│ └── processed_air_data.csv


---

## ✨ Features

- ✅ Predicts AQI levels using trained ML models.
- ✅ Gives appropriate health tips based on AQI level.
- ✅ Shows background animations/videos based on pollution level.
- ✅ Clean and intuitive frontend for user interaction.
- ✅ Flask-powered backend for handling prediction logic.

---

## ⚙️ Tech Stack

| Area       | Technologies                  |
|------------|-------------------------------|
| Frontend   | HTML, CSS, JavaScript         |
| Backend    | Python, Flask                 |
| Machine Learning | XGBoost, Pandas, Scikit-Learn |
| Deployment | GitHub, Vercel (Frontend), Railway (Backend) |

---

## 🚀 How to Run

### ▶️ Backend (Flask API)
1. Navigate to the backend folder:
   ```bash
   cd backend

![homePage](https://github.com/user-attachments/assets/b4ec65e7-c0d6-405e-9e6a-ae7e0386bd6e)
![display results](https://github.com/user-attachments/assets/03e0f6a8-e51b-48ef-bf9c-4b478d4829c3)

