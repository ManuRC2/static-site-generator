import sys
from site_generation import generate_pages_recursive, generate_public


def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    
    generate_public()
    generate_pages_recursive("content", "template.html", "public", basepath)
    
    print(f"Site generated at {basepath}/public/")
    
if __name__ == "__main__":
    main()