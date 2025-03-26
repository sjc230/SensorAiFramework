import yaml

# Data to write to the YAML file (Python dictionary)
data = {
    'name': 'John Doe',
    'age': 30,
    'email': 'johndoe@example.com',
    'hobbies': ['Reading', 'Hiking', 'Coding'],
    'address': {
        'street': '123 Elm St',
        'city': 'Springfield',
        'postal_code': 12347
    }
}

# Open the YAML file in write mode
with open("yaml/example.yaml", "w") as file:
    # Write the data to the YAML file
    yaml.dump(data, file, default_flow_style=False)

print("Data has been written to output.yaml")