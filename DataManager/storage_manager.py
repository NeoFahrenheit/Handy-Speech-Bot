import json
import os
import re
from datetime import datetime

class StorageManager():
    """Class responsible for loading and storing the documents."""

    def __init__(self):
        self.check_folders()
        self.load_app_config()

    def check_folders(self):
        """Check if the working folders in the app exists. If any of them don't, it creates them."""

        user_folder = os.path.expanduser("~")
        self.app_path = os.path.join(user_folder, ".HandySpeechBot")
        self.models_path = os.path.join(self.app_path, "models")
        self.projects_path = os.path.join(self.app_path, "projects")
        self.app_data = {}


        if not (os.path.exists(self.app_path)):
            os.makedirs(self.app_path)

        if not (os.path.exists(self.models_path)):
            os.makedirs(self.models_path)

        if not (os.path.exists(self.projects_path)):
            os.makedirs(self.projects_path)

    def sanitize_folder_filename(self, name: str) -> str:
        """_summary_

        Args:
            name (str): _description_

        Returns:
            str: _description_
        """

        invalid_chars = r'[\\/:"*?<>|]+'
        sanitized_name = re.sub(invalid_chars, '_', name)
        return sanitized_name

    def update_app_settings(self, dict_path: list[str]) -> bool:
        pass

    def create_project_files(self, sanitized_name: str, description: str, model: str) -> tuple[str, str] | None:
        """Create the project files, given a name as typed by the user.

        Args:
            name (sanitized_name): Name of the project, sanitized.
            description (str): Description of the project, as typed by the user.
            model (str): Model chosen by the user.

        Returns:
            tuple[str, str] | None: Rreturns (Name, Path) or None, if any error occurred.
        """        

        try:
            path = os.path.join(self.projects_path, sanitized_name)
            os.makedirs(path)
            os.makedirs(os.path.join(path, 'texts'))
            os.makedirs(os.path.join(path, 'audios'))
            os.makedirs(os.path.join(path, 'databases'))
            settings_file_path = os.path.join(path, 'project_settings.json')
            settings_file = {
                "name": sanitized_name,
                "description": description,
                "needs_processing": False,
                "number_files": 0,
                "model": model,
                "path": path,
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
            
            
            with open(settings_file_path, 'w', encoding='utf-8') as f:
                json.dump(settings_file, f, indent=4)
            
            return (sanitized_name, path)
        except:
            return None
        
    def delete_project_dir(self, name: str) -> None:
        """Deletes a project folder.

        Args:
            name (str): The name of the project to be deleted, sanitized.
        """        

        os.removedirs(os.path.join(self.projects_path, name))

    def check_project_existence(self, project_name: str) -> bool:
        """Checks if the project exists created by checking if the folder.

        Args:
            project_name (str): Name of the project

        Returns:
            bool: True if the project exists, False otherwise.
        """

        sanitized_name = self.sanitize_folder_filename(project_name)
        path = os.path.join(self.projects_path, sanitized_name)
        return os.path.isdir(path)

    def load_app_config(self) -> None:
        """Loads the app configuration file. If does not exists, it creates one."""

        path = os.path.join(self.app_path, "app_config.json")
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                self.app_data = json.loads(text)
        else:
            cpu_threads = os.cpu_count()
            if cpu_threads == None:
                cpu_threads = 4

            self.app_data = {
                "user_config": { 

                    "compute_type": "default",
                    "model": "medium",
                    "cpu_threads": cpu_threads,
                },
                "compute_types": [
                        "default",
                        "int8",
                        "int8_float32",
                        "int8_float16",
                        "int8_bfloat16",
                        "int16",
                        "float16",
                        "bfloat16",
                        "float32",
                    ],
                "models": {
                    "tiny": True,
                    "tiny.en": False,
                    "base": True,
                    "base.en": False,
                    "small": True,
                    "small.en": False,
                    "medium": True,
                    "medium.en":  False,
                    "large-v1": True,
                    "large-v2": True,
                    "large-v3": True,
                    "large": True,
                }
            }

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.app_data, f, indent=4)

    def get_projects(self) -> list[str]:
        """Get the list of available projects. It just returns the name of the folders in the Project dir.

        Returns:
            list[str]: List with the name of the projects, sanitized.
        """        

        projects = [item for item in os.listdir(self.projects_path) if os.path.isdir(os.path.join(self.projects_path, item))]
        return projects
    
    def does_project_exists(self, name: str) -> bool:
        """Checks if a project exists by searching the project dir for the sanitized name.

        Args:
            name (str): The name of the project to be looked for, sanitized.

        Returns:
            bool: Returns true if a project exists with the corresponding name. False otherwise.
        """        

        projects = self.get_projects()
        return True if projects.count(name) > 0 else False