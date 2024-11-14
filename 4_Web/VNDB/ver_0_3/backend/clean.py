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

if __name__ == '__main__':
    delete_pycache_folders()