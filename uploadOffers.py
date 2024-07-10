import datetime
import random
import uuid
from elasticsearch import Elasticsearch, exceptions
import string
def random_date(start, end):
    """Generate a random date between `start` and `end`."""
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def generate_random_string(length=8):
    """Generate a random string of fixed length."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))
def generate_offer():
    """Generate a single job offer with specified attributes."""
    locations = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"]
    companies = ["Microsoft", "Google", "Apple", "Valve", "GitHub", "OpenAI", "Meta", "Sega", "Sony"]
    referents = ["Olivia", "Noah", "Emma", "Liam", "Amelia", "Oliver", "Isabella", "Elijah", "Sophia", "Mateo", "Charlotte", "Lucas", "Ava", "Ezra", "Mia", "Levi", "Luna", "Leo", "Evelyn", "Muhammad"]

    today = datetime.date.today()
    start_of_month = today.replace(day=1)
    end_of_month = today.replace(day=28) + datetime.timedelta(days=4)  # Approximation
    end_of_month = end_of_month - datetime.timedelta(days=end_of_month.day)
    next_monday = today + datetime.timedelta(days=(7 - today.weekday()))
    end_of_year = today.replace(month=12, day=31)

    offer = {
        "employment_type": random.choice(["full time", "part time"]),
        "referent": random.choice(referents),
        "end_service": "2024-07-31",
        "origin": "MIT",
        "date_publication": datetime.date.today(),
        "skills": "springBoot,Angular",
        "start_service": "2024-07-21",
        "date_fin": random_date(next_monday, end_of_year).isoformat(),
        "job_title": "junior software dev",
        "job_description": "you would be taking care of the back end side of the project that would be assigned to you",
        "id": str(uuid.uuid4()),  # Generating a unique UUID for each offer
        "company_name": random.choice(companies),
        "industries": "IT",
        "location": random.choice(locations),
        "internal_reference": generate_random_string(8),
        "seniority": str(random.randint(1, 5)),
        "experience": str(random.randint(1, 5)),
        "status": "open"
    }
    return offer

# Elasticsearch connection
es = Elasticsearch('http://localhost:9200')

# Generate and push 50 offers
for i in range(100):
    offer = generate_offer()
    try:
        es.index(index='offres_emploi', id=offer['id'], body=offer)
        print("done\n")
    except exceptions.ElasticsearchException as e:
        print("not done\n")