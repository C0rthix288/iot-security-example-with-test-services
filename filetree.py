import os

def create_file_tree(root_dir, skip_list, indent=""):
    file_tree = ""
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if item in skip_list or any(skip_path in item_path for skip_path in skip_list):
            continue
        if os.path.isfile(item_path):
            file_tree += f"{indent}- {item}\n"
        elif os.path.isdir(item_path):
            file_tree += f"{indent}+ {item}\n"
            file_tree += create_file_tree(item_path, skip_list, indent + "  ")
    return file_tree

cwd = os.getcwd()
skip_list = ["__pycache__", ".git", "node_modules", ".vscode", ".gitignore", "filetree.txt", ".DS_Store", ".venv"]
tree_structure = create_file_tree(cwd, skip_list)

with open("filetree.txt", "w") as file:
    file.write(tree_structure)

print("File tree has been saved to filetree.txt")
