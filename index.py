class SparseMatrix:
    """
    Represents a sparse matrix.
    """

    def __init__(self, num_rows, num_cols):
        """
        Creates an instance of SparseMatrix.
        
        :param num_rows: Number of rows in the matrix.
        :param num_cols: Number of columns in the matrix.
        """
        self.elements = {}  # To store non-zero elements
        self.rows = num_rows  # Total number of rows
        self.cols = num_cols  # Total number of columns

    @staticmethod
    def from_file(matrix_file_path):
        """
        Creates a SparseMatrix from a file path.
        
        :param matrix_file_path: Path to the matrix file.
        :return: A new SparseMatrix instance.
        """
        try:
            with open(matrix_file_path, "r") as file:
                lines = file.readlines()

            if len(lines) < 2:
                raise ValueError(f"File {matrix_file_path} does not contain enough lines for matrix dimensions.")

            # Parse dimensions
            total_rows = int(lines[0].strip().split('=')[1])
            total_cols = int(lines[1].strip().split('=')[1])

            sparse_matrix = SparseMatrix(total_rows, total_cols)

            # Parse elements
            for line in lines[2:]:
                line = line.strip()
                if line == "":
                    continue  # Skip empty lines

                try:
                    row, col, value = map(int, line.strip("()").split(","))
                except ValueError:
                    raise ValueError(f"Invalid format in line: {line}")

                sparse_matrix.set_element(row, col, value)

            return sparse_matrix
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {matrix_file_path}")

    def get_element(self, row, col):
        """
        Retrieves the value of an element at a specific row and column.
        
        :param row: The row index of the element.
        :param col: The column index of the element.
        :return: The value at the specified position, or 0 if not set.
        """
        key = f"{row},{col}"
        return self.elements.get(key, 0)  # Return the value or 0 if not found

    def set_element(self, row, col, value):
        """
        Sets the value of an element at a specific row and column.
        
        :param row: The row index where the value should be set.
        :param col: The column index where the value should be set.
        :param value: The value to set at the specified position.
        """
        if row >= self.rows:
            self.rows = row + 1  # Update rows if needed
        if col >= self.cols:
            self.cols = col + 1  # Update columns if needed

        key = f"{row},{col}"
        self.elements[key] = value  # Set the value in the dictionary

    def add(self, other):
        """
        Adds another SparseMatrix to the current matrix.
        
        :param other: The matrix to add.
        :return: The resulting matrix after addition.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for addition.")

        result_matrix = SparseMatrix(max(self.rows, other.rows), max(self.cols, other.cols))

        # Add all elements from this matrix
        for key, value in self.elements.items():
            row, col = map(int, key.split(","))
            result_matrix.set_element(row, col, value)

        # Add all elements from the other matrix
        for key, value in other.elements.items():
            row, col = map(int, key.split(","))
            current_value = result_matrix.get_element(row, col)
            result_matrix.set_element(row, col, current_value + value)

        return result_matrix

    def subtract(self, other):
        """
        Subtracts another SparseMatrix from the current matrix.
        
        :param other: The matrix to subtract.
        :return: The resulting matrix after subtraction.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for subtraction.")

        result_matrix = SparseMatrix(max(self.rows, other.rows), max(self.cols, other.cols))

        # Add all elements from this matrix
        for key, value in self.elements.items():
            row, col = map(int, key.split(","))
            result_matrix.set_element(row, col, value)

        # Subtract all elements from the other matrix
        for key, value in other.elements.items():
            row, col = map(int, key.split(","))
            current_value = result_matrix.get_element(row, col)
            result_matrix.set_element(row, col, current_value - value)

        return result_matrix

    def multiply(self, other):
        """
        Multiplies the current SparseMatrix by another SparseMatrix.
        
        :param other: The matrix to multiply.
        :return: The resulting matrix after multiplication.
        """
        if self.cols != other.rows:
            raise ValueError("Invalid dimensions for multiplication.")

        result_matrix = SparseMatrix(self.rows, other.cols)

        # Perform multiplication
        for key1, value1 in self.elements.items():
            row1, col1 = map(int, key1.split(","))

            for key2, value2 in other.elements.items():
                row2, col2 = map(int, key2.split(","))

                if col1 == row2:
                    current_value = result_matrix.get_element(row1, col2)
                    result_matrix.set_element(row1, col2, current_value + value1 * value2)

        return result_matrix

    def to_string(self):
        """
        Converts the SparseMatrix to a string representation.
        
        :return: The string representation of the SparseMatrix.
        """
        result = f"rows={self.rows}\ncols={self.cols}\n"
        for key, value in self.elements.items():
            row, col = key.split(",")
            result += f"({row}, {col}, {value})\n"
        return result.strip()  # Return trimmed string

    def save_to_file(self, file_path):
        """
        Saves the SparseMatrix to a file.
        
        :param file_path: The path to save the matrix file.
        """
        content = self.to_string()  # Get string representation
        with open(file_path, "w") as file:
            file.write(content)  # Write to file


def do_some_calculations():
    """
    Performs a matrix operation based on user input.
    """
    try:
        matrix_operations = {
            'a': {'name': 'addition', 'method': 'add'},
            'b': {'name': 'subtraction', 'method': 'subtract'},
            'c': {'name': 'multiplication', 'method': 'multiply'},
        }

        # Prompt user for the first matrix file path
        matrix_file_path1 = input("Enter the file path for the first matrix: ")
        matrix1 = SparseMatrix.from_file(matrix_file_path1)
        print("First matrix loaded........\n")

        # Prompt user for the second matrix file path
        matrix_file_path2 = input("Enter the file path for the second matrix: ")
        matrix2 = SparseMatrix.from_file(matrix_file_path2)
        print("Second matrix loaded........\n")

        # Prompt user for the operation choice
        operation_choice = input("Choose an operation (a - addition, b - subtraction, c - multiplication): ")

        # Check if the operation choice is valid
        operation = matrix_operations.get(operation_choice)
        if operation is None:
            raise ValueError("Invalid operation choice.")

        # Perform the selected operation
        result_matrix = getattr(matrix1, operation['method'])(matrix2)
        print(f"Result of {operation['name']}........\n")

        # Ask user for the output file path
        output_file_path = input("Enter the file path to save the result: ")

        # Save the result matrix to the specified file
        result_matrix.save_to_file(output_file_path)
        print(f"Result saved to {output_file_path}")

    except Exception as error:
        print("Error:", error)


# Run the matrix operation function
do_some_calculations()
