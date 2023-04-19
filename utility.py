import threading

# Define a global variable to store the current package ID
current_package_id = 0

# Define a lock to protect access to the current package ID variable
id_lock = threading.Lock()

# Define a function to generate a new package ID
def generate_package_id():
    global current_package_id
    with id_lock:
        current_package_id += 1
        return current_package_id