import execute_db_queries

class ButtonInfo():
    def __init__(self, button_id, selected_button_config_id_old ):
        self.button_id = button_id
        self.selected_button_config_id_old = selected_button_config_id_old 

def duplicate_non_default_button_configs(button_ids, old_config_id, type):
    conn, cursor = execute_db_queries.create_db_connection()
    action_dict = {}
    for button in button_ids:
        cursor.execute("""
                        SELECT button_config_id FROM ButtonConfigs WHERE button_id = ? AND configuration_id = ? AND action_type = ?
""",(button.button_id, old_config_id, type))
        button_config_ids = cursor.fetchall()
        if len(button_config_ids) > 0:
            action_dict[button.button_id] = []
            for i in button_config_ids:
                if i[0] == button.selected_button_config_id_old:
                    action_dict[button.button_id].append(i)
                else:
                    action_dict[button.button_id].append(i[0])

    execute_db_queries.close_without_committing_changes(conn)
    return action_dict

def insert_buttonconfig(cursor, device_id, button_id, configuration_id, action_type):
    cursor.execute(""" INSERT INTO ButtonConfigs (device_id, button_id, configuration_id, action_type)
                                VALUES (?, ?, ?, ?)
                           """, (device_id, button_id, configuration_id, action_type))

    cursor.execute(
            """
            SELECT last_insert_rowid();
            """
            )
    return cursor.fetchone()[0]



def duplicate_keypresses(action_dict, device_id, new_config_id):
    conn, cursor = execute_db_queries.create_db_connection()
    
    for i in action_dict.keys():
        for j in action_dict[i]:
            is_selected = False
            if isinstance(j, tuple):
                is_selected = True
                j = j[0]
            cursor.execute("""
                            SELECT keypresses FROM Keypresses WHERE action_id = ? AND source_table = 'ButtonConfigs'
            """,(j,))
            keypresses = cursor.fetchone()[0]
            new_button_config_id = insert_buttonconfig(cursor, device_id, i, new_config_id, "Keypress")
            cursor.execute("""UPDATE Keypresses SET keypresses = ? WHERE action_id = ? AND source_table = 'ButtonConfigs'""",(keypresses, new_button_config_id))
            if is_selected == True:
                cursor.execute("""UPDATE ButtonConfigs SET is_selected = 1 WHERE button_config_id = ?""",(new_button_config_id,))         
    execute_db_queries.commit_changes_and_close(conn)

def duplicate_axes(action_dict, device_id, new_config_id):
    conn, cursor = execute_db_queries.create_db_connection()
    
    for i in action_dict.keys():
        for j in action_dict[i]:
            is_selected = False
            if isinstance(j, tuple):
                is_selected = True
                j = j[0]
            cursor.execute("""
                            SELECT axis_button, axis_multiplier FROM Axes WHERE action_id = ? AND source_table = 'ButtonConfigs'
            """,(j,))
            axis_button, axis_multiplier = cursor.fetchone()
            new_button_config_id = insert_buttonconfig(cursor, device_id, i, new_config_id, "Axis")
            cursor.execute("""UPDATE Axes SET axis_button = ?, axis_multiplier = ?, WHERE action_id = ? AND source_table = 'ButtonConfigs'""", (axis_button, axis_multiplier, new_button_config_id))
            if is_selected == True:
                cursor.execute("""UPDATE ButtonConfigs SET is_selected = 1 WHERE button_config_id = ?""",(new_button_config_id,))   
    execute_db_queries.commit_changes_and_close(conn)

def duplicate_changedpi(action_dict, device_id, new_config_id):


def get_device_button_ids(device_id, old_config_id):
    conn, cursor = execute_db_queries.create_db_connection()

    cursor.execute("""
                        SELECT button_id FROM Buttons WHERE device_id = ? AND reprog = 1 AND accessible = 1
""",(device_id,))
    # device_buttons = [i[0] for i in cursor.fetchall()]
    device_buttons = []
    for i in cursor.fetchall():
        cursor.execute("""SELECT button_config_id FROM ButtonConfigs WHERE is_selected = 1 AND configuration_id = ? AND button_id = ?""", (old_config_id, i[0]))
        instance = ButtonInfo(button_id=i[0], selected_button_config_id_old=cursor.fetchone()[0])
        device_buttons.append(instance)
    execute_db_queries.close_without_committing_changes(conn)

    return device_buttons

def duplicate_default_button_configs(old_config_id, new_config_id, device_buttons):
    conn, cursor = execute_db_queries.create_db_connection()

    for button_id in device_buttons:
        cursor.execute("""
                            SELECT action_type FROM ButtonConfigs WHERE button_id = ? AND configuration_id = ?
    """,(button_id.button_id, new_config_id))
        default_actions = [i[0] for i in cursor.fetchall()]

        cursor.execute("""
                            SELECT action_type FROM ButtonConfigs WHERE button_id = ? AND configuration_id = ? AND is_selected = 1
""",(button_id.button_id, old_config_id))
        selected_action_type = cursor.fetchone()[0]
        if selected_action_type in default_actions:
            cursor.execute("""
                            UPDATE ButtonConfigs SET is_selected = 1 WHERE button_id = ? AND configuration_id = ? AND action_type = ?
                    """,(button_id.button_id, new_config_id, selected_action_type))

    execute_db_queries.commit_changes_and_close(conn)

def duplicate_config(old_config_id, new_config_id):
    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""SELECT configuration_name, dpi, smartshift_on, smartshift_threshold, smartshift_torque, hiresscroll_hires, hiresscroll_invert, hiresscroll_target, thumbwheel_divert, thumbwheel_invert
                   FROM Configurations
                   WHERE configuration_id = ?
                   """, (old_config_id,))

    result = cursor.fetchone()

    cursor.execute("""UPDATE Configurations
                    SET configuration_name = ?, dpi = ?, smartshift_on = ?, smartshift_threshold = ?, smartshift_torque = ?, hiresscroll_hires = ?, hiresscroll_invert = ?, hiresscroll_target = ?, thumbwheel_divert = ?, thumbwheel_invert = ?
                   WHERE configuration_id = ?
                   """, result + (new_config_id,))

    execute_db_queries.commit_changes_and_close(conn)


def main(device_id=1, old_config_id=41, new_config_id=42):
    button_ids = get_device_button_ids(device_id=device_id, old_config_id=old_config_id)
    # duplicate_config(old_config_id=41, new_config_id=42)
    # duplicate_default_button_configs(old_config_id=old_config_id, new_config_id=new_config_id, device_buttons=button_ids)
    keypress_action_dict = duplicate_non_default_button_configs(button_ids, old_config_id, "Keypress")
    if len(keypress_action_dict) > 0:
        duplicate_keypresses(keypress_action_dict, device_id, new_config_id)
    
    axes_action_dict = duplicate_non_default_button_configs(button_ids, old_config_id, "Axis")
    if len(axes_action_dict) > 0:
        duplicate_axes(axes_action_dict, device_id, new_config_id)

    changedpi_action_dict = duplicate_non_default_button_configs(button_ids, old_config_id, "")

if __name__ == "__main__":
    main()