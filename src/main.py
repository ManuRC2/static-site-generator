from site_generation import generate_pages_recursive, generate_public


def main():
    generate_public()
    generate_pages_recursive("content", "template.html", "public")
    
if __name__ == "__main__":
    main()