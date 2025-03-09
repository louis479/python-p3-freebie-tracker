from flask import Flask, jsonify, request
from database import SessionLocal
from models import Company, Dev, Freebie

app = Flask(__name__)

# Homepage route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Freebie Tracker API!"})

# Prevent favicon 404 error
@app.route("/favicon.ico")
def favicon():
    return "", 204  # Returns an empty response with status code 204 (No Content)

@app.route("/companies", methods=["GET"])
def get_companies():
    session = SessionLocal()
    try:
        companies = session.query(Company).all()
        response = [{"id": c.id, "name": c.name, "founding_year": c.founding_year} for c in companies]
        return jsonify(response)
    finally:
        session.close()

@app.route("/devs", methods=["GET"])
def get_devs():
    session = SessionLocal()
    try:
        devs = session.query(Dev).all()
        response = [{"id": d.id, "name": d.name} for d in devs]
        return jsonify(response)
    finally:
        session.close()

@app.route("/freebies", methods=["GET"])
def get_freebies():
    session = SessionLocal()
    try:
        freebies = session.query(Freebie).all()
        response = [{"id": f.id, "item_name": f.item_name, "value": f.value, "dev": f.dev.name, "company": f.company.name} for f in freebies]
        return jsonify(response)
    finally:
        session.close()

@app.route("/give_freebie", methods=["POST"])
def give_freebie():
    data = request.json

    # Validate request body
    if "dev_id" not in data or "company_id" not in data:
        return jsonify({"error": "Missing dev_id or company_id"}), 400

    session = SessionLocal()
    try:
        dev = session.query(Dev).filter_by(id=data["dev_id"]).first()
        company = session.query(Company).filter_by(id=data["company_id"]).first()

        if not dev or not company:
            return jsonify({"error": "Dev or Company not found"}), 404

        new_freebie = Freebie(item_name=data["item_name"], value=data["value"], dev=dev, company=company)
        session.add(new_freebie)
        session.commit()

        return jsonify({"message": "Freebie given successfully!"}), 201
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
