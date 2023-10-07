import os

def split_large_file(input_file, output_directory, lines_per_file):
    # Initialize variables
    file_count = 0
    current_output_file = None

    # Open the input file
    with open(input_file, 'r',errors='ignore') as source_file:
        for line_number, line in enumerate(source_file, 1):
            if line_number == 1 or line_number % lines_per_file == 1:
                # Start a new output file
                file_count += 1
                output_file_path = f"{output_directory}/output_{file_count}.txt"
                current_output_file = open(output_file_path, 'w')
            
            # Write the current line to the output file
            current_output_file.write(line)

            if line_number % lines_per_file == 0:
                # Close the current output file
                current_output_file.close()
                current_output_file = None

    # Close the last output file if not closed
    if current_output_file is not None:
        current_output_file.close()

if __name__ == "__main__":
    input_file = r"C:\Users\91807\Documents\DS\important\Projects\cloned projects\pdf_to_txt\output_texts\monier williams dict.txt"
    output_directory = r"C:\Users\91807\Documents\DS\important\Projects\cloned projects\pdf_to_txt\output_texts\monier williams dict parts"
    lines_per_file = 1000  # Adjust this based on your needs

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    split_large_file(input_file, output_directory, lines_per_file)