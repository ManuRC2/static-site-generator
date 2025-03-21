import sys
from site_generation import generate_website


def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    
    generate_website("content", "template.html", basepath)
    
if __name__ == "__main__":
    main()