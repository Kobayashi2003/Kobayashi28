import os
import shutil

# Function to delete __pycache__ folders
def delete_pycache_folders():
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                pycache_path = os.path.join(root, dir)
                shutil.rmtree(pycache_path)
                print(f"Deleted __pycache__ folder: {pycache_path}")

def delete_empty_folders():
    for root, dirs, files in os.walk('.', topdown=False):
        for dir in dirs:
            try:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"Deleted empty folder: {dir_path}")
            except Exception as e:
                print(f"Error deleting empty folder {dir_path}: {str(e)}")

if __name__ == '__main__':
    delete_pycache_folders()
    delete_empty_folders()