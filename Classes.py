import execute_db_queries
import button_cid_names


class DeviceID:
    def __init__(self, device_id):
        self.device_id = device_id


class Device(DeviceID):
    def __init__(self, device_id, device_name):
        DeviceID.__init__(self, device_id)
        self.device_name = device_name


class Button(DeviceID):
    def __init__(self, device_id, button_cid, button_name):
        DeviceID.__init__(self, device_id)
        self.button_cid = button_cid
        self.button_name = button_name


class ButtonProperties(Button):
    def __init__(
                    self,
                    button_cid, 
                    reprogrammable,
                    fn_key,
                    mouse_key,
                    gesture_support,
                    accessible,
                    button_name=None,
                    device_id=None,
                    ):
        Button.__init__(self, device_id, button_cid, button_name)
        self.reprogrammable = reprogrammable
        self.fn_key = fn_key
        self.mouse_key = mouse_key
        self.gesture_support = gesture_support
        self.accessible = accessible
        self.button_name = button_cid_names.names.get(button_cid, 'Button Name Undefined')


class ButtonSettings(Button):
    def __init__(
                    self,
                    device_id,
                    button_cid, 
                    button_name,
                    button_id,
                    gesture_support,
                    configuration_id,
                    gestures,
                    button_default = {"button_config_id": None, "is_selected": None},
                    button_nopress = {"button_config_id": None, "is_selected": None},
                    button_togglesmartshift = {"button_config_id": None, "is_selected": None},
                    button_togglehiresscroll = {"button_config_id": None, "is_selected": None},
                    button_gestures = {"button_config_id": None, "is_selected": None},
                    button_keypresses = [],
                    button_axes = [],
                    button_changehost = [],
                    button_cycledpi = []
    ):
        super().__init__(
            device_id,
            button_cid,
            button_name,
            button_id,
        )
        self.gesture_support = gesture_support
        self.configuration_id = configuration_id
        self.gestures = gestures
        self.button_default = button_default
        self.button_nopress = button_nopress
        self.button_togglesmartshift = button_togglesmartshift
        self.button_togglehiresscroll = button_togglehiresscroll
        self.button_gestures = button_gestures
        self.button_keypresses = button_keypresses
        self.button_axes = button_axes
        self.button_changehost = button_changehost
        self.button_cycledpi = button_cycledpi



class Configuration:
    def __init__(
            self,
            configuration_id,
            configuration_name,
            is_selected,
            date_configuration_added = None,
            date_configuration_last_modified = None,
    ):
        self.configuration_id = configuration_id
        self.configuration_name = configuration_name
        self.is_selected = bool(is_selected)
        self.date_configuration_added = date_configuration_added
        self.date_configuration_last_modified = date_configuration_last_modified


class UserDevice(Device):
    def __init__(
      self,
      device_id,
      device_name,
      is_activated,
      configurations = None,
      date_device_added = None,
      date_device_last_edited = None,
        
    ):
        super().__init__(device_id, device_name)
        self.is_activated = is_activated
        self.configurations = configurations
        self.date_device_added = date_device_added
        self.date_device_last_edited = date_device_last_edited


class DeviceProperties(Device):
    def __init__(
                self,
                device_id,
                device_name,
                buttons,
                min_dpi,
                max_dpi,
                default_dpi,
                has_scrollwheel,
                smartshift_support,
                hires_scroll_support,
                has_thumbwheel,
                thumbwheel_tap_support,
                thumbwheel_proxy_support,
                thumbwheel_touch_support,
                thumbwheel_timestamp_support,
                number_of_sensors,
    ):
        super().__init__(
                device_id,
                device_name
                )

        self.buttons = buttons
        self.min_dpi = min_dpi
        self.max_dpi = max_dpi
        self.default_dpi = default_dpi
        self.has_scrollwheel = has_scrollwheel
        self.smartshift_support = smartshift_support
        self.hires_scroll_support = hires_scroll_support
        self.has_thumbwheel = has_thumbwheel
        self.thumbwheel_tap_support = thumbwheel_tap_support
        self.thumbwheel_proxy_support = thumbwheel_proxy_support
        self.thumbwheel_touch_support = thumbwheel_touch_support
        self.thumbwheel_timestamp_support = thumbwheel_timestamp_support
        self.number_of_sensors = number_of_sensors


