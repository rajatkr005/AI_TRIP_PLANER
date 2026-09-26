from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """This function will return the list of requirements"""

    requirement_list:List[str] = []
    try:
        # Open and read the text files
        with open('requirements.txt','r') as file_obj:
            # Read lines from the file
            lines = file_obj.readlines()
           # process each line in the file
            for line in lines:
                # Strip whitespace and newline characters
                requirement = line.strip()
                # ignore empty lines and -e .
                if requirement and requirement !=  '-e .':
                    requirement_list.append(requirement)
    except  FileNotFoundError:
        print("requirements.txt file not found.")

    return  requirement_list
print(get_requirements())

setup(
    name="AI-TRIP-PLANNER",
    version="0.0.1",
    author="Rajat Kumar",
    author_email="rajatkrace@gmail.com",
    packages= find_packages()
    install_requires=get_requirements()
)


    