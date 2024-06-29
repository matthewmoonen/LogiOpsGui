import execute_db_queries
import Classes
import os

conn, cursor = execute_db_queries.create_db_connection()



def print_object(settings_object):

    print(settings_object._configuration_name)
    print(settings_object._dpi)
    print(settings_object._hiresscroll_hires)
    print(settings_object._hiresscroll_invert)
    print(settings_object._hiresscroll_target)
    print(settings_object._smartshift_on)
    print(settings_object._smartshift_threshold)
    print(settings_object._smartshift_torque)
    print(settings_object._thumbwheel_divert)
    print(settings_object._thumbwheel_invert)
    print(settings_object.buttons)
    print(settings_object.config_file_name)
    print(settings_object.configuration_id)
    print(settings_object.configuration_name)
    print(settings_object.create_from_configuration_id)
    print(settings_object.date_configuration_added)
    print(settings_object.date_configuration_last_modified)
    print(settings_object.date_device_added)
    print(settings_object.date_device_last_edited)
    print(settings_object.default_dpi)
    print(settings_object.device_id)
    print(settings_object.device_name)
    print(settings_object.dpi)
    print(settings_object.get_data)
    print(settings_object.has_scrollwheel)
    print(settings_object.has_thumbwheel)
    print(settings_object.hires_scroll_support)
    print(settings_object.hiresscroll_hires)
    print(settings_object.hiresscroll_invert)
    print(settings_object.hiresscroll_target)
    print(settings_object.is_activated)
    print(settings_object.is_selected)
    print(settings_object.is_user_device)
    print(settings_object.max_dpi)
    print(settings_object.min_dpi)
    print(settings_object.number_of_sensors)
    print(settings_object.scroll_actions)
    print(settings_object.smartshift_on)
    print(settings_object.smartshift_support)
    print(settings_object.smartshift_threshold)
    print(settings_object.smartshift_torque)
    print(settings_object.thumbwheel_divert)
    print(settings_object.thumbwheel_invert)
    print(settings_object.thumbwheel_proxy_support)
    print(settings_object.thumbwheel_tap_support)
    print(settings_object.thumbwheel_timestamp_support)
    print(settings_object.thumbwheel_touch_support)
    print(settings_object.update_dpi)
    print(settings_object.update_smartshift_threshold)
    print(settings_object.update_smartshift_torque)


def get_configurations():
    cursor.execute("""
                        SELECT configuration_id
                   FROM Configurations
                   WHERE is_selected = 1
""")
    configuration_ids = cursor.fetchall()
    return [i[0] for i in configuration_ids]


def write_intro(file, settings_object):
    file.write(
"""devices: (
{
"""
+ f'    name: "{settings_object.config_file_name}"')


def write_smartshift(file, settings_object):
    file.write("""
    smartshift:
    {
"""
+ f"        on: {str(settings_object.smartshift_on).lower()};\n"
+ f"        threshold: {str(settings_object.smartshift_threshold)};\n"
+ f"        torque: {str(settings_object.smartshift_torque)};\n"
+ "    };")

def write_hires_scroll(file, settings_object):
    file.write("""
    hiresscroll:
    {
"""
+ f"        hires: {str(settings_object.hiresscroll_hires).lower()};\n"
+ f"        invert: {str(settings_object.hiresscroll_invert).lower()};\n"
+ f"        target: {str(settings_object.hiresscroll_target).lower()}\n"
+ "    }; \n")

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

def write_gestures(file, gestures):
    spacer_string = '                '
    file.write(
 f'                 gestures: (\n'
    )

    for gesture in gestures.keys():
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
            write_axis(file, gestures[gesture].gesture_axes[gestures[gesture].selected_gesture_id], spacer_string=spacer_string)
        elif action_type == "CycleDPI":
            write_cycle_dpi(file, gestures[gesture].gesture_cycledpi[gestures[gesture].selected_gesture_id], spacer_string=spacer_string)
        elif action_type == "ChangeHost":
            write_changehost(file, gestures[gesture].gesture_changehost[gestures[gesture].selected_gesture_id], spacer_string=spacer_string)
        elif action_type == "ChangeDPI":
            write_changedpi(file, gestures[gesture].gesture_changedpi[gestures[gesture].selected_gesture_id], spacer_string=spacer_string)
        elif action_type == "Keypress":
            write_keypress(file, gestures[gesture].gesture_keypresses[gestures[gesture].selected_gesture_id], spacer_string=spacer_string)

        if action_type != "NoPress":
            file.write(
  '                             };\n')
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
        write_axis(file, button.button_axes[button.selected_button_config_id])
    elif action_type == "CycleDPI":
        write_cycle_dpi(file, button.button_cycledpi[button.selected_button_config_id])
    elif action_type == "ChangeHost":
        write_changehost(file, button.button_changehost[button.selected_button_config_id])
    elif action_type == "ChangeDPI":
        write_changedpi(file, button.button_changedpi[button.selected_button_config_id])
    elif action_type == "Keypress":
        write_keypress(file, button.button_keypresses[button.selected_button_config_id])
    elif action_type == "Gestures":
        write_gestures(file, button.gesture_dict)
    file.write("             };\n")


def create_cfg_file(settings_object, cfg_dir="app_data/logid.cfg"):

    if os.path.exists(cfg_dir):
       os.remove(cfg_dir)


    with open(cfg_dir, 'w') as file:
        write_intro(file, settings_object)        
        
        if settings_object.smartshift_support == True:
            write_smartshift(file, settings_object)
        
        if settings_object.hires_scroll_support == True:
            write_hires_scroll(file, settings_object)

        file.write(f"    dpi: {settings_object.dpi};\n \n"
                + f"    buttons: (\n")

        for button in settings_object.buttons:
            if button.selected_button_config_id != button.button_default:
                write_button(file, button)
                file.write("        },\n")
        file.write("    );\n")

        file.write("}\n")

        file.write(");")


def main():
    configuration_ids = get_configurations()

    settings_object = Classes.CFGConfig.create_from_configuration_id(configuration_ids[0])

    create_cfg_file(settings_object = settings_object)


if __name__ == "__main__":
    main()