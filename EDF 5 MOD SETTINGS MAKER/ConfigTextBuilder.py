import os, json, time, sys

def load_json_file(file_path):
    """Utility function to load a JSON file with UTF-8 encoding."""
    with open(file_path, "r", encoding='utf-8') as file:
        return json.load(file)

def sort_and_append_entries(itt_data, new_entries):
    """Sorts and appends new text table entries to the existing data."""
    if 'variables' not in itt_data:
        itt_data['variables'] = []
    itt_data['variables'].extend(new_entries)
    itt_data['variables'].sort(key=lambda entry: entry['name'])
    return itt_data

# Determine the language code from command-line argument
language_code = "EN"  # Default language code
if len(sys.argv) > 1:
    arg = sys.argv[1].upper()
    if arg in ["EN", "CN", "KR", "JA"]:
        language_code = arg

# Paths and directory setup
mod_config_directory_relative = "MOD CONFIG DATA PLACED HERE"
current_directory = os.path.dirname(os.path.abspath(__file__))
default_text_path = os.path.join(current_directory, f"ImportTextTable-{language_code}.json")
mod_config_directory = os.path.join(current_directory, mod_config_directory_relative)

# Load data
ITTdata = load_json_file(default_text_path)
new_text_table_entries = []

# Process each mod config file
for filename in os.listdir(mod_config_directory):
    if filename.endswith('Mod_config_data.json'):
        file_path = os.path.join(mod_config_directory, filename)
        mod_config = load_json_file(file_path)
        if 'NewToAddTextTableEntries' in mod_config:
            new_text_table_entries.extend(mod_config['NewToAddTextTableEntries'])

# Append and sort entries
updated_ITTdata = sort_and_append_entries(ITTdata, new_text_table_entries)

# Determine the output file name based on command-line argument
output_file_name = "TEXTTABLE_XBOX.EN.TXT.json"  # Default value
if len(sys.argv) > 1:
    arg = sys.argv[1].upper()
    if arg in ["EN", "CN", "KR", "JA"]:
        output_file_name = f"TEXTTABLE_XBOX.{arg}.TXT.json"

# Visual indication of process completion
print("Building Text Table", end="", flush=True)
time.sleep(1)  # Wait for 1 second
print(" . ", end="", flush=True)
time.sleep(1)  # Wait for another second
print(" . ", end="", flush=True)
time.sleep(1)  # Wait for another second
print(" . ", end="", flush=True)
time.sleep(1)  # Wait for another second
print("DONE")

# Save the updated data to the specified file
with open(output_file_name, "w", encoding='utf-8') as file:
    json.dump(updated_ITTdata, file, ensure_ascii=False, indent=4)