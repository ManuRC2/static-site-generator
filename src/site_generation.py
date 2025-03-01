import os, shutil

from markdown_to_html import markdown_to_html_node

def copy_dir(src: str, dest: str):
    files = os.listdir(src)
    for file in files:
        path = os.path.join(src, file)
        if os.path.isfile(path):
            print("Copying file:", file)
            shutil.copy(path, dest)
        else:
            dest_path = os.path.join(dest, file)
            print("Creating directory:", dest_path)
            os.mkdir(dest_path)
            copy_dir(path, dest_path)

def generate_public():
    current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    public_path = os.path.join(current_path, "public")
    static_path = os.path.join(current_path, "static")
    if os.path.exists(public_path):
        print("Directory exists")
        shutil.rmtree(public_path)
        print("Directory deleted")
    else:
        print("Directory does not exist")
    os.mkdir(public_path)
    print("Directory created")
    
    copy_dir(static_path, public_path)
    print("Files copied")
    
    
def extract_title(markdown: str):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line.split("# ")[1]
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        content = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    title = extract_title(content)
    html_node = markdown_to_html_node(content)
    html = html_node.to_html()
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    with open(dest_path, "w+") as file:
        file.write(final_html)
        
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    for file in files:
        path = os.path.join(dir_path_content, file)
        dest_file = file.split(".")[0] + ".html"
        if os.path.isfile(path):
            print("Generating page:", path)
            dest_file = file.split(".")[0] + ".html"
            dest_path = os.path.join(dest_dir_path, dest_file)
            generate_page(path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, file)
            os.mkdir(dest_path)
            generate_pages_recursive(path, template_path, dest_path)