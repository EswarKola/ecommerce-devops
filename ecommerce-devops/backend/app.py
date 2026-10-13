import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify

app = Flask(__name__)

def connect_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode=os.getenv("DB_SSLMODE", "require"),
        connect_timeout=5,
    )

@app.get("/api/health")
def health():
    return jsonify(status="ok", service="ecommerce-backend"), 200

@app.get("/api/ready")
def ready():
    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return jsonify(status="ready"), 200
    except Exception:
        app.logger.exception("Database readiness check failed")
        return jsonify(status="not ready"), 503

@app.get("/api/products")
def products():
    try:
        with connect_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id,name,description,price FROM products ORDER BY id")
                rows = cur.fetchall()
        for row in rows:
            row["price"] = float(row["price"])
        return jsonify(products=rows)
    except Exception:
        app.logger.exception("Product query failed")
        return jsonify(error="Product service temporarily unavailable"), 503
