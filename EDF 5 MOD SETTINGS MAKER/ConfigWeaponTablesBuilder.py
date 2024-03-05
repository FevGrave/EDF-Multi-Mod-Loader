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

def extract_weapon_data_from_config(mods_settings_folder_dir):
    extracted_data = {}
    for filename in os.listdir(mods_settings_folder_dir):
        if filename == "Mod_config_data.json":
            with open(os.path.join(mods_settings_folder_dir, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                new_to_add_weapon_tables = data.get('NewToAddWeaponTables', {})
                for class_name, weapon_types in new_to_add_weapon_tables.items():
                    extracted_data[class_name] = extracted_data.get(class_name, {})
                    for weapon_type, weapons in weapon_types.items():
                        extracted_data[class_name][weapon_type] = []
                        for weapon in weapons:
                            weapon_data = {
                                'Name': weapon.get('Name'),
                                'Data': weapon.get('Data', {}),
                                'Text': weapon.get('Text', {})
                            }
                            # Process the 'Data' field to calculate weapon level
                            for item in weapon_data['Data'].get('value', []):
                                if item['type'] == 'float' and item.get('value'):
                                    # Calculate the weapon level
                                    weapon_level = math.ceil(item['value'] * 25)
                                    # Add or update the weapon level in your data structure
                                    weapon_data['Level'] = weapon_level
                            extracted_data[class_name][weapon_type].append(weapon_data)
    return extracted_data

def calculate_table_pre_offset(import_data, category_offset_count):
    """
    Adjust the import_data based on category_offset_count to calculate pre-offsets.
    """
    for class_name, weapon_types in category_offset_count.items():
        for weapon_type, expected_count in weapon_types.items():
            # Placeholder for offset calculation
            print(f"Calculating offsets for {class_name} -> {weapon_type} with expected count: {expected_count}")
            # Actual logic to adjust offsets goes here


def main(base_dir, language_code):
    # Define file paths
    weapon_table_path = os.path.join(base_dir, "ImportWeaponTable.json")
    weapon_text_table_path = os.path.join(base_dir, f"ImportWeaponTextTable-{language_code}.json")

    # Load JSON data
    import_weapon_data = load_json_file(weapon_table_path)
    import_text_data = load_json_file(weapon_text_table_path)

    # Calculate pre-offsets
    calculate_table_pre_offset(import_weapon_data, category_offset_count)
    calculate_table_pre_offset(import_text_data, category_offset_count)

    # Placeholder for data dumping logic
    # dump_json_files(import_weapon_data, ...)
    # dump_json_files(import_text_data, ...)

if __name__ == "__main__":
    # Default values
    language_code = "EN"
    if len(sys.argv) >= 3:
        language_code = sys.argv[1].upper()
        output_dir = sys.argv[2]  # Assuming output_dir is used later for dumping updated JSON data
    else:
        print("Usage: script.py <language_code> <output_directory>")
        sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    main(base_dir, language_code)
    mods_settings_folder_dir = os.path.join(base_dir, "MOD CONFIG DATA PLACED HERE")
    output_text_file_name = f"WEAPONTEXT.{language_code}.json"
    output_weapon_file_name = "WEAPONTABLE.json"

    # Process JSON files
    files_content = open_json_files(base_dir, language_code)
    dump_json_files(files_content, output_dir, output_text_file_name, output_weapon_file_name)

    # Extract and validate Mod_config_data.json content
    extracted_data = extract_weapon_data_from_config(mods_settings_folder_dir)
