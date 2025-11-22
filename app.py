from flask import Flask, request, jsonify
from flask_cors import CORS
from heuristics import HeuristicDetector

app = Flask(__name__)
CORS(app)  # Allows your React/HTML frontend to talk to this backend

# Initialize your logic engine
detector = HeuristicDetector()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "message": "PhishGuard Backend is Running!"})

@app.route('/scan', methods=['POST'])
def scan_url():
    """
    Endpoint to scan a URL.
    Expects JSON: { "url": "http://example.com" }
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400
    
    url_to_check = data['url']
    
    # Run your heuristics logic
    result = detector.check_url(url_to_check)
    
    return jsonify(result)

if __name__ == '__main__':
    print("🔥 PhishGuard Backend running on port 5000")
    app.run(debug=True, port=5000)