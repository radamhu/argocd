from flask import Flask
import redis
import subprocess

app = Flask(__name__)
r = redis.Redis(host='redis.local', port=6379)

@app.route('/healthz')
def health_check():
    return 'ok'

@app.route('/alert')
def increment_counter():
    r.incr('counter')
    return 'Counter incremented'

@app.route('/counter')
def get_counter():
    return f'Counter: {r.get("counter")}'

@app.route('/version')
def get_version():
    try:
        commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        return commit.decode('utf-8')
    except Exception:
        return 'Unable to get version information'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
