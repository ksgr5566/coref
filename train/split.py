import json
from sklearn.model_selection import train_test_split

# Load the data from train.json
with open('./train.json', 'r') as file:
    data = json.load(file)['data']

# Split the data into train, test, and dev sets
train_data, test_dev_data = train_test_split(data, test_size=0.2, random_state=42)
test_data, dev_data = train_test_split(test_dev_data, test_size=0.5, random_state=42)

# Save the data into respective JSON files
train_json = {'data': train_data}
with open('./train.json', 'w') as file:
    json.dump(train_json, file)

test_json = {'data': test_data}
with open('./test.json', 'w') as file:
    json.dump(test_json, file)

dev_json = {'data': dev_data}
with open('./dev.json', 'w') as file:
    json.dump(dev_json, file)
