MinIO Association Rules & Recommendation CLI
===========================================

Quick start:
1. Create a Python virtualenv and activate it.
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
2. Install dependencies:
   pip install -r requirements.txt
3. Edit minio_config.json with your MinIO endpoint and credentials if needed.
4. Run generation:
   python main.py generate
5. Recommend using a matrix (after generation):
   python main.py recommend
