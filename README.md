# Kubernetes Platform

## Overview

Kubernetes Platform is a web-based application designed to manage a Kubernetes clusters.You can create/delete namespaces and checke the status of pods and services. This platform is containerized and uses Helm for deployment.

## Features

- **Namespace Management**: Create and delete namespaces with ease.
- **Pod and Service Status**: Get real-time status updates on your pods and services.

## Prerequisites

Before using the Kubernetes Platform, ensure you have the following:

- A Kubernetes cluster with the necessary permissions to create/delete namespaces and access pod/service statuses.
- Docker installed on your local machine to build and run the containerized application.
- Python 3.8+ for running the backend logic (if not using Docker).

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/oraharon209/kubernetes-platform.git
cd kubernetes-platform
```

### 2. Configure the Backend

Edit the `backend.py` file to set your Helm chart repository details:

```python
helm_chart_repo_url = "https://your-helm-chart-repo-url"
helm_chart_repo_name = "your-helm-chart-repo-name"
```

### 3. Build and Run the Container

Build the Docker image and run it as a container:

```bash
docker build -t kubernetes-platform .
docker run -p 5000:5000 kubernetes-platform
```

### 4. Access the Web Interface

Once the container is running, you can access the Kubernetes Platform via your web browser:

```
http://localhost:5000
```

## Usage

1. **Access the Platform**: Open the web interface in your browser.
2. **Manage Namespaces**: Use the provided options to create or delete namespaces in your Kubernetes cluster.
3. **Check Pod and Service Status**: View the status of your pods and services in real-time.
