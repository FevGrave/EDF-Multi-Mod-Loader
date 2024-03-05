import os
import json
import sys
import math 

# Define Classes's Weapon category offset count data
category_offset_count = {
    "RANGER": {
        "Assault Rifles": 45,
        "Shotguns": 28,
        "Snipers": 31,
        "Rocket Launchers": 34,
        "Missile Launchers": 20,
        "Grenades": 41,
        "Special": 58,
        "Support Equipment": 38,
        "Bikes": 9,
        "Tanks": 13,
        "Helicopters": 10
    },
    "WINGDIVER": {
        "Short-Range": 45,
        "Mid-Range Kinetic Weapons": 32,
        "Mid-Range Pulse Weapons": 23,
        "Mid-Range Energy Weapons": 25,
        "Long-Range": 22,
        "Ranged Weapons": 39,
        "Homing Weapons": 19,
        "Special": 21,
        "Plasma Cores": 35
    },
    "FENCER": {
        "CC Strikers": 25,
        "CC Piercers": 26,
        "Shields": 24,
        "Autocannons": 32,
        "Cannons": 33,
        "Missile Launchers": 24,
        "Enhanced Boosters": 18,
        "Enhanced Shields": 12,
        "Enhanced Cannons": 6,
        "Enhanced Exoskeletons": 11
    },
    "AIRRAIDER": {
        "Request Artillery Units": 17,
        "Request Gunships": 37,
        "Request Bombers": 33,
        "Request Missiles": 15,
        "Request Satellites": 20,
        "Limpet Guns": 23,
        "Stationary Weapons": 24,
        "Support Equipment": 35,
        "Special": 28,
        "Empty": 1,
        "Powered Exoskeletons": 21,
        "Special Weapons": 15,
        "Helicopters": 6,
        "Ground Vehicles": 20,
        "Tanks": 20
    },
    "DLC": {
        "DLC PACK 01 & 02": 73
    }
}

