import os, json, time

def load_json_file(file_path):
    """Utility function to load a JSON file with UTF-8 encoding."""
    with open(file_path, "r", encoding='utf-8') as file:
        return json.load(file)

def add_new_modes_to_mode_list(mode_list, new_modes):
    """Adds new modes to the ModeList with an incremented Y value after every 2 additions."""
    y_value = 3  # Starting value for Y
    usage_count = 0  # Counter for how many times the current Y value has been used
    for mode in new_modes:
        # Update the relevant dictionary in `mode['value']` list where Y should be inserted
        y_position = 8  # This needs to be adjusted based on your structure
        if len(mode['value']) > y_position:
            mode['value'][y_position] = {"type": "int", "value": y_value}
            usage_count += 1
            if usage_count == 2:
                y_value += 1
                usage_count = 0
        mode_list.append(mode)

def process_weapon_catalog_updates(soldier_init, weapon_catalog_updates, class_name):
    """Appends new weapon catalog entries on top of existing data for a specific class."""
    for entry in soldier_init:
        if entry.get('value')[1].get('value') == class_name:
            weapon_slots = entry.get('value')[4].get('value')
            for slot_index, slot_updates in enumerate(weapon_catalog_updates):
                if slot_index < len(weapon_slots):
                    target_slot = weapon_slots[slot_index]
                    existing_data = target_slot['value'][2]['value']
                    updated_data = existing_data + slot_updates
                    target_slot['value'][2]['value'] = updated_data

def debug_log(data, message="Debug Log"):
    """Function to log data structure for debugging purposes."""
    print(f"{message}: {json.dumps(data, indent=4)}")

def append_to_soldier_weapon_category(soldier_weapon_category, new_categories):
    """Appends new entries to the SoldierWeaponCategory"""
    soldier_weapon_category.extend(new_categories)
    
    soldier_weapon_category.sort(key=lambda x: x[0]['value'] if isinstance(x, list) and x else x['value'][0]['value'] if 'value' in x and isinstance(x['value'], list) and x['value'] else None)

# Paths and directory setup
IDD = "ImportDefaultData.json"
mod_config_directory_relative = "MOD CONFIG DATA PLACED HERE"
current_directory = os.path.dirname(os.path.abspath(__file__))
default_data_path = os.path.join(current_directory, IDD)
mod_config_directory = os.path.join(current_directory, mod_config_directory_relative)

# Load data
IDdata = load_json_file(default_data_path)

# Iterate over each file in the directory that ends with 'Mod_config_data.json'
for filename in os.listdir(mod_config_directory):
    if filename.endswith('Mod_config_data.json'):
        file_path = os.path.join(mod_config_directory, filename)
        mod_config = load_json_file(file_path)

        # Apply additions to the ModeList from each mod configuration file
        add_new_modes_to_mode_list(IDdata["ModeList"], mod_config.get("NewToAddModeList", []))
        process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config.get("NewToAddWeaponCatalog-Ranger", []), "SoldierType_Ranger")
        process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config.get("NewToAddWeaponCatalog-Wingdiver", []), "SoldierType_Wingdiver")
        process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config.get("NewToAddWeaponCatalog-AirRaider", []), "SoldierType_AirRaider")
        process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config.get("NewToAddWeaponCatalog-Fencer", []), "SoldierType_Fencer")
        {"name": "SoldierWeaponCategory", "type": "ptr", "value": IDdata["SoldierWeaponCategory"]},
        append_to_soldier_weapon_category(IDdata["SoldierWeaponCategory"], mod_config["NewToAddSoldierWeaponCategory"])


# Define the data structure for the output CONFIG.JSON file
Head = {
    "format": "SGO",
    "endian": "BE",
    "version": 258,
    "variables": [
        {"name": "ModeList", "type": "ptr", "value": IDdata["ModeList"]},
        {"name": "PackageName", "type": "string", "value": "DEFP"},
        {"name": "SoldierInit", "type": "ptr", "value": IDdata["SoldierInit"]},
        {"name": "SoldierWeaponCategory", "type": "ptr", "value": IDdata["SoldierWeaponCategory"]},
        {"name": "WeaponTable", "type": "string", "value": "app:/Weapon/WeaponTable.sgo"},
        {"name": "WeaponText", "type": "string", "value": "app:/Weapon/WeaponText.%LOCALE%.sgo"}
    ]
}

# Right before exporting the Head dictionary to a JSON file, add:
print("Building Config", end="", flush=True)
time.sleep(1)  # Wait for 1 second
print(" . ", end="", flush=True)
time.sleep(1)  # Wait for another second
print(" . ", end="", flush=True)
time.sleep(1)  # Wait for another second
print(" . ", end="", flush=True)
time.sleep(1)  # Wait for another second
print("DONE")

# Export the Head dictionary to a JSON file
with open('CONFIG.json', "w") as file:
    json.dump(Head, file, indent=4)