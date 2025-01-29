import os

def list_files_in_folder(folder_path):
    # Get a list of items in the directory
    items = os.listdir(folder_path)
    
    # Print each item
    for item in items:
        print(item)

if __name__ == "__main__":
    # Replace this path with the folder you want to inspect
    folder_to_check = "assets/riderWeightPublicDomain/convertedx2"
    
    list_files_in_folder(folder_to_check)
