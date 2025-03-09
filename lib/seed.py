from models import Dev, Company, Freebie
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Sample data
company1 = Company(name="TechCorp", founding_year=2000)
company2 = Company(name="GadgetInc", founding_year=2010)
company3 = Company(name="Google-corp", founding_year=1992)
company4 = Company(name="AWS", founding_year=2007)
company5 = Company(name="AI-solution", founding_year=2015)


dev1 = Dev(name="Lucas")
dev2 = Dev(name="Allie")
dev3 = Dev(name="Damien")
dev4 = Dev(name="Robert")
dev5 = Dev(name="Caleb")


freebie1 = Freebie(item_name="T-Shirt", value=10, company=company1, dev=dev1)
freebie2 = Freebie(item_name="A Hat", value=5, company=company2, dev=dev2)
freebie3 = Freebie(item_name="USB-Drive", value=20, company=company3, dev=dev3)
freebie4 = Freebie(item_name="A Cup", value=12, company=company4, dev=dev4)
freebie5 = Freebie(item_name="T-Shirt", value=15, company=company5, dev=dev5)

# Add to session and commit
try:
    session.bulk_save_objects([
        company1, company2, company3, company4, company5,
        dev1, dev2, dev3, dev4, dev5,
        freebie1, freebie2, freebie3, freebie4, freebie5
    ])
    session.commit()
    print("Database seeded successfully!")
except Exception as e:
    session.rollback()
    print(f"Error seeding database: {e}")
finally:
    session.close()