class DeviceDatabase(DeviceProperties):
    def __init__(
                self,
                device_id,
                device_name,
                buttons,
                min_dpi,
                max_dpi,
                default_dpi,
                has_scrollwheel,
                smartshift_support,
                hires_scroll_support,
                has_thumbwheel,
                thumbwheel_tap_support,
                thumbwheel_proxy_support,
                thumbwheel_touch_support,
                thumbwheel_timestamp_support,
                number_of_sensors,
                config_file_device_name,
                device_pids,
    ):
        super().__init__(
                device_id,
                device_name,
                buttons,
                min_dpi,
                max_dpi,
                default_dpi,
                has_scrollwheel,
                smartshift_support,
                hires_scroll_support,
                has_thumbwheel,
                thumbwheel_tap_support,
                thumbwheel_proxy_support,
                thumbwheel_touch_support,
                thumbwheel_timestamp_support,
                number_of_sensors
                )
        self.config_file_device_name = config_file_device_name
        self.device_pids = device_pids




class ConfigurationSettings(Configuration):
    def __init__(
            self,
            configuration_id,
            device_id,
            configuration_name,
            date_configuration_added,
            date_configuration_last_modified,
            is_selected,
            dpi,
            smartshift_on,
            smartshift_threshold,
            smartshift_torque,
            hiresscroll_hires,
            hiresscroll_invert,
            hiresscroll_target,
            thumbwheel_divert,
            thumbwheel_invert
    ):
        super().__init__(
            configuration_id,
            device_id,
            configuration_name,
            date_configuration_added,
            date_configuration_last_modified,
            is_selected,        
        )
        self.dpi = dpi
        self.smartshift_on = smartshift_on
        self.smartshift_threshold = smartshift_threshold
        self.smartshift_torque = smartshift_torque
        self.hiresscroll_hires = hiresscroll_hires
        self.hiresscroll_invert = hiresscroll_invert
        self.hiresscroll_target = hiresscroll_target
        self.thumbwheel_divert = thumbwheel_divert
        self.thumbwheel_invert = thumbwheel_invert




