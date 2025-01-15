import json
import base64

class DataStoreManager:
    def __init__(self, file_name="", initial_load=False):
        self.file_name = file_name
        self.data_store = {}  # Dictionary to store key-data pairs
        if initial_load:
            self.read()  # Load existing data from the file if it exists

    def append(self, key, data):
        """Add data to the data store with a specific key, auto-detecting the data type."""
        if isinstance(data, bytes):
            # Data is binary
            self.data_store[key] = {
                "type": "binary",
                "value": base64.b64encode(data).decode("utf-8")
            }

        elif isinstance(data, str):
            # Data is text
            self.data_store[key] = {
                "type": "text",
                "value": data
            }
        else:
            raise ValueError("Data must be either a bytes object (for binary) or a string (for text).")

    def write(self):
        """Write the current data store to the specified JSON file."""
        if self.file_name=="":
            raise ValueError("file_name must be passed to this instance")
        with open(self.file_name, 'w') as f:
            json.dump(self.data_store, f)

    def read(self):
        """Load data from the specified JSON file into the data store."""
        try:
            with open(self.file_name, 'r') as f:
                self.data_store = json.load(f)
        except FileNotFoundError:
            self.data_store = {}  # If the file does not exist, start with an empty store

    def get(self, key):
        """Retrieve data for a specific key, returning the appropriate type."""
        if key not in self.data_store:
            raise KeyError(f"Key '{key}' not found in data store.")

        entry = self.data_store[key]
        if entry["type"] == "binary":
            encoded_data=entry["value"]
            # Decode base64 string back to binary data
            return base64.b64decode(encoded_data)   #.encode("utf-8")
        elif entry["type"] == "text":
            # Return text data directly
            return entry["value"]
        else:
            raise ValueError("Unrecognized data type stored in the data.")
    def to_binary(self):
        """Return the JSON representation of the data store as plain text to ensure consistency with write()."""
        # Convert data_store to a JSON string in plain text format
        json_string = json.dumps(self.data_store)
        return json_string.encode('utf-8')  # Convert to bytes using UTF-8 encoding

    def load_from_binary(self, binary_data):
        """Load data from a binary JSON string and save it to data_store."""
        # Convert the binary JSON data to a string and load it into the data_store
        json_string = binary_data.decode('utf-8')  # Decode bytes to string
        self.data_store = json.loads(json_string)
        
'''
# Usage Example
manager = DataStoreManager("data_store.json")

# Append both binary and text paragraphs
manager.append("binary_paragraph1", b"11001010 10111001 ...")  # Binary data
manager.append("text_paragraph1", "This is a text paragraph.")  # Text data

# Write data to the file
manager.write()

# Access specific data
binary_data = manager.get("binary_paragraph1")
text_data = manager.get("text_paragraph1")

print(binary_data)  # Outputs binary data
print(text_data)    # Outputs text data
'''