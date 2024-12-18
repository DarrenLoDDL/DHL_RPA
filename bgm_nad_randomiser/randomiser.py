import os
import random

# List of random numbers to be used for replacement
random_numbers = [
    12009110,
12561150,
12531001,
12609401,
12101004,
12102405,
12402002,
12102613,
12201035]

# Function to replace the numbers in the BGM segment
def modify_bgm_segment(segment):
    parts = segment.split("+")
    if len(parts) > 1:
        original_value = parts[-1]
        random_value = ''.join(random.choices('0123456789', k=len(original_value)))
        parts[-1] = random_value
    return "+".join(parts)

# Function to replace the numbers in the NAD+ST segment
def modify_nad_st_segment(segment, iteration):
    parts = segment.split("+")
    if len(parts) > 2:
        sub_parts = parts[2].split(":")
        if len(sub_parts) > 0:
            index = iteration % len(random_numbers)
            random_number = "00" + str(random_numbers[index])
            parts[2] = random_number + (":" + ":".join(sub_parts[1:]) if len(sub_parts) > 1 else "")
    return "+".join(parts)

# Function to modify the content of a DAT file
def modify_dat_file_content(content):
    segments = content.split("'")
    nad_st_count = 0

    for i in range(len(segments)):
        if segments[i].startswith("BGM+"):
            segments[i] = modify_bgm_segment(segments[i])
        if segments[i].startswith("NAD+ST+"):
            segments[i] = modify_nad_st_segment(segments[i], nad_st_count)
            nad_st_count += 1

    return "'".join(segments)

# Function to process all DAT files in the input folder
def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".DAT"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, "TEST_" + filename)

            with open(input_file_path, 'r') as file:
                content = file.read()

            modified_content = modify_dat_file_content(content)

            with open(output_file_path, 'w') as file:
                file.write(modified_content)

# Main function
def main():
    input_folder = "input"
    output_folder = "output"

    process_files(input_folder, output_folder)

if __name__ == "__main__":
    main()
    print('Randomisation Complete')