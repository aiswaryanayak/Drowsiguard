# Backend - DrowsyGuard

This folder contains the backend logic for *DrowsyGuard*, our AI-powered drowsiness detection system developed for Hack The Night 5.0.

---

## Description
The backend is developed using Python and Flask to support real-time eye state detection for monitoring drowsiness. 

A Convolutional Neural Network (CNN) model is used to classify eye states (Open or Closed), enabling accurate detection of drowsiness based on live video feed.

---

## Technologies Used
- Python
- Flask
- OpenCV
- TensorFlow / Keras
- Haar Cascade Classifier (Face & Eye Detection)
- CNN-based Custom Trained Model

---

## Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application for handling video frames and predicting drowsiness |
| `buildCNN.py` | Contains the CNN model architecture for eye state classification |
| `preprocessData.py` | Script for preprocessing the dataset used for model training |

---

## Note
This backend is specifically designed to work with our trained model and frontend interface for the DrowsyGuard project.

All model files are stored securely in the `models/` directory (not publicly shared).

---

## Team
Built with passion by Team DrowsyGuard | Hack The Night 5.0

