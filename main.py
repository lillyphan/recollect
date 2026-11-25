import argparse

from parse import extract_pages, pages_to_text


def run_parse(args):
    pages = extract_pages(args.file)

    for page in pages:
        print(f"===== {page['location']} =====")
        print(page["text"])
        print()

    all_text = pages_to_text(pages)
    print(f"{len(pages)} pages/slides with text")


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    parse_command = commands.add_parser("parse", help="Print the text extracted from a lecture file")
    parse_command.add_argument("file")

    args = parser.parse_args()

    if args.command == "parse":
        run_parse(args)


if __name__ == "__main__":
    main()
