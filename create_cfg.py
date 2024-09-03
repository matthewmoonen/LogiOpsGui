import execute_db_queries
import os
import BackendData



def get_configurations():
    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""SELECT c.configuration_id
                   FROM Configurations c
                   JOIN Devices d ON c.device_id = d.device_id
                   WHERE d.is_activated = 1 AND c.is_selected = 1;
                   """)
    configuration_ids = cursor.fetchall()

    execute_db_queries.close_without_committing_changes(conn)
    return [i[0] for i in configuration_ids]


def write_intro(file):
    file.write("devices: (\n")


def write_smartshift(file, settings_object):
    file.write("""
    smartshift:
    {
"""
+ f"        on: {str(settings_object.smartshift_on).lower()};\n"
+ f"        threshold: {str(settings_object.smartshift_threshold)};\n"
+ f"        torque: {str(settings_object.smartshift_torque)};\n"
+ "    };")


def write_keypress(file, keypress, spacer_string=''):
    file.write(
 f'{spacer_string}                 keys: {keypress.keypresses};\n'
    )

def write_cycle_dpi(file, dpi_array, spacer_string=''):
    file.write(
 f'{spacer_string}                 dpis: {dpi_array.dpi_array};\n'
    )

def write_axis(file, axis, spacer_string=''):
    file.write(
 f'{spacer_string}                 axis: "{axis.axis_button}";\n'
+f'{spacer_string}                 axis_multiplier: {axis.axis_multiplier};\n'
    )

def write_changedpi(file, dpi_change, spacer_string=''):
    file.write(
 f'{spacer_string}                 inc: {dpi_change.increment};\n'

    )

def write_changehost(file, host_change, spacer_string=''):
    host_string = f'{spacer_string}                 host: "{host_change.host_change}";\n' if host_change.host_change in ["prev", "next"] else f'{spacer_string}                 host: {host_change.host_change};\n'
    file.write(host_string)


def write_nopress(file):
    file.write(
f'                      '
    )


def write_hires_scroll(file, settings_object):
    file.write("""
    hiresscroll:
    {
"""
+ f"        hires: {str(settings_object.hiresscroll_hires).lower()};\n"
+ f"        invert: {str(settings_object.hiresscroll_invert).lower()};\n"
+ f"        target: {str(settings_object.hiresscroll_target).lower()};\n")


        
    def write_scrollwheel_directions(direction):
        selected_action_id = settings_object.scroll_directions[direction].actions.selected_action_id
        spacer_string = "   "
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""SELECT action_type FROM ScrollActions WHERE scroll_action_id = ?""", (selected_action_id,))
        selected_action_type = cursor.fetchone()[0]
        execute_db_queries.close_without_committing_changes(conn)
        if selected_action_type == "Default":
            pass
        else:
            file.write(f"            {direction.lower()}:\n            " + "{\n")

            file.write(f"                mode: \"{settings_object.scroll_directions[direction].mode}\";\n")

            if settings_object.scroll_directions[direction].mode == "OnInterval":
                interval_threshold = "interval"
            else:
                interval_threshold = "threshold"
            file.write(f"                {interval_threshold}: {settings_object.scroll_directions[direction].threshold};\n")
            file.write(f"                action =\n                " + "{" + f"\n                    type: \"{selected_action_type}\";\n")

            if selected_action_type == "Axis":
                write_axis(file, settings_object.scroll_directions[direction].actions.axes[selected_action_id], spacer_string)
            elif selected_action_type == "CycleDPI":
                write_cycle_dpi(file, settings_object.scroll_directions[direction].actions.cycledpi[selected_action_id], spacer_string)
            elif selected_action_type == "ChangeHost":
                write_changehost(file, settings_object.scroll_directions[direction].actions.changehost[selected_action_id], spacer_string)
            elif selected_action_type == "ChangeDPI":
                write_changedpi(file, settings_object.scroll_directions[direction].actions.changedpi[selected_action_id], spacer_string)
            elif selected_action_type == "Keypress":
                write_keypress(file, settings_object.scroll_directions[direction].actions.keypresses[selected_action_id], spacer_string)

            file.write("                };\n")
            file.write("            };\n")

    for direction in ["Up", "Down"]:
        write_scrollwheel_directions(direction)

    file.write("    }; \n")


def write_gestures(file, gestures):
    spacer_string = '                '
    file.write(
 f'                 gestures: (\n'
    )

    for index, gesture in enumerate(gestures.keys()):
        action_type = gestures[gesture].request_selected_type()

        threshold_line = '' if gestures[gesture].threshold == 50 else f'                         threshold: {gestures[gesture].threshold};\n'

        file.write(
  '                     {'
+f'\n                         direction: "{gesture}";\n'
        )
        
        if action_type == "NoPress":
            file.write(
f'                         mode: "NoPress";\n'
            )
        
        else:
            file.write(
f'                         mode: "{gestures[gesture].mode}";\n'
+ threshold_line
+f'                         action = \n'
+ '                             {\n'
+f'                                 type: "{action_type}";\n'
        )
        if action_type == "Axis":
            write_axis(file, gestures[gesture].axes[gestures[gesture].selected_action_id], spacer_string=spacer_string)
        elif action_type == "CycleDPI":
            write_cycle_dpi(file, gestures[gesture].cycledpi[gestures[gesture].selected_action_id], spacer_string=spacer_string)
        elif action_type == "ChangeHost":
            write_changehost(file, gestures[gesture].changehost[gestures[gesture].selected_action_id], spacer_string=spacer_string)
        elif action_type == "ChangeDPI":
            write_changedpi(file, gestures[gesture].changedpi[gestures[gesture].selected_action_id], spacer_string=spacer_string)
        elif action_type == "Keypress":
            write_keypress(file, gestures[gesture].keypresses[gestures[gesture].selected_action_id], spacer_string=spacer_string)

        if action_type != "NoPress":
            file.write(
  '                             };\n')
        if index == 4:
            file.write('                     }\n'  )
        else:
            file.write('                     },\n'  )


    file.write(
 f'         )\n'
    )

def write_button(file, button):
    action_type = button.request_selected_type()

    file.write("""        {
"""
+f"             cid: {button.button_cid};\n"
+f"             action =\n"
+ "             {\n"
+f'                 type: "{action_type}";\n'
)


    if action_type == "Axis":
        write_axis(file, button.axes[button.selected_action_id])
    elif action_type == "CycleDPI":
        write_cycle_dpi(file, button.cycledpi[button.selected_action_id])
    elif action_type == "ChangeHost":
        write_changehost(file, button.hangehost[button.selected_action_id])
    elif action_type == "ChangeDPI":
        write_changedpi(file, button.changedpi[button.selected_action_id])
    elif action_type == "Keypress":
        write_keypress(file, button.keypresses[button.selected_action_id])
    elif action_type == "Gestures":
        write_gestures(file, button.gestures)
    file.write("             };\n")



def write_outro(file):
    file.write(");")



def write_device_cfg(file, settings_object):

    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""SELECT config_file_device_name FROM Devices WHERE device_id = ?""", (settings_object.device_id,))
    config_file_name = cursor.fetchone()[0]
    execute_db_queries.close_without_committing_changes(conn)
    file.write("{\n"
        +f'    name: "{config_file_name}";')

    if settings_object.smartshift_support == True:
        write_smartshift(file, settings_object)
    
    if settings_object.hires_scroll_support == True:
        write_hires_scroll(file, settings_object)

    file.write(f"    dpi: {settings_object.dpi};\n \n"
            + f"    buttons: (\n")

    length = len(settings_object.buttons)

    for index, button in enumerate(settings_object.buttons.values()):
        if button.selected_action_id != button.default:
            write_button(file, button)
            if index == length - 1:
                file.write("        }\n")
            else:
                file.write("        },\n")
    file.write("    );\n")
    if settings_object.has_thumbwheel == True:
        thumbwheel_divert = "true" if settings_object.thumbwheel_divert == True else "false"
        thumbwheel_invert = "true" if settings_object.thumbwheel_invert == True else "false"
        file.write("    thumbwheel: \n    {\n        divert: " + thumbwheel_divert + ";\n        invert: " + thumbwheel_invert + ";\n")
        
        def write_thumbwheel_directions(direction):
            selected_action_id = settings_object.scroll_directions[direction].actions.selected_action_id
            spacer_string = "   "
            conn, cursor = execute_db_queries.create_db_connection()
            cursor.execute("""SELECT action_type FROM ScrollActions WHERE scroll_action_id = ?""", (selected_action_id,))
            selected_action_type = cursor.fetchone()[0]
            execute_db_queries.close_without_committing_changes(conn)
            if selected_action_type == "Default":
                pass
            else:
                file.write(f"            {direction.lower()}:\n            " + "{\n")

                file.write(f"                mode: \"{settings_object.scroll_directions[direction].mode}\";\n")

                if settings_object.scroll_directions[direction].mode == "OnInterval":
                    interval_threshold = "interval"
                else:
                    interval_threshold = "threshold"
                file.write(f"                {interval_threshold}: {settings_object.scroll_directions[direction].threshold};\n")
                file.write(f"                action =\n                " + "{" + f"\n                    type: \"{selected_action_type}\";\n")

                if selected_action_type == "Axis":
                    write_axis(file, settings_object.scroll_directions[direction].actions.axes[selected_action_id], spacer_string)
                elif selected_action_type == "CycleDPI":
                    write_cycle_dpi(file, settings_object.scroll_directions[direction].actions.cycledpi[selected_action_id], spacer_string)
                elif selected_action_type == "ChangeHost":
                    write_changehost(file, settings_object.scroll_directions[direction].actions.changehost[selected_action_id], spacer_string)
                elif selected_action_type == "ChangeDPI":
                    write_changedpi(file, settings_object.scroll_directions[direction].actions.changedpi[selected_action_id], spacer_string)
                elif selected_action_type == "Keypress":
                    write_keypress(file, settings_object.scroll_directions[direction].actions.keypresses[selected_action_id], spacer_string)

                file.write("                };\n")
                file.write("            };\n")




        for direction in ["Right", "Left"]:
            write_thumbwheel_directions(direction)
        
        def write_ttp(object):
            spacer_string = "   "
            selected_action_id = object.selected_action_id
            conn, cursor = execute_db_queries.create_db_connection()
            cursor.execute("""SELECT action_type FROM TouchTapProxy WHERE touch_tap_proxy_id = ?""", (selected_action_id,))
            selected_action_type = cursor.fetchone()[0]
            if selected_action_type == "NoPress":
                pass
            else:
                file.write(f"            {object.ttp.lower()}:\n            " + "{\n")
                file.write(f"\n                    type: \"{selected_action_type}\";\n")

                if selected_action_type == "Axis":
                    write_axis(file, object.axes[selected_action_id], spacer_string)
                elif selected_action_type == "CycleDPI":
                    write_cycle_dpi(file, object.cycledpi[selected_action_id], spacer_string)
                elif selected_action_type == "ChangeHost":
                    write_changehost(file, object.changehost[selected_action_id], spacer_string)
                elif selected_action_type == "ChangeDPI":
                    write_changedpi(file, object.changedpi[selected_action_id], spacer_string)
                elif selected_action_type == "Keypress":
                    write_keypress(file, object.keypresses[selected_action_id], spacer_string)
                file.write("                };\n")


        if settings_object.thumbwheel_touch_support == True:
            write_ttp(settings_object.touch)
        if settings_object.thumbwheel_tap_support == True:
            write_ttp(settings_object.tap)
        if settings_object.thumbwheel_proxy_support == True:
            write_ttp(settings_object.proxy)


        file.write("    }\n")


def set_cfg_location(new_location, new_filename):
    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""UPDATE UserSettings SET value = ? WHERE key = 'cfg_directory'""",(new_location,))
    cursor.execute("""UPDATE UserSettings SET value = ? WHERE key = 'cfg_filename'""",(new_filename,))

    execute_db_queries.commit_changes_and_close(conn)
    return new_location, new_filename

