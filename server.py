from flask import Flask, jsonify, request, redirect
import logging
import os
from consistent_hashing import ConsistentHashRing

# Configure logging
if not os.path.exists('app.log'):
    open('app.log', 'a').close()

logging.basicConfig(filename='app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Logging is set up.")

app = Flask(__name__)

@app.before_request
def log_request_info():
    logging.info(f"Received request: {request.method} {request.path} from {request.remote_addr}")

@app.after_request
def log_response_info(response):
    logging.info(f"Response: {response.status_code} {response.get_data(as_text=True)}")
    return response

# Initialize consistent hashing ring
nodes = ["server1", "server2", "server3"]
hash_ring = ConsistentHashRing(nodes)
server_ports = {
    "server1": "5000",
    "server2": "5000",
    "server3": "5000"
}

# Endpoint /home
@app.route('/home', methods=['GET'])
def home():
    server_id = hash_ring.get_node(str(request.remote_addr))
    return jsonify({
        "message": f"Hello from {server_id}",
        "status": "successful"
    }), 200

# Endpoint /heartbeat
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "", 200

# Endpoint /rep
@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(nodes),
            "replicas": nodes
        },
        "status": "successful"
    }), 200

# Endpoint /add
@app.route('/add', methods=['POST'])
def add_server():
    data = request.json
    new_nodes = data.get('hostnames', [])
    for node in new_nodes:
        if node not in nodes:
            nodes.append(node)
            hash_ring.add_node(node)
    return jsonify({
        "message": {
            "N": len(nodes),
            "replicas": nodes
        },
        "status": "successful"
    }), 200

# Endpoint /rm
@app.route('/rm', methods=['DELETE'])
def remove_server():
    data = request.json
    remove_nodes = data.get('hostnames', [])
    for node in remove_nodes:
        if node in nodes:
            nodes.remove(node)
            hash_ring.remove_node(node)
    return jsonify({
        "message": {
            "N": len(nodes),
            "replicas": nodes
        },
        "status": "successful"
    }), 200

# Endpoint to route requests to the appropriate server
@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    server_id = hash_ring.get_node(request.remote_addr)
    server_port = server_ports.get(server_id)
    if server_port:
        logging.info(f"Routing request for {path} to {server_id}")
        return redirect(f"http://{server_id}:{server_port}/{path}", code=307)
    else:
        logging.error(f"Server {server_id} not found for routing request")
        return jsonify({
            "message": "Server not found",
            "status": "failed"
        }), 500

if __name__ == '__main__':
    logging.info("Flask app is starting.")
    app.run(host='0.0.0.0', port=5000)
