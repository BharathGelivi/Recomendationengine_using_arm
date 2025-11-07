# project-minioverse
A fully dockerized multi-node MinIO cluster setup using Docker Compose for distributed object storage across multiple nodes.


# 🚀 MinIO Docker Cluster

A fully dockerized **multi-node MinIO cluster setup** using Docker Compose for distributed object storage across multiple nodes.

---

## 📦 Overview

This project demonstrates how to deploy a **4-node distributed MinIO cluster** using Docker and Docker Compose.  
It provides a ready-to-run setup for experimenting with scalable, fault-tolerant, and high-performance object storage compatible with Amazon S3 APIs.

---

## ⚙️ Features

- 🧱 Multi-node MinIO deployment (4 nodes by default)
- 🗄️ Distributed & fault-tolerant object storage
- 🔒 Common credentials and unified console access
- 🌐 Accessible from other computers over LAN
- 🧰 Easy to start, stop, and manage with Docker Compose

---
minio-docker-cluster/
├── docker-compose.yml
├── data1/



Each data folder represents storage for one MinIO node.

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/minio-docker-cluster.git
cd minio-docker-cluster
###Access minio data from other laptops
🧠 Access from Another Computer

Find your host IP (e.g., 192.168.1.105)
Check the mc client version-mc.exe --version

Open firewall ports 9000 and 9001

From another system, visit:

http://192.168.1.105:9001

#Download and set up nodes
mc client-Invoke- WebRequest https://dl.min.io/client/mc/release/windows-amd64/mc.exe -OutFile mc.exe

Or use the MinIO Client:

mc alias set myminio http://192.168.1.105:9000 admin password123
mc cp ./example.txt myminio/mybucket
move it to your venv for not disturbing the global python command-mv mc.exe ./venv/Scripts/
and then set up the permission for mc client
mc alias set myminio http://localhost:9000 minioadmin minioadmin

## 🧩 Folder Structure


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
