from database import SessionLocal
from models import Company, Dev, Freebie

session = SessionLocal()

# Fetch instances to test relationships
dev = session.query(Dev).first()
company = session.query(Company).first()
freebie = session.query(Freebie).first()

if dev:
    print(f"Dev: {dev.name}")
else:
    print("No developers found in the database.")

if company:
    print(f"Company: {company.name}")
else:
    print("No companies found in the database.")

if freebie:
    print(f"Freebie: {freebie.print_details()}")
else:
    print("No freebies found in the database.")

session.close()
