
# Histology Slide Annotation & AI Analysis Platform

A web-based platform for uploading, annotating, and analyzing histology slide images using computer vision and AI. Built with Django and vanilla JavaScript, integrated with Hugging Face pretrained image classification models.

---

##  Features

- Upload and view high-resolution histology slide images
- Annotate regions of interest directly on the image using a canvas overlay
- Save, delete, and export annotations (CSV)
- AI-assisted prediction using pretrained vision transformer models (e.g., ResNet-50, ViT)
- Results displayed live with prediction labels
- User authentication (login/signup)
- Designed for local or cloud deployment

---

## Tech Stack

- **Backend**: Django + SQLite
- **Frontend**: HTML + CSS + JavaScript (canvas drawing)
- **AI Model**: Hugging Face Transformers (`microsoft/resnet-50`, `google/vit-base`, etc.)
- **Deployment**: Local or cloud-ready (Render, Heroku, Railway)

---

