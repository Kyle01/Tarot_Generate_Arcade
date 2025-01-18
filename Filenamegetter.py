import os

def get_file_names_from_folder(folder_path):
    try:
        # List all files in the folder
        file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return file_names
    except FileNotFoundError:
        print(f"Error: The folder '{folder_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    folder_path = "assets\copyright"  # Replace with the path to your folder
    file_names = get_file_names_from_folder(folder_path)
    
    if file_names:
        print("List of file names in the folder:")
        for name in file_names:
            print(name)
    else:
        print("No files found in the folder.")
