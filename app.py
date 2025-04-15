from flask import Flask, request, redirect, render_template
import redis
import hashlib
import os

# Redis hostname from environment variable (default: redis)
redis_host = os.getenv("REDIS_HOST", "redis")

# Connect to Redis
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)

app = Flask(__name__)
BASE_URL = "http://localhost:8080/"

def generate_short_url(long_url):
    return hashlib.md5(long_url.encode()).hexdigest()[:6]

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get("url")
        if long_url:
            short_code = generate_short_url(long_url)
            redis_client.set(short_code, long_url)
            short_url = f"{BASE_URL}{short_code}"
    
    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    long_url = redis_client.get(short_code)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
