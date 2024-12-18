import os
import random
import csv

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
    return "+".join(parts), original_value, random_value

# Function to replace the numbers in the NAD+ST segment
def modify_nad_st_segment(segment, iteration):
    parts = segment.split("+")
    if len(parts) > 2:
        sub_parts = parts[2].split(":")
        if len(sub_parts) > 0:
            index = iteration % len(random_numbers)
            random_number = "00" + str(random_numbers[index])
            og_nad = parts[2].split(':')[0]
            parts[2] = random_number + (":" + ":".join(sub_parts[1:]) if len(sub_parts) > 1 else "")
    return "+".join(parts), random_number, og_nad

# Function to modify the content of a DAT file
def modify_dat_file_content(original_fn, alt_fn, content, count):
    segments = content.split("'")
    nad_st_count = count
    lin_data = []
    lin_id_data = []
    qty_data = []
    orignal_id = ''
    alt_id = ''
    partial_report = []
    whi_ftx_segments = []

    for i in range(len(segments)):
        if segments[i].startswith("BGM+"):
            segments[i], original_id, alt_id = modify_bgm_segment(segments[i])
        if segments[i].startswith("NAD+ST+"):
            segments[i], alt_st, original_st = modify_nad_st_segment(segments[i], nad_st_count)
        if segments[i].startswith("QTY"):
            qty_data.append(extract_qty_value(segments[i]))
        if segments[i].startswith("LIN"):
            lin_data.append(extract_lin_value(segments[i])[0])
            lin_id_data.append(extract_lin_value(segments[i])[1])
        if segments[i].startswith("FTX+WHI+++"):
            whi_ftx_segments.append(segments[i])
        
    customer_name = extract_customer_value(whi_ftx_segments)
    
    for i in range(len(lin_data)):
        partial_report.append([original_fn, original_id, alt_fn, alt_id, original_st, alt_st, customer_name, lin_id_data[i], lin_data[i], qty_data[i]])

    return "'".join(segments), partial_report


# Function to extract the second last entry from the QTY segment
def extract_qty_value(segment):
    parts = segment.split(":")
    return parts[-2] if len(parts) > 1 else ""

# Function to extract the last value from the LIN segment
def extract_lin_value(segment):
    parts = segment.split("+")
    real = parts[-1].split(":")
    return real[0], parts[1] if len(parts) > 1 else ""

# Function to extract the last value from the LIN segment
def extract_customer_value(segments):
    return segments[1][10:]

# Function to process all DAT files in the input folder
def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
# partial_report.append([original_fn, original_id, alt_fn, alt_id, og_st_data[i], alt_st_data[i], customer_name, lin_id_data[i], lin_data[i], qty_data[i]])
    report = [['ORIGINAL_FILENAME','ORIGINAL_ORDER_ID','ALT_FILENAME','ALT_ORDER_ID','ORIGINAL_ST','ALT_ST','CUSTOMER_NAME','LINE_ID', 'SKU_ID','QUANTITY']]
    
    i = 0
    for filename in os.listdir(input_folder):
        if filename.endswith(".DAT"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, "TEST_" + filename)

            with open(input_file_path, 'r') as file:
                content = file.read()

            modified_content, partial_report = modify_dat_file_content(filename, "TEST_" + filename, content, i)
            i = i + 1

            for j in range(len(partial_report)):
                report.append(partial_report[j])

            with open(output_file_path, 'w') as file:
                file.write(modified_content)
    
    csv_file = 'output/data.csv'

    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(report[0])

        # Write the remaining rows of the array to the CSV file
        for row in report[1:]:
            writer.writerow(row)

    print(f"Array successfully converted to CSV: {csv_file}")
    

# Main function
def main():
    input_folder = "input"
    output_folder = "output"

    process_files(input_folder, output_folder)

if __name__ == "__main__":
    main()
    print('Imputation Complete')