def get_cfg_location():
    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""SELECT value FROM UserSettings WHERE key = 'cfg_directory'""")
    cfg_location = cursor.fetchone()[0]
    cursor.execute("""SELECT value FROM UserSettings WHERE key = 'cfg_filename'""")
    cfg_filename = cursor.fetchone()[0]
    execute_db_queries.close_without_committing_changes(conn)
    return cfg_location, cfg_filename

def automatically_generate_in_home_directory(old_location=None):
    home_dir = os.path.expanduser("~")
    default_location = os.path.join(home_dir, "logid.cfg")

    def found_new_location(new_location):
        return generate_config_file(cfg_dir=new_location, previously_tried_location=old_location)

    if not os.path.exists(default_location):
        return found_new_location(default_location)
    else:
        for i in range(2, 10000):
            location_to_check = os.path.join(home_dir, f"logid({i}).cfg")
            if i == 10000:
                raise FileGenError("Cannot create a unique file name in the home directory.")
            elif not os.path.exists(location_to_check):
                return found_new_location(location_to_check)

def generate_config_file(cfg_dir, previously_tried_location=None, fall_back_to_homedir=False):
    
    device_data = BackendData.Devices.get_all_devices()

    def write_to_file(file):
        write_intro(file)
        length = len(device_data.user_devices)
        for index, (key, device) in enumerate(device_data.user_devices.items()):
            settings_object = device.configurations[device.selected_config]
            write_device_cfg(file, settings_object)
            if index == length - 1:
                file.write("}\n")
            else:
                file.write("},\n")
        write_outro(file)
    
    try:
        with open(cfg_dir, 'w') as file:
            write_to_file(file)
    except PermissionError as e:
        if previously_tried_location:
            return f"Something went wrong. Do not have permission to write to {previously_tried_location} or {cfg_dir}"
        if fall_back_to_homedir:
            return automatically_generate_in_home_directory(cfg_dir)
        else:
            return e

    return (Status.SUCCESS, f"Success! Config file saved as {cfg_dir}") if previously_tried_location is None else \
           f"Permission Error: Do not have permission to write to {previously_tried_location}. Saved as {cfg_dir} instead."

from enum import Enum
class Status(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class FileGenError(Exception):
    "Raised when the file cannot be created"
    pass

def generate_in_app_data():

    current_directory = os.path.dirname(os.path.abspath(__file__))
    target_directory = os.path.join(current_directory, 'app_data')
    log_file_path = os.path.join(target_directory, 'logid.cfg')
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    return generate_config_file(log_file_path)
    

def generate_in_user_chosen_directory(save_directory=None, directory=None, filename=None, overwrite=None):
    if directory == None:
        directory, filename = get_cfg_location()
        if directory == "~":
            home_dir = os.path.expanduser("~")
            save_directory = os.path.join(home_dir, "logid.cfg")
    def join_path():
        return directory + filename if directory[-1] == "/" else directory + "/" + filename
    if save_directory is None and filename is not None and directory is not None:
        save_directory = join_path()
            
    if overwrite == True:
        try:
            os.remove(save_directory)
        except PermissionError as e:
            # return f"Do not have permission to write to user chosen directory: {e}"
            raise e
            # return

    elif os.path.exists(save_directory) and overwrite != True:
        return f"Error: file exists"

    if save_directory is not None:
        return generate_config_file(save_directory)
    
    else:
        return "Error, incomplete save directory specified"

def set_overwrite_or_save_as_copy(new_setting):
    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""UPDATE UserSettings SET value = ? WHERE key = 'overwrite'""",(new_setting,))
    execute_db_queries.commit_changes_and_close(conn)


def get_overwrite_or_save_as_copy():
    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""SELECT value FROM UserSettings WHERE key = 'overwrite'""")
    overwrite = cursor.fetchone()[0]
    execute_db_queries.close_without_committing_changes(conn)
    return True if overwrite == "True" else False if overwrite == "False" else "Error getting overwrite setting"


def main():
    pass

    # print(get_overwrite_or_save_as_copy())
    # generate_in_app_data()

if __name__ == "__main__":
    main()