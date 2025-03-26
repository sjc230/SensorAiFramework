import yaml

# Load the YAML file
with open("yaml/example.yaml", "r") as file:
    data = yaml.safe_load(file)

# Print the loaded data (this will be a dictionary)
print(data)

# Access individual variables
print("Name:", data["name"])
print("Age:", data["age"])
print("Email:", data["email"])
print("Hobbies:", data["hobbies"])
print("Address:", data["address"])

# Access nested data (address is a dictionary)
print("Street:", data["address"]["street"])
print("City:", data["address"]["city"])
print("Postal Code:", data["address"]["postal_code"])
