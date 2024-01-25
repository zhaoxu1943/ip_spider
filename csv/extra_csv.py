import json

import pandas as pd


def test():
    # Read the file
    with open('/home/ip_asn.txt', 'r', encoding="UTF-8") as file:
        data = file.readlines()

    # Count the occurrences of each asn_description
    asn_description_counts = {}
    for line in data:
        json_data = json.loads(line)
        asn_description = json_data.get('asn_description')
        if asn_description:
            if asn_description in asn_description_counts:
                asn_description_counts[asn_description] += 1
            else:
                asn_description_counts[asn_description] = 1

    # Create lists for the columns of the DataFrame
    unique_asn_descriptions = list(asn_description_counts.keys())
    counts = list(asn_description_counts.values())

    # Create DataFrame with columns 'asn_description' and 'count'
    output_df = pd.DataFrame({'asn_description': unique_asn_descriptions, 'count': counts})

    # Sort DataFrame by 'count' column in descending order
    output_df = output_df.sort_values(by='count', ascending=False)

    # Add 'order' column with sequential numbers
    output_df.insert(0, 'order', range(1, len(output_df) + 1))

    # Save DataFrame to a CSV file
    output_df.to_csv('output.csv', index=False)


if __name__ == '__main__':
    test()
