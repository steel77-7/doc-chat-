# making the terminal app
from utils.document_loader import load_document
from utils.document_loader import query_func
from utils.content_gen import gen_content
import os
import sys


def main():
    print("""Welcome to doc chat\nTo start specify the file location of the pdf document you want to talk to :\n
        """)
    while True:
        file_path = input(": ")
        if not os.path.isfile(file_path):
            print(
                "The provided file path does not exist \nPlease enter a valid file path"\n
            )
            continue

        load_document(file_path)
        while True:
            print(
                "Now Enter what would you like to ask to your documents or enter /exit to terminate\n"
            )
            query = input(": ")
            if query[0] == "/":
                if query != "/exit":
                    print(
                        "Bitch dont try to act cocky just type the right command \nNow either enter the '/exit' cmd or the correct file path\n"
                    )
                    continue
                elif query == "/exit":
                    print("Thanks for using")
                    sys.exit()
            res = gen_content(query_func(query, file_path), query)
            print(res)


main()
