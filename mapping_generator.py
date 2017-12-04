from faker import Faker
import json
import random

fake = Faker()
fake.seed(4321)

record_len = 100
record = {}

for i in range(record_len):
	ip = fake.ipv4()
	hostname = fake.url()
	port = random.randint(0,5000)
	entry = {"hostname":hostname, "ip":ip, "port":port}
	record[f'entry{i}'] = entry

record_json = json.dumps(record)

with open('sample_mapping',mode='w') as f:
	f.write(record_json)

