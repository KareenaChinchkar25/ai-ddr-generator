from jinja2 import Environment, FileSystemLoader
import os


def generate_report(content):

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("ddr_template.md")

    md_output = template.render(content=content)

    os.makedirs("outputs", exist_ok=True)

    output_path = "outputs/DDR_Report.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_output)

    return output_path