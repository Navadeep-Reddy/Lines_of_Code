import ast
import glob
import os

# Store the paths of the folder
path = r"C:\Users\Navadeep Reddy\Documents\CODE\xml"

# List to store path of every python file
py_files = glob.glob(os.path.join(path, "**\*.py"), recursive=True)

# Opening size.txt to append the outputs
with open("size.txt", 'a') as f:
    # Looping through the files
    for file in py_files:
        with open(file, 'r') as file_reader:
            # Reading the entire file into a string
            code = file_reader.read()
            # Parsing it into a Tree
            Tree = ast.parse(code)

            # Variables for counting classes, methods, and functions
            class_count = 0
            func_count = 0
            meth_count = 0

            # Variables to store lines of code for each class and function
            class_lines = {}
            func_lines = {}

            # Variable to store the total number of lines in the file
            total_lines = code.count("\n") + 1

            # Traversing through the tree
            for node in ast.walk(Tree):
                # Counting the number of classes, methods, and functions
                if isinstance(node, ast.ClassDef):
                    class_count += 1
                    class_lines[node.name] = (node.lineno, node.end_lineno)

                    # Iterating the child nodes to find methods
                    for node1 in ast.iter_child_nodes(node):
                        if isinstance(node1, ast.FunctionDef):
                            meth_count += 1
                            func_lines[node1.name] = (node1.lineno, node1.end_lineno)
                elif isinstance(node, ast.FunctionDef):
                    func_count += 1
                    func_lines[node.name] = (node.lineno, node.end_lineno)

            # Printing the file path and information to console and file
            output = (f"The file at location {file} has\nTotal Size = {total_lines}\n"
                      f" Classes = {class_count}\n Methods = {meth_count}\n"
                      f" Independent Functions = {func_count - meth_count}\n")
            print(output)
            f.write(output)

            # Printing lines of code for each class and function
            for class_name, (start, end) in class_lines.items():
                class_loc = end - start + 1
                class_output = f" Class : {class_name}, has LOC = {class_loc}\n"
                print(class_output)
                f.write(class_output)

            for func_name, (start, end) in func_lines.items():
                func_loc = end - start + 1
                func_output = f" Function : {func_name}, has LOC = {func_loc}\n"
                print(func_output)
                f.write(func_output)

            # Calculating and printing other LOC
            submodule_loc_total = sum(end - start + 1 for start, end in class_lines.values()) + \
                                  sum(end - start + 1 for start, end in func_lines.values())
            other_loc = total_lines - submodule_loc_total
            other_loc_output = f" Other LOC = {other_loc}\n\n"
            print(other_loc_output)
            f.write(other_loc_output)