class ScrollProperties:
    def __init__(
            self,
            configuration_id = None,
            scroll_up_threshold = None,
            scroll_up_mode = None,
            scroll_down_threshold = None,
            scroll_down_mode = None,
            scroll_left_threshold = None,
            scroll_left_mode = None,
            scroll_right_threshold = None,
            scroll_right_mode = None
    ):
            self.configuration_id = configuration_id
            self.scroll_up_threshold = scroll_up_threshold
            self.scroll_down_threshold = scroll_down_threshold
            self.scroll_up_mode = scroll_up_mode
            self.scroll_down_mode = scroll_down_mode
            self.scroll_left_mode = scroll_left_mode
            self.scroll_right_mode = scroll_right_mode
            self.scroll_right_threshold = scroll_right_threshold
            self.scroll_left_threshold = scroll_left_threshold


    @classmethod
    def create_from_configuration_id(cls, configuration_id):
        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        SELECT scroll_direction, threshold, mode
        FROM ScrollActionProperties
        WHERE configuration_id = ?;
        """, (configuration_id,))

        scroll_property_query_results = cursor.fetchall()

        scroll_properties = cls()

        scroll_properties.configuration_id = configuration_id

        for i in scroll_property_query_results:
            scroll_direction, threshold, mode = i
            if scroll_direction == "Up":
                scroll_properties.scroll_up_threshold = threshold
                scroll_properties.scroll_up_mode = mode
            elif scroll_direction == "Down":
                scroll_properties.scroll_down_threshold = threshold
                scroll_properties.scroll_down_mode = mode
            elif scroll_direction == "Left":
                scroll_properties.scroll_left_threshold = threshold
                scroll_properties.scroll_left_mode = mode
            elif scroll_direction == "Right":
                scroll_properties.scroll_right_threshold = threshold
                scroll_properties.scroll_right_mode = mode

        execute_db_queries.close_without_committing_changes(conn)

        return scroll_properties


    @property
    def scroll_up_threshold(self):
        return self._scroll_up_threshold

    @scroll_up_threshold.setter
    def scroll_up_threshold(self, value):
        self._scroll_up_threshold = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE ScrollActionProperties
        SET threshold = ?
        WHERE configuration_id = ? AND scroll_direction = 'Up'
        """, (self._scroll_up_threshold, self.configuration_id))

        conn.commit()
        conn.close()

    @property
    def scroll_down_threshold(self):
        return self._scroll_down_threshold

    @scroll_down_threshold.setter
    def scroll_down_threshold(self, value):
        self._scroll_down_threshold = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE ScrollActionProperties
        SET threshold = ?
        WHERE configuration_id = ? AND scroll_direction = 'Down'
        """, (self._scroll_down_threshold, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def scroll_left_threshold(self):
        return self._scroll_left_threshold

    @scroll_left_threshold.setter
    def scroll_left_threshold(self, value):
        self._scroll_left_threshold = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE ScrollActionProperties
        SET threshold = ?
        WHERE configuration_id = ? AND scroll_direction = 'Left'
        """, (self._scroll_left_threshold, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def scroll_right_threshold(self):
        return self._scroll_right_threshold

    @scroll_right_threshold.setter
    def scroll_right_threshold(self, value):
        self._scroll_right_threshold = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE ScrollActionProperties
        SET threshold = ?
        WHERE configuration_id = ? AND scroll_direction = 'Right'
        """, (self._scroll_right_threshold, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def scroll_up_mode(self):
        return self._scroll_up_mode

    @scroll_up_mode.setter
    def scroll_up_mode(self, value):
        self._scroll_up_mode = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE ScrollActionProperties
        SET mode = ?
        WHERE configuration_id = ? AND scroll_direction = 'Up'
        """, (self._scroll_up_mode, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def scroll_down_mode(self):
        return self._scroll_down_mode

    @scroll_down_mode.setter
    def scroll_down_mode(self, value):
        self._scroll_down_mode = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE ScrollActionProperties
        SET mode = ?
        WHERE configuration_id = ? AND scroll_direction = 'Down'
        """, (self._scroll_down_mode, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def scroll_left_mode(self):
        return self._scroll_left_mode

    @scroll_left_mode.setter
    def scroll_left_mode(self, value):
        self._scroll_left_mode = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE ScrollActionProperties
        SET mode = ?
        WHERE configuration_id = ? AND scroll_direction = 'Left'
        """, (self._scroll_left_mode, self.configuration_id))

        conn.commit()
        conn.close()



    @property
    def scroll_right_mode(self):
        return self._scroll_right_mode

    @scroll_right_mode.setter
    def scroll_right_mode(self, value):
        self._scroll_right_mode = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE ScrollActionProperties
        SET mode = ?
        WHERE configuration_id = ? AND scroll_direction = 'Right'
        """, (self._scroll_right_mode, self.configuration_id))

        conn.commit()
        conn.close()




# class ButtonSettings(Button):
#     def __init__(
#                     self,
#                     device_id,
#                     button_cid, 
#                     button_name,
#                     button_id,
#                     gesture_support,
#                     configuration_id,
#                     gestures,
#                     button_default = {"button_config_id": None, "is_selected": None},
#                     button_nopress = {"button_config_id": None, "is_selected": None},
#                     button_togglesmartshift = {"button_config_id": None, "is_selected": None},
#                     button_togglehiresscroll = {"button_config_id": None, "is_selected": None},
#                     button_gestures = {"button_config_id": None, "is_selected": None},
#                     button_axes = [],
#                     button_changehost = [],
#                     button_cycledpi = []
#     ):
#         super().__init__(
#             device_id,
#             button_cid,
#             button_name,
#             button_id,
#         )
#         self.gesture_support = gesture_support
#         self.configuration_id = configuration_id
#         self.gestures = gestures
#         self.button_default = button_default
#         self.button_nopress = button_nopress
#         self.button_togglesmartshift = button_togglesmartshift
#         self.button_togglehiresscroll = button_togglehiresscroll
#         self.button_gestures = button_gestures
#         self.button_axes = button_axes
#         self.button_changehost = button_changehost
#         self.button_cycledpi = button_cycledpi
        


class DeviceConfig:
    def __init__(
        self,
        device_id=None,
        device_name=None,
        is_user_device=None,
        is_activated=None,
        buttons=[],
        min_dpi=None,
        max_dpi=None,
        default_dpi=None,
        has_scrollwheel=None,
        smartshift_support=None,
        hires_scroll_support=None,
        has_thumbwheel=None,
        thumbwheel_tap_support=None,
        thumbwheel_proxy_support=None,
        thumbwheel_touch_support=None,
        thumbwheel_timestamp_support=None,
        number_of_sensors=None,
        configuration_id=None,
        configuration_name=None,
        date_configuration_added=None,
        date_configuration_last_modified=None,
        is_selected=None,
        dpi=None,
        smartshift_on=None,
        smartshift_threshold=None,
        smartshift_torque=None,
        hiresscroll_hires=None,
        hiresscroll_invert=None,
        hiresscroll_target=None,
        thumbwheel_divert=None,
        thumbwheel_invert=None,
        date_device_added=None,
        date_device_last_edited=None,
    ):
        self.device_id=device_id
        self.device_name=device_name
        self.is_user_device=is_user_device
        self.date_device_added=date_device_added
        self.date_device_last_edited=date_device_last_edited
        self.buttons=buttons
        self.min_dpi=min_dpi
        self.max_dpi=max_dpi
        self.default_dpi=default_dpi
        self.has_scrollwheel=has_scrollwheel
        self.smartshift_support = smartshift_support
        self.hires_scroll_support=hires_scroll_support
        self.has_thumbwheel=has_thumbwheel
        self.thumbwheel_tap_support=thumbwheel_tap_support
        self.thumbwheel_proxy_support=thumbwheel_proxy_support
        self.thumbwheel_touch_support=thumbwheel_touch_support
        self.thumbwheel_timestamp_support=thumbwheel_timestamp_support
        self.number_of_sensors=number_of_sensors
        self.configuration_id=configuration_id
        self.configuration_name=configuration_name
        self.date_configuration_added=date_configuration_added
        self.date_configuration_last_modified=date_configuration_last_modified
        self.is_selected=is_selected
        self.dpi=dpi
        self.smartshift_on = smartshift_on
        self.smartshift_threshold=smartshift_threshold
        self.smartshift_torque=smartshift_torque
        self.hiresscroll_hires=hiresscroll_hires
        self.hiresscroll_invert=hiresscroll_invert
        self.hiresscroll_target=hiresscroll_target
        self.thumbwheel_divert=thumbwheel_divert
        self.thumbwheel_invert=thumbwheel_invert
        self.is_activated=is_activated

    @classmethod
    def create_from_configuration_id(cls, configuration_id):
        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        SELECT *
        FROM Configurations AS C
        JOIN Devices AS D ON C.device_id = D.device_id
        WHERE C.configuration_id = ?;
        """, (configuration_id,))

        configuration_query_result = cursor.fetchone()

        config = cls()

            # Extract values from the query result and set them as attributes
        config.configuration_id, config.device_id, config.configuration_name, config.date_configuration_added, config.date_configuration_last_modified, is_selected, \
        config.dpi, smartshift_on, config.smartshift_threshold, config.smartshift_torque, hiresscroll_hires, hiresscroll_invert, hiresscroll_target, \
        thumbwheel_divert, thumbwheel_invert, repeat_device_id, config.device_name, is_user_device, config_file_device_name, device_pids, \
        config.min_dpi, config.max_dpi, config.default_dpi, has_scrollwheel, has_thumbwheel, thumbwheel_tap_support, thumbwheel_proxy_support, \
        thumbwheel_touch_support, thumbwheel_timestamp_support, smartshift_support, hires_scroll_support, config.number_of_sensors, \
        config.date_device_added, config.date_device_last_edited, is_activated = configuration_query_result


        config.is_selected = bool(is_selected)
        config.smartshift_on = bool(smartshift_on)
        config.hiresscroll_hires = bool(hiresscroll_hires)
        config.hiresscroll_invert = bool(hiresscroll_invert)
        config.hiresscroll_target = bool(hiresscroll_target)
        config.thumbwheel_divert = bool(thumbwheel_divert)
        config.thumbwheel_invert = bool(thumbwheel_invert)
        config.is_user_device = bool(is_user_device)
        config.has_scrollwheel = bool(has_scrollwheel)
        config.has_thumbwheel = bool(has_thumbwheel)
        config.thumbwheel_tap_support = bool(thumbwheel_tap_support)
        config.thumbwheel_proxy_support = bool(thumbwheel_proxy_support)
        config.thumbwheel_touch_support = bool(thumbwheel_touch_support)
        config.thumbwheel_timestamp_support = bool(thumbwheel_timestamp_support)
        config.smartshift_support = bool(smartshift_support)
        config.hires_scroll_support = bool(hires_scroll_support)
        config.is_activated = bool(is_activated)


        cursor.execute("""
            SELECT button_id
            FROM Buttons
            WHERE device_id = ? AND reprog = 1 AND accessible = 1
        """, (config.device_id,))
        button_id_list = cursor.fetchall()

        for [i] in button_id_list:
            
            one_config_values = {"Default":None, "Gestures":None, "NoPress":None, "ToggleHiresScroll":None, "ToggleSmartShift":None}
            for key in one_config_values:
                cursor.execute("""
                            SELECT button_config_id
                            FROM ButtonConfigs
                            WHERE button_id = ? AND action_type = ?
                """, (i, key))
                result = cursor.fetchone()

                if result:
                    one_config_values[key] = result[0]
        
            cursor.execute("""
                            SELECT 
                                ButtonConfigs.button_config_id,
                                Keypresses.keypress_id,
                                Keypresses.keypresses
                            FROM 
                                ButtonConfigs
                            JOIN 
                                Keypresses ON Keypresses.action_id = ButtonConfigs.button_config_id
                            WHERE 
                                ButtonConfigs.configuration_id = ?
                                AND ButtonConfigs.button_id = ?
                                AND ButtonConfigs.action_type = 'Keypress' 
                                AND Keypresses.source_table = 'ButtonConfigs';
                            """, (configuration_id, i))
            
            keypress_list = cursor.fetchall()
            if len(keypress_list) != 0:
                print(keypress_list)

            cursor.execute("""
                            SELECT
                                ButtonConfigs.button_config_id,
                                ChangeHost.host_id,
                                ChangeHost.host_change
                            FROM
                                ButtonConfigs
                            JOIN
                                ChangeHost ON ChangeHost.action_id = ButtonConfigs.button_config_id
                            WHERE
                                ButtonConfigs.configuration_id = ?
                                AND ButtonConfigs.button_id = ?
                                AND ButtonConfigs.action_type = 'Keypress'
                                AND ChangeHost.source_table = 'ButtonConfigs';
                            """, (configuration_id, i))
            changehost_list = cursor.fetchall()
            if len(changehost_list) != 0:
                print(changehost_list)


            cursor.execute("""
                            SELECT
                                ButtonConfigs.button_config_id,
                                CycleDPI.cycle_dpi_id,
                                CycleDPI.dpi_array
                            FROM
                                ButtonConfigs
                            JOIN
                                CycleDPI ON CycleDPI.action_id = ButtonConfigs.button_config_id
                            WHERE 
                                ButtonConfigs.configuration_id = ?
                                AND ButtonConfigs.button_id = ?
                                AND ButtonConfigs.action_type = 'CycleDPI'
                                AND CycleDPI.source_table = 'ButtonConfigs';
                            """, (configuration_id, i))
            cycledpi_list = cursor.fetchall()
            if len(cycledpi_list) != 0:
                print(cycledpi_list)


            cursor.execute("""
                            SELECT
                                ButtonConfigs.button_config_id,
                                Axes.axis_id,
                                Axes.axis_button,
                                Axes.axis_multiplier
                            FROM
                                ButtonConfigs
                            JOIN
                                Axes ON Axes.action_id = ButtonConfigs.button_config_id
                            WHERE 
                                ButtonConfigs.configuration_id = ?
                                AND ButtonConfigs.button_id = ?
                                AND ButtonConfigs.action_type = 'Keypress'
                                AND Axes.source_table = 'ButtonConfigs';
                            """, (configuration_id, i))
            axes_list = cursor.fetchall()
            if len(axes_list) != 0:
                print(axes_list)





        execute_db_queries.close_without_committing_changes(conn)

        return config


    @property
    def smartshift_on(self):
        return self._smartshift_on

    @smartshift_on.setter
    def smartshift_on(self, value):
        self._smartshift_on = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET smartshift_on = ?
        WHERE configuration_id = ?;
        """, (self._smartshift_on, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def hiresscroll_hires(self):
        return self._hiresscroll_hires

    @hiresscroll_hires.setter
    def hiresscroll_hires(self, value):
        self._hiresscroll_hires = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET hiresscroll_hires = ?
        WHERE configuration_id = ?;
        """, (self._hiresscroll_hires, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def hiresscroll_invert(self):
        return self._hiresscroll_invert

    @hiresscroll_invert.setter
    def hiresscroll_invert(self, value):
        self._hiresscroll_invert = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET hiresscroll_invert = ?
        WHERE configuration_id = ?;
        """, (self._hiresscroll_invert, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def hiresscroll_target(self):
        return self._hiresscroll_target

    @hiresscroll_target.setter
    def hiresscroll_target(self, value):
        self._hiresscroll_target = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET hiresscroll_target = ?
        WHERE configuration_id = ?;
        """, (self._hiresscroll_target, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def thumbwheel_divert(self):
        return self._thumbwheel_divert

    @thumbwheel_divert.setter
    def thumbwheel_divert(self, value):
        self._thumbwheel_divert = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET thumbwheel_divert = ?
        WHERE configuration_id = ?;
        """, (self._thumbwheel_divert, self.configuration_id))

        conn.commit()
        conn.close()

    @property
    def thumbwheel_invert(self):
        return self._thumbwheel_invert

    @thumbwheel_invert.setter
    def thumbwheel_invert(self, value):
        self._thumbwheel_invert = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET thumbwheel_invert = ?
        WHERE configuration_id = ?;
        """, (self._thumbwheel_invert, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def dpi(self):
        return self._dpi

    @dpi.setter
    def dpi(self, value):
        self._dpi = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET dpi = ?
        WHERE configuration_id = ?;
        """, (self._dpi, self.configuration_id))

        conn.commit()
        conn.close()

    @property
    def smartshift_threshold(self):
        return self._smartshift_threshold

    @smartshift_threshold.setter
    def smartshift_threshold(self, value):

        self._smartshift_threshold = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET smartshift_threshold = ?
        WHERE configuration_id = ?;
        """, (self._smartshift_threshold, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def smartshift_torque(self):
        return self._smartshift_torque

    @smartshift_torque.setter
    def smartshift_torque(self, value):
        
        self._smartshift_torque = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET smartshift_torque = ?
        WHERE configuration_id = ?;
        """, (self._smartshift_torque, self.configuration_id))

        conn.commit()
        conn.close()


    @property
    def configuration_name(self):
        return self._configuration_name

    @configuration_name.setter
    def configuration_name(self, value):
        
        self._configuration_name = value

        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        UPDATE Configurations
        SET configuration_name = ?
        WHERE configuration_id = ?;
        """, (self._configuration_name, self.configuration_id))

        conn.commit()
        conn.close()








def get_device_config(configuration_id):

    conn, cursor = execute_db_queries.create_db_connection()


    cursor.execute("""
    SELECT *
    FROM Configurations AS C
    JOIN Devices AS D ON C.device_id = D.device_id
    WHERE C.configuration_id = ?;

                    """, (configuration_id,))


    configuration_query_result = cursor.fetchone()

    configuration_id, device_id, configuration_name, date_configuration_added, date_configuration_last_modified, is_selected, \
    dpi, smartshift_on, smartshift_threshold, smartshift_torque, hiresscroll_hires, hiresscroll_invert, hiresscroll_target, \
    thumbwheel_divert, thumbwheel_invert, configuration_id, device_name, is_user_device, config_file_device_name, device_pids, \
    min_dpi, max_dpi, default_dpi, has_scrollwheel, has_thumbwheel, thumbwheel_tap_support, thumbwheel_proxy_support, \
    thumbwheel_touch_support, thumbwheel_timestamp_support, smartshift_support, hires_scroll_support, number_of_sensors, \
    date_device_added, date_device_last_edited, is_activated = configuration_query_result

    buttons = []


    cursor.execute("""
    SELECT *
    FROM Buttons
    WHERE device_id = ?
                    """, (device_id,))

    device_buttons = cursor.fetchall()

    # print(device_buttons)




    configuration = DeviceConfig(
                                    device_id=device_id,
                                    device_name=device_name,
                                    is_user_device=is_user_device,
                                    date_device_added=date_device_added,
                                    date_device_last_edited=date_device_last_edited,
                                    buttons=buttons,
                                    min_dpi=min_dpi,
                                    max_dpi=max_dpi,
                                    default_dpi=default_dpi,
                                    has_scrollwheel =bool(has_scrollwheel),
                                    smartshift_support = bool(smartshift_support),
                                    hires_scroll_support = bool(hires_scroll_support),
                                    has_thumbwheel = bool(has_thumbwheel),
                                    thumbwheel_tap_support = bool(thumbwheel_tap_support),
                                    thumbwheel_proxy_support = bool(thumbwheel_proxy_support),
                                    thumbwheel_touch_support = bool(thumbwheel_touch_support),
                                    thumbwheel_timestamp_support = bool(thumbwheel_timestamp_support),
                                    number_of_sensors=number_of_sensors,
                                    is_activated=is_activated,
                                    configuration_id=configuration_id,
                                    configuration_name=configuration_name,
                                    date_configuration_added=date_configuration_added,
                                    date_configuration_last_modified=date_configuration_last_modified,
                                    is_selected=is_selected,
                                    dpi=dpi,
                                    smartshift_on=smartshift_on,
                                    smartshift_threshold=smartshift_threshold,
                                    smartshift_torque=smartshift_torque,
                                    hiresscroll_hires=hiresscroll_hires,
                                    hiresscroll_invert=hiresscroll_invert,
                                    hiresscroll_target=hiresscroll_target,
                                    thumbwheel_divert=bool(thumbwheel_divert),
                                    thumbwheel_invert=bool(thumbwheel_invert),

    )

    execute_db_queries.close_without_committing_changes(conn)

    return configuration





def get_main_page_user_devices():
    conn, cursor = execute_db_queries.create_db_connection()

    cursor.execute("""
        SELECT device_id, device_name, is_activated
        FROM Devices
        WHERE is_user_device = 1
        ORDER BY date_added DESC
                   """)

    devices = cursor.fetchall()

    user_devices_objects = []
    for device in devices:

        device_id, device_name, is_activated = device


        cursor.execute("""
            SELECT configuration_id, configuration_name, is_selected
            FROM Configurations
            WHERE device_id = ?
            ORDER BY date_added DESC
        """, (device_id,))

        configs_data = cursor.fetchall()
        # print(configs_data)

        configs = []

        for config_data in configs_data:
        
            config_id, configuration_name, is_selected = config_data
            
            user_config = Configuration(configuration_id=config_id, configuration_name=configuration_name, is_selected=is_selected)

            configs.append(user_config)


        user_device = UserDevice(device_id, device_name, is_activated, configs)
        user_devices_objects.append(user_device)

    execute_db_queries.close_without_committing_changes(conn)
    return user_devices_objects









class Gesture:
    def __init__(
            self,
            gesture_id,
            button_config_id,
            direction,
            gesture_action,
            gesture_mode,
            gesture_threshold

    ):
        self.gesture_id = gesture_id
        self.button_config_id = button_config_id
        self.direction = direction
        self.gesture_action = gesture_action
        self.gesture_mode = gesture_mode
        self.gesture_threshold = gesture_threshold



class Action:
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            origin,
            action_id,
            is_selected,
    ):
    # Actions that have no futher configuration other than on or off
    # Default
    # NoPress
    # ToggleSmartShift
    # ToggleHiresScroll
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.origin = origin
        self.action_id = action_id
        self.is_selected = is_selected

class DefaultAction(Action):
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            is_selected,
    ):
        super.__init__(
            device_id,
            button_id,
            configuration_id,
            is_selected
        )

class NoPress(Action):
    def __init__(
            self,
            device_id,


            button_id,
            configuration_id,
            is_selected,
    ):
        super.__init__(
            device_id,
            button_id,
            configuration_id,
            is_selected
        )

class ToggleSmartShift(Action):
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            is_selected,
    ):
        super.__init__(
            device_id,
            button_id,
            configuration_id,
            is_selected
        )



