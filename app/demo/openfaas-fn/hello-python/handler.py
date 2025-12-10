import json
from datetime import datetime

def handle(req):
    """Simple Python function for OpenFaaS"""
    
    name = req.strip() if req else "World"
    
    response = {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat(),
        "platform": "OpenFaaS on k3s"
    }
    
    return json.dumps(response, indent=2)
