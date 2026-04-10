import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    markdown = markdown.split("\n")
    for line in markdown:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No Title Found")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    entries = os.listdir(dir_path_content)
    for entry in entries:
        content_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(content_path):
            base, ext = os.path.splitext(entry)
            if ext == ".md":
                html_file = base + ".html"
                generate_page(
                    content_path,
                    template_path,
                    os.path.join(dest_dir_path, html_file),
                    basepath,
                )

        elif os.path.isdir(content_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(
                os.path.join(dir_path_content, entry),
                template_path,
                os.path.join(dest_dir_path, entry),
                basepath,
            )


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    file_obj = open(from_path, "r")
    file = file_obj.read()
    template_obj = open(template_path, "r")
    template = template_obj.read()
    file_obj.close()
    template_obj.close()

    content = markdown_to_html_node(file)
    title = extract_title(file)
    html = content.to_html()

    title_rep = template.replace("{{ Title }}", title)
    content_rep = title_rep.replace("{{ Content }}", html)
    content_rep = content_rep.replace('href="/', f'href="{basepath}')
    content_rep = content_rep.replace('src"/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(content_rep)
