import os

def list_applications():
    # Define the directories to search for applications
    app_dirs = [
        "/Applications",                # System-wide applications
        os.path.expanduser("~/Applications")  # User-specific applications
    ]
    
    # Collect all application paths
    applications = []
    for directory in app_dirs:
        if os.path.exists(directory):  # Check if the directory exists
            for item in os.listdir(directory):
                if item.endswith(".app"):
                    applications.append(item)
    
    return applications

# Get and print the list of applications
apps = list_applications()
for app in apps:
    print(app)
