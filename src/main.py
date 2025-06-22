from textnode import *
import os
import shutil

def main():
    dm1 = TextNode("hello we are your bank", TextType.BOLD)
    dm2 = TextNode("fuck it up ayyyyy", TextType.LINK, "https://www.boot.dev")
    public_path = "public"
    static_path = "static"
    copy_directory_contents(public_path, static_path)
    generate_pages_recursive("content", "template.html", "public")   

    print(dm1)
    print(dm2)

def copy_directory_contents(public_path, static_path):
    print(f"public path: {public_path} \nstatic_path: {static_path}")
    #if path exists, clear it
    if(os.path.exists(public_path)):
        shutil.rmtree(public_path)
    #create new path
    os.mkdir(public_path)
    dir_list = os.listdir(static_path)
    #base case: dir list is empty so no iteration happens
    for dir_item in dir_list:
        #concatenate dir item to paths
        curr_static_path = static_path + "/" + dir_item
        curr_public_path = public_path + "/" + dir_item
        #item is a file
        if(os.path.isfile(curr_static_path)):
            shutil.copy(curr_static_path, public_path)
        #item is a directory
        else:
            #recurse with address of directory
            copy_directory_contents(curr_public_path, curr_static_path)
                
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        #header line should start with a single #
        if line.startswith("#"):
            return line.strip("# ")
    #if function reaches this point, no header was found
    raise Exception("Title not found :(")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #open markdown file and read it
    markdown_file = open(f"{from_path}", "r")
    markdown = markdown_file.read()
    #open template file and read it
    template_file = open(f"{template_path}", "r")
    template = template_file.read()
    #convert markdown to html string
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    #extract title line from markdown string
    title = extract_title(markdown)
    #insert title and html-formatted content into template string
    template = template.replace("{{ Title }}", title)
    html_page = template.replace("{{ Content }}", html_string)
    #open destination file and write html page to it
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)       
    destination_file = open(f"{dest_path}", "w")
    destination_file.write(html_page)
    print(f"writing html page to {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    #list entries in current directory
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        #define new paths for current item
        item_from_path = dir_path_content + "/" + item
        item_dest_path = dest_dir_path + "/" + item
        #if path leads to markdown file, generate page
        if(os.path.isfile(item_from_path)):
            if(item.endswith(".md")):
                #change destination file type to html
                item_dest_path = item_dest_path.replace(".md", ".html")
                generate_page(item_from_path, template_path, item_dest_path)
        #if path leads to directory, recurse into directory
        elif(os.path.isdir(item_from_path)):
            generate_pages_recursive(item_from_path, template_path, item_dest_path)
        #otherwise, do nothing

main()
