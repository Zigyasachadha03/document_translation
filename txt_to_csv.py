import csv

input_file = 'data.txt'
output_file = 'data.csv'
column_labels = ['English', 'Spanish', 'Attribution']

# Open the input TXT file for reading and the output CSV file for writing
with open(input_file, 'r', encoding='utf-8') as txt_file, open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file, delimiter=',')

    # Write the column labels as the first row
    csv_writer.writerow(column_labels)

    # Iterate over each line in the TXT file
    for line in txt_file:
        # Split the line into three parts: Spanish phrase, English translation, and attribution
        parts = line.strip().split('\t')

        # Write the parts to the CSV file as a row
        csv_writer.writerow(parts)

print('Conversion complete.')
