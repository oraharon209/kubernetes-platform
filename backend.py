import os
import subprocess
from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)

# Ensure KUBECONFIG environment variable is set
os.environ['KUBECONFIG'] = os.path.expanduser('~/.kube/config')

# GitHub Pages URL for Helm charts
helm_chart_repo_url = "https://oraharon209.github.io/helmcharts"
helm_chart_repo_name = "oraharon209-charts"

# Add Helm repository if it's not already added
try:
    subprocess.run(["helm", "repo", "add", helm_chart_repo_name, helm_chart_repo_url], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error adding Helm repository: {e}")

@app.route('/')
def index():
    # Fetch namespaces using kubectl
    try:
        namespaces_raw = subprocess.check_output(["kubectl", "get", "namespaces", "-o", "jsonpath={.items[*].metadata.name}"], universal_newlines=True)
        namespaces = namespaces_raw.strip().split()  # Split by whitespace and strip extra spaces/newlines
    except subprocess.CalledProcessError as e:
        return f"An error occurred while fetching namespaces: {e}", 500

    return render_template('index.html', namespaces=namespaces)


@app.route('/create', methods=['POST'])
def create():
    namespace = request.form['namespace']
    image = request.form['image']
    try:
        repository, tag = image.split(':')
    except ValueError:
        return "Invalid image format. Please use the format 'name:tag'.", 400

    # Create namespace using kubectl
    try:
        subprocess.run(["kubectl", "create", "namespace", namespace], check=True)
    except subprocess.CalledProcessError as e:
        return f"An error occurred while creating namespace: {e}", 500

    # Deploy using Helm with --set for namespace and image values
    release_name = f"{namespace}-release"
    helm_chart_name = "chartforecast"
    helm_install_command = [
        "helm", "install", release_name, f"{helm_chart_repo_name}/{helm_chart_name}",
        "--namespace", namespace,
        "--set", f"ingress.namespace={namespace}",
        "--set", f"myapp.image={repository}",
        "--set", f"myapp.tag={tag}"
    ]

    try:
        subprocess.run(helm_install_command, check=True)
    except subprocess.CalledProcessError as e:
        return f"An error occurred while deploying with Helm: {e}", 500

    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    namespace = request.form['namespace']

    # Delete namespace using kubectl
    try:
        subprocess.run(["kubectl", "delete", "namespace", namespace], check=True)
    except subprocess.CalledProcessError as e:
        return f"An error occurred while deleting namespace: {e}", 500

    return redirect(url_for('index'))


@app.route('/status/pods', methods=['GET'])
def get_pod_status():
    namespace = request.args.get('namespace')

    try:
        pod_status = subprocess.check_output(["kubectl", "get", "pods", "-n", namespace], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return f"An error occurred while fetching pod status: {e}", 500

    return jsonify({'pod_status': pod_status})


@app.route('/status/services', methods=['GET'])
def get_service_status():
    namespace = request.args.get('namespace')

    try:
        service_status = subprocess.check_output(["kubectl", "get", "services", "-n", namespace], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return f"An error occurred while fetching service status: {e}", 500

    return jsonify({'service_status': service_status})


if __name__ == '__main__':
    app.run(debug=True)
