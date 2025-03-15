import random
import datetime

def generate_church_member_sql(num_records, output_file):
    with open(output_file, "w") as f:
        f.write("INSERT INTO church_member (id, address, car_number, custom_properties, name, phone_number, profile_image_thumbnail_url, profile_image_url, relationship_with_householder, sex, church_id, householder_id) VALUES\n")
        
        for i in range(300001, num_records + 1):
            record = (
                i,  # id
                f"{random.randint(100, 999)} Example St",  # address
                f"{random.randint(10, 99)}-{random.randint(1000, 9999)}",  # car_number
                f'{{"membershipLevel": "{random.choice(["silver", "gold", "platinum"])}", "joinDate": "{datetime.date(2020, random.randint(1, 12), random.randint(1, 28))}", "preferences": {{"newsletters": {str(random.choice(["true", "false"]))}, "notifications": ["email", "sms"]}}, "hobbies": ["reading", "sports"]}}',  # custom_properties
                f"User {i}",  # name
                f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",  # phone_number
                f"http://example.com/thumb/{i}.jpg",  # profile_image_thumbnail_url
                f"http://example.com/{i}.jpg",  # profile_image_url
                random.choice(["self", "spouse", "child"]),  # relationship_with_householder
                random.choice(["male", "female"]),  # sex
                random.randint(1, 2),  # church_id
                "NULL" if i == 1 else random.randint(1, i-1)  # householder_id
            )
            # SQL INSERT 구문 작성
            sql = f"({record[0]}, '{record[1]}', '{record[2]}', '{record[3]}', '{record[4]}', '{record[5]}', '{record[6]}', '{record[7]}', '{record[8]}', '{record[9]}', {record[10]}, {record[11]}),\n"
            f.write(sql)
        
        # 마지막 줄의 쉼표 제거 후 세미콜론 추가
        f.seek(f.tell() - 2, 0)  # 마지막 쉼표 제거
        f.write(";\n")

# 10만, 30만, 100만 SQL 데이터 생성
# generate_church_member_sql(100000, "church_member_100k.sql")
# generate_church_member_sql(300000, "church_member_300k.sql")
generate_church_member_sql(1000000, "church_member_1m.sql")
