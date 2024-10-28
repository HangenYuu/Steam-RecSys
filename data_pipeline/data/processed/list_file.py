import os

# Get the list of all files in the current directory
files = os.listdir(".")

# Filter out directories and remove file extensions
file_names_without_extension = [
    os.path.splitext(file)[0] for file in files if os.path.isfile(file)
]

# Print the list of file names without extensions
print(",".join(file_names_without_extension))
