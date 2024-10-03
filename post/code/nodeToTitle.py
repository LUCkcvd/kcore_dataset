import re

# Function to load the ID to description mapping from DBLPtitles.txt
def load_id_description_mapping(filename):
    id_to_description = {}
    with open(filename, 'r') as f:
        for line in f:
            # Split by the first space to separate the ID and description correctly
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                id_to_description[parts[0]] = parts[1]
            else:
                print(f"Warning: Could not parse line: {line.strip()}")
    return id_to_description

# Function to process the vectors file (result_lines.log), replace IDs with descriptions from DBLPtitles.txt, and sort by vector length (descending)
def replace_and_sort_by_length_desc(vector_filename, mapping, output_filename):
    clusters = []
    with open(vector_filename, 'r') as f:
        for idx, line in enumerate(f):
            # Extract the IDs inside braces
            ids_match = re.search(r'\{([0-9, ]+)\}', line)
            if ids_match:
                ids_str = ids_match.group(1)
                ids = [id.strip() for id in ids_str.split(',')]
                clusters.append((idx, ids))  # Store original index and ids
            else:
                print(f"Warning: Could not extract IDs from line: {line.strip()}")

    # Replace IDs with descriptions
    clusters_with_descriptions = []
    for idx, cluster in clusters:
        descriptions = []
        for id in cluster:
            if id in mapping:
                descriptions.append(mapping[id])
            else:
                print(f"Warning: No description found for ID {id}")
                descriptions.append(id)  # Keep the ID if no description
        clusters_with_descriptions.append((idx, descriptions))

    # Sort clusters by size (descending) but keep original indices
    clusters_sorted = sorted(clusters_with_descriptions, key=lambda x: len(x[1]), reverse=True)

    # Write to the output file
    with open(output_filename, 'w') as output_file:
        for _, (original_idx, cluster) in enumerate(clusters_sorted):
            cluster_size = len(cluster)
            output_file.write(f'Cluster {original_idx}, size {cluster_size}\n')
            for description in cluster:
                output_file.write(f'{description}\n')
            output_file.write('\n')

    return output_filename

# File paths based on your provided file names
vector_file = 'result_lines.log'
id_description_file = 'DBLPtitles.txt'
output_file = 'JournalTitleClusters.txt'

# Load the ID-to-description mapping from DBLPtitles.txt
id_description_mapping = load_id_description_mapping(id_description_file)

# Check if the mapping was loaded correctly
if not id_description_mapping:
    print("Error: No descriptions were loaded from the DBLPtitles.txt file. Check the file format.")
else:
    print(f"Loaded {len(id_description_mapping)} descriptions from DBLPtitles.txt.")

# Replace the IDs in the vectors from result_lines.log, sort by length (largest to smallest), and write to a file
result_file = replace_and_sort_by_length_desc(vector_file, id_description_mapping, output_file)

# Print success message with the output file location
print(f'Results have been written to {result_file}')

