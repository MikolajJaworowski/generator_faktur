import os
from datetime import datetime


def create_invoice_directory_structure(base_path: str):
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")

    directory_path = os.path.join(base_path, f"{year}-{month}")

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Folder {directory_path} został utworzony.")
    else:
        print(f"Folder {directory_path} już istnieje.")

    return directory_path