class ToggleHiresScroll(Action):
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            is_selected,
    ):
        super.__init__(
            device_id,
            button_id,
            configuration_id,
            is_selected
        )




# TODO these subclasses of the above class if possible
class Keypress(Action):
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
        action_type,
        keypresses
    ):
        super().__init__(
            button_config_id,
            device_id,
            button_id,
            configuration_id,
            is_selected,
            action_type = "Keypresses"
        )
        self.action_type = action_type
        self.keypresses = keypresses


class Axis(Action):
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
        action_id,
        axis_id,
        axis_button,
        axis_multiplier

    ):
        super().__init__(
            button_config_id,
            device_id,
            button_id,
            configuration_id,
            is_selected,
            action_type = "Keypresses"
        )
        self.action_type = action_type


        self.button_config_id = button_config_id
        self.device_id = device_id
        self.button_id = button_id
        self.configuration_id = configuration_id
        self.is_selected = is_selected


        self.action_id = action_id
        self.axis_id = axis_id
        self.axis_button = axis_button
        self.axis_multiplier = axis_multiplier

class CycleDPI:
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
        action_id,
        cycle_dpi_id,
        dpi_array,
        sensor

    ):
        self.button_config_id = button_config_id
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.is_selected = is_selected

        self.action_id = action_id

        self.cycle_dpi_id = cycle_dpi_id
        self.dpi_array = dpi_array
        self.sensor = sensor



class ChangeHost:
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
        action_id,
        host_change

    ):
        self.button_config_id = button_config_id
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.is_selected = is_selected

        self.action_id = action_id

        self.host_change = host_change



def main():
    pass
    # x = get_device_config(2)
    # test(x)
    # config = DeviceConfig.create_from_configuration_id(1)
    # print(f"{config.configuration_id}, {config.configuration_name}, {config.smartshift_on}")


if __name__ == "__main__":
    main()




