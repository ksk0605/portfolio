import json
import random
import datetime

def generate_church_member_data(num_records, output_file):
    data = []
    for i in range(1, num_records + 1):
        record = {
            "id": i,
            "address": f"{random.randint(100, 999)} Example St",
            "car_number": f"{random.randint(10, 99)}-{random.randint(1000, 9999)}",
            "custom_properties": {
                "membershipLevel": random.choice(["silver", "gold", "platinum"]),
                "joinDate": datetime.date(2020, random.randint(1, 12), random.randint(1, 28)).isoformat(),
                "preferences": {
                    "newsletters": random.choice([True, False]),
                    "notifications": random.sample(["email", "sms", "push"], 2)
                },
                "hobbies": random.sample(["reading", "sports", "music", "travel", "gaming"], 3)
            },
            "name": f"User {i}",
            "phone_number": f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            "profile_image_thumbnail_url": f"http://example.com/thumb/{i}.jpg",
            "profile_image_url": f"http://example.com/{i}.jpg",
            "relationship_with_householder": random.choice(["self", "spouse", "child"]),
            "sex": random.choice(["male", "female"]),
            "church_id": random.randint(1, 2),
            "householder_id": None if i == 1 else random.randint(1, i-1),
        }
        data.append(record)
    
    with open(output_file, "w") as f:
        for record in data:
            f.write(json.dumps(record) + "\n")


# 10만, 30만, 100만 데이터 생성
generate_church_member_data(100000, "church_member_100k.json")
generate_church_member_data(300000, "church_member_300k.json")
generate_church_member_data(1000000, "church_member_1m.json")