def load_json_file(file_path):
    """
    Load JSON data from a file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def open_json_files(base_dir, language_code):
    files_content = {}
    weapon_text_table_filename = f"ImportWeaponTextTable-{language_code}.json"
    weapon_table_filename = "ImportWeaponTable.json"
    
    for filename in os.listdir(base_dir):
        if filename == weapon_text_table_filename or filename == weapon_table_filename:
            with open(os.path.join(base_dir, filename), 'r', encoding='utf-8') as f:
                files_content[filename] = json.load(f)

    return files_content

def dump_json_files(files_content, output_dir, output_text_file_name, output_weapon_file_name):
    if "ImportWeaponTable.json" in files_content:
        with open(os.path.join(output_dir, output_weapon_file_name), 'w', encoding='utf-8') as f:
            json.dump(files_content["ImportWeaponTable.json"], f, ensure_ascii=False, indent=4)
    
    weapon_text_table_filename = f"ImportWeaponTextTable-{language_code}.json"
    if weapon_text_table_filename in files_content:
        with open(os.path.join(output_dir, output_text_file_name), 'w', encoding='utf-8') as f:
            json.dump(files_content[weapon_text_table_filename], f, ensure_ascii=False, indent=4)

def extract_and_prepare_new_data(mods_settings_folder_dir):
    new_weapon_data = {}
    new_text_data = {}
    for filename in os.listdir(mods_settings_folder_dir):
        if filename == "Mod_config_data.json":
            with open(os.path.join(mods_settings_folder_dir, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                new_to_add_weapon_tables = data.get('NewToAddWeaponTables', {})
                for class_name, weapon_types in new_to_add_weapon_tables.items():
                    for weapon_type, weapons in weapon_types.items():
                        # Modify the sorting key function to safely handle shorter 'value' lists
                        sorted_weapons = sorted(weapons, key=lambda w: math.ceil(w.get('Data', {}).get('value', [{}]*5)[4].get('value', 0) * 25))
                        for weapon in sorted_weapons:
                            weapon_level = math.ceil(weapon.get('Data', {}).get('value', [{}]*5)[4].get('value', 0) * 25)
                            weapon_name = weapon.get('Name')
                            if class_name not in new_weapon_data:
                                new_weapon_data[class_name] = {}
                            if weapon_type not in new_weapon_data[class_name]:
                                new_weapon_data[class_name][weapon_type] = []
                            new_weapon_data[class_name][weapon_type].append({
                                'Name': weapon_name,
                                'Level': weapon_level,
                                'Data': weapon.get('Data', {}),
                                'Text': weapon.get('Text', {})
                            })
    return new_weapon_data, new_text_data

def append_new_data(files_content, new_weapon_data, new_text_data, language_code):
    # Assuming files_content contains the structures for both the weapon and text tables
    # and that these need to be updated based on new data

    weapon_table_filename = "ImportWeaponTable.json" # Assuming this is the key for weapon data in files_content
    text_table_filename = f"ImportWeaponTextTable-{language_code}.json" # Constructed with language_code

    # Example logic for appending new weapon data
    if weapon_table_filename in files_content:
        for class_name, weapon_types in new_weapon_data.items():
            for weapon_type, weapons in weapon_types.items():
                # Append or merge the new weapons into the existing data
                # The specific logic here depends on the structure of your files_content
                pass # Replace with actual merging logic

    # Similar logic for appending new text data, using text_table_filename
    if text_table_filename in files_content:
        for class_name, weapon_types in new_text_data.items():
            for weapon_type, texts in weapon_types.items():
                # Append or merge the new texts into the existing data
                pass # Replace with actual merging logic

    # Note: Actual implementation details for merging/appending depend on the structure
    # of files_content and how it represents weapon and text data.

def append_and_sort_weapon_data(weapon_data, new_weapon_data, table_type="table"|"text_table"):
    # Assuming weapon_data is the structure loaded from ImportWeaponTable
    # and new_weapon_data is the sorted list of new weapons with their levels
    for class_name, weapon_types in new_weapon_data.items():
        for weapon_type, weapons in weapon_types.items():
            if class_name not in weapon_data:
                weapon_data[class_name] = {}
            if weapon_type not in weapon_data[class_name]:
                weapon_data[class_name][weapon_type] = []
            weapon_data[class_name][weapon_type].extend(weapons)
            # Sort combined data by weapon level
            weapon_data[class_name][weapon_type] = sorted(weapon_data[class_name][weapon_type], key=lambda w: w['Level'])
    
    # Create a header block with the appropriate table type
    header_block = {
        "format": "SGO",
        "endian": "LE",
        "version": 258,
        "variables": [
            {
                "name": table_type, # This can be "table" or "text_table"
                "type": "ptr",
                "value": []
            }
        ]
    }
    
    # Wrap the weapon data with the header block
    final_data = {
        "header": header_block,
        "data": weapon_data
    }
    
    return final_data

def dump_updated_json_files(weapon_table, text_table, output_dir, output_weapon_file_name, output_text_file_name):
    weapon_table_path = os.path.join(output_dir, output_weapon_file_name)
    text_table_path = os.path.join(output_dir, output_text_file_name)
    
    with open(weapon_table_path, 'w', encoding='utf-8') as f:
        json.dump(weapon_table, f, ensure_ascii=False, indent=4)
    
    with open(text_table_path, 'w', encoding='utf-8') as f:
        json.dump(text_table, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Default values and checks for command-line arguments
    language_code = "EN"  # Default language code
    if len(sys.argv) >= 3:
        language_code = sys.argv[1].upper()
        output_dir = sys.argv[2]
    else:
        print("Usage: script.py <language_code> <output_directory>")
        sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    mods_settings_folder_dir = os.path.join(base_dir, "MOD CONFIG DATA PLACED HERE")
    output_text_file_name = f"WEAPONTEXT.{language_code}.json"
    output_weapon_file_name = "WEAPONTABLE.json"

    # Process JSON files
    files_content = open_json_files(base_dir, language_code)

    # Extract, prepare, and append new data
    new_weapon_data, new_text_data = extract_and_prepare_new_data(mods_settings_folder_dir)
    append_new_data(files_content, new_weapon_data, new_text_data, language_code) # Ensure this function is correctly defined and used

    # Sort (if necessary) and dump updated files
    dump_json_files(files_content, output_dir, output_text_file_name, output_weapon_file_name)


