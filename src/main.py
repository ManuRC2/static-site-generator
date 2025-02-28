from site_generation import generate_public, generate_page


def main():
    generate_public()
    generate_page("content/index.md", "template.html", "public/index.html")
    
if __name__ == "__main__":
    main()