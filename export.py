import os

def export_markdown(filename, intent, insights):

    os.makedirs("outputs", exist_ok=True)

    path = f"outputs/{filename}.md"

    with open(path, "w", encoding="utf-8") as f:

        f.write("# AI Insights\n\n")

        f.write(f"## Intent: {intent}\n\n")

        f.write(insights)

    return path