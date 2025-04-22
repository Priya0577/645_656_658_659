from flask import Flask, request, redirect, render_template
import redis
import random
import string
import os

app = Flask(__name__)

# Read from environment variables (injected via ConfigMap and Secret)
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD", "")

# Initialize Redis client with error handling
try:
    client = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True
    )
    client.ping()
    print("✅ Connected to Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"❌ Redis connection error: {e}")
    client = None

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url()
        if client:
            client.set(short_url, original_url)
            return render_template('index.html', short_url=request.host_url + short_url)
        return "Redis is not connected", 500
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    if client:
        original_url = client.get(short_url)
        if original_url:
            return redirect(original_url)
    return 'URL not found or Redis not connected', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
