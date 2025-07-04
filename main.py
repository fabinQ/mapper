import argparse
import file_name, renaming, XML_repair, table_scratch, coordinate_transformer, compression_folders

def main():
    while (True):
        print("\nNarzędzie terminalowe, wybierz numer")
        print(" 1. file_name\n", "2. renaming\n", "3. XML_repair\n", "4. table_scratch\n", "5. coordinate_transformer\n", "6. compression\n","exit\n")
        input_value = input()

        if input_value == "1" or input_value == "file_name" or input_value == "1. file_name":
            file_name.main()
        elif input_value == "2" or input_value == "renaming" or input_value == "2. renaming":
            renaming.main()
        elif input_value == "3" or input_value == "XML_repair" or input_value == "3. XML_repair":
            XML_repair.main()
        elif input_value == "4" or input_value == "table_scratch" or input_value == "4. table_scratch":
            table_scratch.main()
        elif input_value == "5" or input_value == "coordinate_transformer" or input_value == "5. coordinate_transformer":
            coordinate_transformer.main()
        elif input_value == "6" or input_value == "compression" or input_value == "6. compression":
            compression_folders.main()
        elif input_value.lower() == "exit":
            break;

if __name__ == "__main__":
    main()