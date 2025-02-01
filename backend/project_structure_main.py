import os

from resources.functions.Functions import print_project_structure

if __name__ == "__main__":
    base_path = os.path.abspath(os.path.dirname(__file__))
    project_directory = os.path.join(base_path, "..")

    exclude_folders = [".venv", ".git", ".idea", "_pycache__"]
    print_project_structure(project_directory, exclude_folders)
