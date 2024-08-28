import execute_db_queries
import re


class Keypress():
    def __init__(
        self,
        keypress_id,
        keypresses,
    ):
        self.keypress_id = keypress_id
        self.keypresses = keypresses

    @staticmethod
    def fetch_using_action_id_and_source_table(action_id, source_table, conn, cursor):
        cursor.execute("""SELECT keypress_id, keypresses
                        FROM Keypresses
                        WHERE AND action_id = ? AND source_table = ?
                        """, (action_id, source_table))
        return cursor.fetchone()[0]

    

class ButtonKeypress(Keypress):
    def __init__(self, keypress_id, keypresses, button_config_id):
        super().__init__(keypress_id, keypresses)
        self.button_config_id = button_config_id



class Keypresses1:
    def __init__(self, keypresses, reference_id, reference_id_type, keypress_id=None):
        self.keypresses = keypresses
        self.reference_id = reference_id
        self.reference_id_type = reference_id_type
        self.keypress_id = keypress_id

    @classmethod
    def fetch_all(cls, reference_ids, reference_id_type, conn, cursor):
        instances = {}
        for reference_id in reference_ids:
            cursor.execute("""SELECT keypresses
                              FROM Keypresses
                              WHERE action_id = ? AND source_table = ?""",
                           (reference_id[0], reference_id_type))
            row = cursor.fetchone()
            if row:
                keypresses = row[0]
                instance = cls(keypresses, reference_id[0], reference_id_type)
                instances[reference_id[0]] = instance
        return instances


class ScrollKeypress(Keypress):
    def __init__(self, keypress_id, keypresses):
        super().__init__(keypress_id, keypresses)
    
    @classmethod
    def fetch_scroll_keypress(cls, scroll_action_id, conn, cursor):
        cls.fetch_using_action_id_and_source_table(action_id=scroll_action_id, source_table="ScrollActions", conn=conn, cursor=cursor)
        

class CycleDPI:
    def __init__(
        self,
        cycle_dpi_id,
        dpi_array,
        sensor=None,
        button_config_id=None,
    ):
        self.cycle_dpi_id = cycle_dpi_id
        self.dpi_array = dpi_array
        self.sensor = sensor
        self.button_config_id = button_config_id

    @staticmethod
    def fetch_using_action_id_and_source_table(action_id, source_table, conn, cursor):

        cursor.execute("""SELECT cycle_dpi_id, dpi_array
                        FROM CycleDPI
                        WHERE action_id = ? AND source_table = ?
                        """, (action_id, source_table))
        return cursor.fetchone()


class ScrollCycleDPI(CycleDPI):
    def __init__(self, cycle_dpi_id, dpi_array):
        super().__init__(cycle_dpi_id, dpi_array)
    
    @classmethod
    def fetch_scroll_cycledpi(cls, action_id, conn, cursor):
        cls.reference_id = action_id
        cls.cycle_dpi_id, cls.dpi_array = cls.fetch_using_action_id_and_source_table(action_id=action_id, source_table="ScrollActions", conn=conn, cursor=cursor)
        return cls


class ChangeDPI:
    def __init__(
            self,
            change_dpi_id,
            increment,
            button_config_id=None
    ):
        self.change_dpi_id = change_dpi_id
        self.increment = increment
        self.button_config_id = button_config_id

    @staticmethod
    def fetch_using_action_id_and_source_table(action_id, source_table, conn, cursor):

        cursor.execute("""
                            SELECT change_dpi_id, increment
                            FROM ChangeDPI
                        WHERE action_id = ? AND source_table = ?
                        """, (action_id, source_table))
        return cursor.fetchone()[0]
    




class CycleDPI1:
    def __init__(
        self,
        dpi_array,
        reference_id,
        reference_id_type,
        cycle_dpi_id=None,
        sensor=None,
    ):
        self.dpi_array = dpi_array
        self.reference_id = reference_id
        self.reference_id_type = reference_id_type
        self.cycle_dpi_id = cycle_dpi_id
        self.sensor = sensor


    @classmethod
    def fetch_all(cls, reference_ids, reference_id_type, conn, cursor):
        instances = {}
        for reference_id in reference_ids:

            cursor.execute("""SELECT dpi_array
                            FROM CycleDPI
                            WHERE action_id = ? AND source_table = ?""",
                           (reference_id[0], reference_id_type))
            row = cursor.fetchone()
            if row:
                dpi_array = row[0]
                instance = cls(dpi_array, reference_id[0], reference_id_type)
                instances[reference_id[0]] = instance
        return instances



class ChangeDPI1:
    def __init__(self, increment, reference_id, reference_id_type):
        self.increment = increment
        self.reference_id = reference_id
        self.reference_id_type = reference_id_type


    @classmethod
    def fetch_all(cls, reference_ids, reference_id_type, conn, cursor):
        instances = {}
        for reference_id in reference_ids:
            cursor.execute("""SELECT increment
                           FROM ChangeDPI
                           WHERE action_id = ? AND source_table = ?""",
                           (reference_id[0], reference_id_type))
            row = cursor.fetchone()
            if row:
                instance = cls(row[0], reference_id[0], reference_id_type)
                instances[reference_id[0]] = instance
        return instances





# class GestureDict(dict):
#     def __init__(self, button, button_config_id, configuration):
#         super().__init__()
#         self.button = button
#         self.configuration = configuration
#         self.button_config_id = button_config_id
#         self.gesture_directions = {}

#     def __getitem__(self, key):
#         return self.gesture_directions[key]

#     def __setitem__(self, key, value):
#         self.gesture_directions[key] = value

#     def __repr__(self):
#         return repr(self.gesture_directions)

#     @classmethod
#     def create_object(cls, button, button_config_id, configuration, conn, cursor):
#         instance = cls(button, button_config_id, configuration)

#         for direction in ["Up", "Down", "Left", "Right", "None"]:
#             cursor.execute("""
#                 SELECT threshold, mode 
#                 FROM GestureProperties
#                 WHERE button_config_id = ? AND direction = ?
#             """, (button_config_id, direction))

#             threshold, mode = cursor.fetchone()

#             cursor.execute("""
#                 SELECT gesture_id FROM Gestures WHERE button_config_id = ? AND direction = ? AND is_selected = 1
#             """, (button_config_id, direction))

#             selected_action_id = cursor.fetchone()[0]

#             def select_single_actions(action_type):
#                 cursor.execute("""
#                     SELECT gesture_id FROM Gestures WHERE button_config_id = ? AND direction = ? AND action_type = ?
#                 """, (button_config_id, direction, action_type))
#                 result = cursor.fetchone()
#                 return result[0] if result is not None else None

#             nopress = select_single_actions("NoPress")
#             togglesmartshift = select_single_actions("ToggleSmartShift")
#             togglehiresscroll = select_single_actions("ToggleHiresScroll")

#             def get_multiple_values(action_type):
#                 cursor.execute("""
#                     SELECT gesture_id FROM Gestures WHERE button_config_id = ? AND direction = ? AND action_type = ?
#                 """, (button_config_id, direction, action_type))
#                 return cursor.fetchall()

#             keypresses = Keypresses1.fetch_all(
#                 reference_ids=get_multiple_values("Keypress"),
#                 reference_id_type="TouchTapProxy",
#                 conn=conn, cursor=cursor
#             )
#             cycledpi = CycleDPI1.fetch_all(
#                 reference_ids=get_multiple_values("CycleDPI"),
#                 reference_id_type="TouchTapProxy",
#                 conn=conn, cursor=cursor
#             )
#             changehost = ChangeHost1.fetch_all(
#                 reference_ids=get_multiple_values("ChangeHost"),
#                 reference_id_type="TouchTapProxy",
#                 conn=conn, cursor=cursor
#             )
#             changedpi = ChangeDPI1.fetch_all(
#                 reference_ids=get_multiple_values("ChangeDPI"),
#                 reference_id_type="TouchTapProxy",
#                 conn=conn, cursor=cursor
#             )
#             axes = Axis1.fetch_all(
#                 reference_ids=get_multiple_values("Axes"),
#                 reference_id_type="TouchTapProxy",
#                 conn=conn, cursor=cursor
#             )

#             instance[direction] = GestureSettings1(
#                 direction, button, configuration, threshold, mode, selected_action_id, nopress,
#                 togglesmartshift, togglehiresscroll, keypresses, axes, changehost, cycledpi, changedpi
#             )
#         return instance



class GestureDict(dict):
    def __init__(self, button, button_config_id, configuration):
        super().__init__()
        self.button = button
        self.configuration = configuration
        self.button_config_id = button_config_id

    @classmethod
    def create_object(cls, button, button_config_id, configuration, conn, cursor):
        instance = cls(button, button_config_id, configuration)

        for direction in ["Up", "Down", "Left", "Right", "None"]:
            cursor.execute("""
                SELECT threshold, mode 
                FROM GestureProperties
                WHERE button_config_id = ? AND direction = ?
            """, (button_config_id, direction))

            threshold, mode = cursor.fetchone()

            cursor.execute("""
                SELECT gesture_id FROM Gestures WHERE button_config_id = ? AND direction = ? AND is_selected = 1
            """, (button_config_id, direction))

            selected_action_id = cursor.fetchone()[0]

            def select_single_actions(action_type):
                cursor.execute("""
                    SELECT gesture_id FROM Gestures WHERE button_config_id = ? AND direction = ? AND action_type = ?
                """, (button_config_id, direction, action_type))
                result = cursor.fetchone()
                return result[0] if result is not None else None

            nopress = select_single_actions("NoPress")
            togglesmartshift = select_single_actions("ToggleSmartShift")
            togglehiresscroll = select_single_actions("ToggleHiresScroll")

            def get_multiple_values(action_type):
                cursor.execute("""
                    SELECT gesture_id FROM Gestures WHERE button_config_id = ? AND direction = ? AND action_type = ?
                """, (button_config_id, direction, action_type))
                return cursor.fetchall()

            keypresses = Keypresses1.fetch_all(
                reference_ids=get_multiple_values("Keypress"),
                reference_id_type="Gestures",
                conn=conn, cursor=cursor
            )
            cycledpi = CycleDPI1.fetch_all(
                reference_ids=get_multiple_values("CycleDPI"),
                reference_id_type="Gestures",
                conn=conn, cursor=cursor
            )
            changehost = ChangeHost1.fetch_all(
                reference_ids=get_multiple_values("ChangeHost"),
                reference_id_type="Gestures",
                conn=conn, cursor=cursor
            )
            changedpi = ChangeDPI1.fetch_all(
                reference_ids=get_multiple_values("ChangeDPI"),
                reference_id_type="Gestures",
                conn=conn, cursor=cursor
            )
            axes = Axis1.fetch_all(
                reference_ids=get_multiple_values("Axis"),
                reference_id_type="Gestures",
                conn=conn, cursor=cursor
            )

            instance[direction] = GestureSettings1(
                direction, button, configuration, threshold, mode, selected_action_id, nopress,
                togglesmartshift, togglehiresscroll, keypresses, axes, changehost, cycledpi, changedpi
            )
        return instance



class GestureSettings1:
    def __init__(self,
                direction,
                button,
                configuration,
                threshold,
                mode,
                selected_action_id,
                nopress,
                togglesmartshift,
                togglehiresscroll,
                keypresses,
                axes,
                changehost,
                cycledpi,
                changedpi,
                default=None
                 ):
        self.direction=direction
        self.button=button
        self.configuration=configuration
        self.config_object = configuration
        self.threshold=threshold
        self.mode=mode
        self.selected_action_id=selected_action_id
        self.nopress=nopress
        self.togglesmartshift=togglesmartshift
        self.togglehiresscroll=togglehiresscroll
        self.keypresses=keypresses
        self.axes=axes
        self.changehost=changehost
        self.cycledpi=cycledpi
        self.changedpi=changedpi
        self.default = None

    def update_selected(self, new_selected_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE Gestures SET is_selected = 1 WHERE gesture_id = ?""", (new_selected_id,))
        execute_db_queries.commit_changes_and_close(conn)
        self.selected_action_id = new_selected_id

    def update_threshold(self, new_threshold):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                        UPDATE GestureProperties
                       SET threshold = ?
                       WHERE button_config_id = ?
                       AND direction = ?
                        """, (new_threshold, self.button.gestures.button_config_id, self.direction))
        execute_db_queries.commit_changes_and_close(conn)
        self.threshold = new_threshold

    def update_mode(self, new_mode):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                        UPDATE GestureProperties
                       SET mode = ?
                       WHERE button_config_id = ?
                       AND direction = ?
                        """, (new_mode, self.button.gestures.button_config_id, self.direction))
        execute_db_queries.commit_changes_and_close(conn)
        self.mode = new_mode

    def get_added_order(self):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""SELECT gesture_id FROM Gestures WHERE button_config_id = ? AND direction = ? AND date_added IS NOT NULL ORDER BY date_added;""",(self.button.gestures.button_config_id, self.direction))
        result = cursor.fetchall()
        execute_db_queries.close_without_committing_changes(conn)
        return [i[0] for i in result]

    def add_new_keypress_action(self, keypresses):
        new_gesture_id, conn, cursor = self.add_action("Keypress")
        cursor.execute("""UPDATE Keypresses SET keypresses = ? WHERE action_id = ? AND source_table = 'Gestures'""", (keypresses, new_gesture_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.keypresses[new_gesture_id] = Keypresses1(keypresses=keypresses, reference_id=new_gesture_id, reference_id_type="Gestures")
        return self.keypresses[new_gesture_id]
    def delete_keypress_action(self, action_id):
        self.delete_action(action_id)
        del self.keypresses[action_id]

    def add_new_axis_action(self, axis, axis_multiplier):
        new_gesture_id, conn, cursor = self.add_action("Axis")
        cursor.execute("""UPDATE Axes SET axis_button = ?, axis_multiplier = ? WHERE action_id = ? AND source_table = 'Gestures'""", (axis, axis_multiplier, new_gesture_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.axes[new_gesture_id] = Axis1(axis_button=axis, axis_multiplier=axis_multiplier, reference_id=new_gesture_id, reference_id_type="Gestures")
        return self.axes[new_gesture_id]
    def delete_axis_action(self, action_id):
        self.delete_action(action_id)
        del self.axes[action_id]

    def add_new_changehost_action(self, host_change):
        new_gesture_id, conn, cursor = self.add_action("ChangeHost")
        cursor.execute("""UPDATE ChangeHost Set host_change = ? WHERE action_id = ? AND source_table = 'Gestures'""", (host_change, new_gesture_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.changehost[new_gesture_id] = ChangeHost1(host_change=host_change, reference_id=new_gesture_id, reference_id_type="Gestures")
        return self.changehost[new_gesture_id]
    def delete_changehost_action(self, action_id):
        self.delete_action(action_id)
        del self.changehost[action_id]

    def add_new_changedpi_action(self, new_value):
        new_gesture_id, conn, cursor = self.add_action("ChangeDPI")
        cursor.execute("""UPDATE ChangeDPI Set increment = ? WHERE action_id = ? AND source_table = 'Gestures'""", (new_value, new_gesture_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.changedpi[new_gesture_id] = ChangeDPI1(increment=new_value, reference_id=new_gesture_id, reference_id_type="Gestures")
        return self.changedpi[new_gesture_id]
    def delete_cycledpi_action(self, action_id):
        self.delete_action(action_id)
        del self.cycledpi[action_id]

    def add_new_cycledpi_action(self, dpi_array):
        new_gesture_id, conn, cursor = self.add_action("CycleDPI")
        cursor.execute("""UPDATE CycleDPI SET dpi_array = ? WHERE action_id = ? AND source_table = 'Gestures'""", (dpi_array, new_gesture_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.cycledpi[new_gesture_id] = CycleDPI1(dpi_array=dpi_array, reference_id=new_gesture_id, reference_id_type="Gestures")
        return self.cycledpi[new_gesture_id]
    def delete_changedpi_action(self, action_id):
        self.delete_action(action_id)
        del self.changedpi[action_id]

    def delete_action(self, action_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""DELETE FROM Gestures WHERE gesture_id = ?""",(action_id,))
        execute_db_queries.commit_changes_and_close(conn)

    def add_action(self, action_type):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""INSERT INTO Gestures (button_config_id, direction, action_type) VALUES (?, ?, ?)""",(self.button.gestures.button_config_id, self.direction, action_type))
        cursor.execute(
            """
            SELECT last_insert_rowid();
            """
            )
        return cursor.fetchone()[0], conn, cursor

    def request_selected_type(self):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
            SELECT action_type   
            FROM Gestures
            WHERE gesture_id = ?
""", (self.selected_action_id,))
        selected = cursor.fetchone()[0]
        execute_db_queries.close_without_committing_changes(conn)
        return selected


class GestureSettings():
    def __init__(
        self,
        button_config_id,
        gesture_property_id,
        selected_gesture_id,
        threshold=None,
        mode=None,
        gesture_changehost = {},
        gesture_cycledpi = {},
        gesture_changedpi = {},
        gesture_axes = {},
        gesture_keypresses={},
        gesture_nopress = None,
        gesture_togglesmartshift = None,
        gesture_togglehiresscroll = None,
    ):
        self.button_config_id = button_config_id
        self.gesture_property_id = gesture_property_id
        self.selected_gesture_id = selected_gesture_id
        self.threshold = threshold
        self.mode = mode 
        self.gesture_changehost = gesture_changehost 
        self.gesture_cycledpi = gesture_cycledpi 
        self.gesture_changedpi = gesture_changedpi 
        self.gesture_axes = gesture_axes 
        self.gesture_nopress = gesture_nopress 
        self.gesture_togglesmartshift = gesture_togglesmartshift 
        self.gesture_togglehiresscroll = gesture_togglehiresscroll 
        self.gesture_keypresses = gesture_keypresses
        

    @classmethod
    def create_object(cls, cursor, button_config_id, direction):
        
        gesture = cls(cursor, button_config_id, direction,)
        gesture.direction = direction

        cursor.execute("""
                        SELECT gesture_property_id, threshold, mode 
                        FROM GestureProperties
                        WHERE button_config_id = ? AND direction = ?
                    """, (button_config_id, direction))

        gesture.gesture_property_id, gesture.threshold, gesture.mode = cursor.fetchone()

        one_config_values = {"NoPress":None, "ToggleHiresScroll":None, "ToggleSmartShift":None}
        for key in one_config_values:
            cursor.execute("""
                        SELECT gesture_id
                        FROM Gestures
                        WHERE button_config_id = ? AND action_type = ? AND direction = ?
            """, (button_config_id, key, direction))
            result = cursor.fetchone()

            if result:
                one_config_values[key] = result[0]


        gesture.gesture_nopress = one_config_values["NoPress"]
        gesture.gesture_togglehiresscroll = one_config_values["ToggleHiresScroll"]
        gesture.gesture_togglesmartshift = one_config_values["ToggleSmartShift"]

        gesture.gesture_keypresses = {}
        cursor.execute("""
                        SELECT 
                            Gestures.gesture_id,
                            Keypresses.keypress_id,
                            Keypresses.keypresses
                        FROM
                            Gestures
                        JOIN 
                            Keypresses ON Keypresses.action_id = Gestures.gesture_id
                        WHERE
                            Gestures.button_config_id = ?
                            AND
                            direction = ?
                            AND
                            action_type = 'Keypress' 
                        """, (button_config_id, direction))
        keypress_list = cursor.fetchall()
        if len(keypress_list) != 0:
            for i in keypress_list:
                gesture.gesture_keypresses[i[0]] = ButtonKeypress(button_config_id=i[0], keypress_id=i[1], keypresses=i[2])



        gesture.gesture_changehost = {}
        cursor.execute("""
                        SELECT
                            Gestures.gesture_id,
                            ChangeHost.host_id,
                            ChangeHost.host_change
                        FROM
                            Gestures
                        JOIN
                            ChangeHost ON ChangeHost.action_id = Gestures.gesture_id
                        WHERE
                            Gestures.button_config_id = ?
                            AND
                            direction = ?
                            AND
                            action_type = 'ChangeHost' 
                        """, (button_config_id, direction))
        changehost_list = cursor.fetchall()
        if len(changehost_list) != 0:
            for i in changehost_list:
                gesture.gesture_changehost[i[0]] = ChangeHost(button_config_id=i[0], host_id=i[1], host_change=i[2])



        gesture.gesture_changedpi = {}
        cursor.execute("""
                        SELECT
                            Gestures.gesture_id,
                            ChangeDPI.change_dpi_id,
                            ChangeDPI.increment
                        FROM
                            Gestures
                        JOIN
                            ChangeDPI ON ChangeDPI.action_id = Gestures.gesture_id
                        WHERE
                            Gestures.button_config_id = ?
                            AND
                            direction = ?
                            AND
                            action_type = 'ChangeDPI' 
                        """, (button_config_id, direction))
        changedpi_list = cursor.fetchall()
        if len(changedpi_list) != 0:
            for i in changedpi_list:
                gesture.gesture_changedpi[i[0]] = ChangeDPI(button_config_id=i[0], change_dpi_id=i[1], increment=i[2])




        gesture.gesture_cycledpi = {}
        cursor.execute("""
                        SELECT
                            Gestures.gesture_id,
                            CycleDPI.cycle_dpi_id,
                            CycleDPI.dpi_array
                        FROM
                            Gestures
                        JOIN
                            CycleDPI ON CycleDPI.action_id = Gestures.gesture_id
                        WHERE
                            Gestures.button_config_id = ?
                            AND
                            direction = ?
                            AND
                            action_type = 'CycleDPI' 
                        """, (button_config_id, direction))
        cycledpi_list = cursor.fetchall()
        if len(cycledpi_list) != 0:
            for i in cycledpi_list:
                gesture.gesture_cycledpi[i[0]] = CycleDPI(button_config_id=i[0], cycle_dpi_id=i[1], dpi_array=i[2])



        gesture.gesture_axes = {}

        cursor.execute("""
                        SELECT
                            Gestures.gesture_id,
                            Axes.axis_id,
                            Axes.axis_button,
                            Axes.axis_multiplier
                        FROM
                            Gestures
                        JOIN
                            Axes ON Axes.action_id = Gestures.gesture_id
                        WHERE 
                            Gestures.button_config_id = ?
                            AND
                            direction = ?
                            AND
                            action_type = 'Axis' 
                        """, (button_config_id, direction))
        axes_list = cursor.fetchall()
        if len(axes_list) != 0:
            for i in axes_list:
                gesture.gesture_axes[i[0]] = Axis(button_config_id=i[0], axis_id=i[1], axis_button=i[2], axis_multiplier=i[3])


        cursor.execute("""
                        SELECT gesture_id
                        FROM Gestures
                        WHERE is_selected = 1
                        AND button_config_id = ?
                        AND direction = ?
                        """, (button_config_id, direction))

        gesture.selected_gesture_id = cursor.fetchone()[0]
        gesture.button_config_id = button_config_id

        return gesture

    def delete_keypresses(self, gesture_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                    DELETE FROM Gestures
                    WHERE gesture_id = ?;
                        """, (gesture_id,))

        execute_db_queries.commit_changes_and_close(conn)
        del self.gesture_keypresses[gesture_id]

    def add_action(self, cursor, action_type):
        cursor.execute(""" INSERT INTO Gestures (button_config_id, direction, action_type)
                        VALUES (?, ?, ?) """, (self.button_config_id, self.direction, action_type))
        
        cursor.execute("""SELECT last_insert_rowid();""")
        return cursor.fetchone()[0]

    def add_new_cycledpi(self, dpi_array):

        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_gesture_id = self.add_action(cursor=cursor, action_type="CycleDPI")

        cursor.execute(
            """
            UPDATE CycleDPI
            SET dpi_array = ?
            WHERE action_id = ? and source_table = "Gestures";
            """, (dpi_array, inserted_row_gesture_id))
        
        cursor.execute("""
                        SELECT cycle_dpi_id
                        FROM CycleDPI
                        WHERE action_id = ? AND source_table = 'Gestures';
                        """, (inserted_row_gesture_id,))
        new_cycledpi_id = cursor.fetchone()[0]
        self.gesture_cycledpi[inserted_row_gesture_id] = CycleDPI(button_config_id=inserted_row_gesture_id, cycle_dpi_id=new_cycledpi_id, dpi_array=dpi_array)
        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_gesture_id


    def update_threshold(self, new_threshold):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                        UPDATE GestureProperties
                       SET threshold = ?
                       WHERE gesture_property_id = ?
                        """, (new_threshold, self.gesture_property_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.threshold = new_threshold

    def update_mode(self, new_mode):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                        UPDATE GestureProperties
                       SET mode = ?
                       WHERE gesture_property_id = ?
                        """, (new_mode, self.gesture_property_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.mode = new_mode

    def add_new_axis(self, axis, axis_multiplier):

        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="Axis")

        cursor.execute(
            """
            UPDATE Axes
            SET axis_button = ?, axis_multiplier = ?
            WHERE action_id = ? and source_table = "Gestures";
            """, (axis, axis_multiplier, inserted_row_button_config_id))
        
        cursor.execute(
            """
            SELECT axis_id
            FROM Axes
            WHERE action_id = ? AND source_table = 'Gestures';
            """, (inserted_row_button_config_id,))
        
        new_axis_id = cursor.fetchone()[0]
        self.gesture_axes[inserted_row_button_config_id] = Axis(button_config_id=inserted_row_button_config_id, axis_id=new_axis_id, axis_button=axis, axis_multiplier=axis_multiplier)
        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_button_config_id


    def add_new_changedpi(self, increment):

        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="ChangeDPI")

        cursor.execute(
            """
            UPDATE ChangeDPI
            SET increment = ?
            WHERE action_id = ? and source_table = "Gestures";
            """, (increment, inserted_row_button_config_id))
        
        cursor.execute(
            """
            SELECT change_dpi_id
            FROM ChangeDPI
            WHERE action_id = ? AND source_table = 'Gestures';
            """, (inserted_row_button_config_id,))
        
        new_changedpi_id = cursor.fetchone()[0]
        self.gesture_changedpi[inserted_row_button_config_id] = ChangeDPI(button_config_id=inserted_row_button_config_id, change_dpi_id=new_changedpi_id, increment=increment)
        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_button_config_id


    def add_new_changehost(self, host):
        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="ChangeHost")

        cursor.execute(
            """
            UPDATE ChangeHost
            SET host_change = ?
            WHERE action_id = ? and source_table = 'Gestures';
            """, ("prev" if host == "Previous" else "next" if host == "Next" else host, inserted_row_button_config_id))

        cursor.execute("""
            SELECT host_id
            FROM ChangeHost
            WHERE action_id = ? AND source_table = 'Gestures';
            """, (inserted_row_button_config_id,))
        
        new_changehost_id = cursor.fetchone()[0]
        self.gesture_changehost[inserted_row_button_config_id] = ChangeHost(button_config_id=inserted_row_button_config_id, host_id=new_changehost_id, host_change=host)
        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_button_config_id

    def add_new_keypress_action(self, keypresses):
        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="Keypress")

        cursor.execute("""
            UPDATE Keypresses
            SET keypresses = ?
            WHERE action_id = ? and source_table = 'Gestures';
            """, (keypresses, inserted_row_button_config_id))

        cursor.execute("""
            SELECT keypress_id
            FROM Keypresses
            WHERE action_id = ? AND source_table = 'Gestures';
            """, (inserted_row_button_config_id,))
        
        new_keypress_id = cursor.fetchone()[0]
        self.gesture_keypresses[inserted_row_button_config_id] = ButtonKeypress(button_config_id=inserted_row_button_config_id, keypress_id=new_keypress_id, keypresses=keypresses)
        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_button_config_id

    def request_selected_type(self):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
            SELECT action_type   
            FROM Gestures
            WHERE gesture_id = ?
""", (self.selected_gesture_id,))
        selected = cursor.fetchone()[0]
        execute_db_queries.close_without_committing_changes(conn)
        return selected

class ChangeHost:
    def __init__(
        self,
        host_id,
        host_change,
        button_config_id=None
    ):
        self.host_id = host_id
        self.host_change = host_change
        self.button_config_id = button_config_id

    @classmethod
    def fetch_using_action_id_and_source_table(cls, configuration_id, action_id, source_table):
        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
                            SELECT host_id, host_change
                            FROM ChangeHost
                            WHERE configuration_id = ? AND action_id = ? AND source_table = ?
                        """, (configuration_id, action_id, source_table))
        change_host = cls
        change_host.host_id, change_host.host_change = cursor.fetchone()
        execute_db_queries.close_without_committing_changes(conn)
        return change_host   

class Axis():
    def __init__(
        self,
        axis_id,
        axis_button,
        axis_multiplier,
        button_config_id=None

    ):
        self.axis_id = axis_id
        self.axis_button = axis_button
        self.axis_multiplier = axis_multiplier
        self.button_config_id = button_config_id

    @classmethod
    def fetch_using_action_id_and_source_table(cls, configuration_id, action_id, source_table):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                            SELECT axis_id, axis_button, axis_multiplier
                            FROM Axes
                            WHERE configuration_id = ? AND action_id = ? AND source_table = ?
                            """,(configuration_id, action_id, source_table,))
        axis = cls
        axis.axis_id, axis.axis_button, axis.axis_multiplier = cursor.fetchone()
        execute_db_queries.close_without_committing_changes(conn)
        return axis




class Axis1():
    def __init__(
        self,
        axis_button,
        axis_multiplier,
        reference_id,
        reference_id_type

    ):
        self.axis_button = axis_button
        self.axis_multiplier = axis_multiplier
        self.reference_id = reference_id
        self.reference_id_type = reference_id_type


    @classmethod
    def fetch_all(cls, reference_ids, reference_id_type, conn, cursor):
        instances = {}

        for reference_id in reference_ids:
            cursor.execute("""SELECT axis_button, axis_multiplier                           
                           FROM Axes
                           WHERE action_id = ? AND source_table = ?""",
                           (reference_id[0], reference_id_type))
            row = cursor.fetchone()
            if row:
                axis_button, axis_multiplier = row
                instance = cls(axis_button, axis_multiplier, reference_id[0], reference_id_type)
                instances[reference_id[0]] = instance

        return instances


class ChangeHost1:
    def __init__(
        self,
        host_change,
        reference_id,
        reference_id_type
    ):
        self.host_change = host_change
        self.reference_id = reference_id
        self.reference_id_type = reference_id_type    

    @classmethod
    def fetch_all(cls, reference_ids, reference_id_type, conn, cursor):
        instances = {}
        for reference_id in reference_ids:
            cursor.execute("""SELECT host_change
                           FROM ChangeHost
                           WHERE action_id = ? AND source_table = ?""",
                           (reference_id[0], reference_id_type))
            row = cursor.fetchone()
            if row:
                instance = cls(row[0], reference_id[0], reference_id_type)
                instances[reference_id[0]] = instance

        return instances


























class ScrollActions:
    def __init__(self, scroll_action_property_id, selected_action_id, config_object=None, default = None, nopress = None, togglesmartshift = None, togglehiresscroll = None, keypresses={}, axes={},  changehost = {}, cycledpi = {}, changedpi = {}):
        self.scroll_action_property_id=scroll_action_property_id
        self.selected_action_id = selected_action_id
        self.config_object = config_object
        self.default = default
        self.nopress = nopress
        self.togglesmartshift = togglesmartshift
        self.togglehiresscroll = togglehiresscroll
        self.keypresses = keypresses
        self.axes = axes
        self.changehost = changehost
        self.cycledpi = cycledpi
        self.changedpi = changedpi

    # def update_selected(self, new_selected_id):
    #     conn, cursor = execute_db_queries.create_db_connection()
    #     cursor.execute("""UPDATE ScrollActions SET is_selected = 1 WHERE scroll_action_id = ?""")
    #     execute_db_queries.commit_changes_and_close(conn)
    #     self.selected_action_id = new_selected_id

    @classmethod
    def create_from_scroll_action_property_id(cls, scroll_action_property_id, config_object, conn=None, cursor=None):
        close_db = False
        if cursor is None:
            conn, cursor = execute_db_queries.create_db_connection()
            close_db = True

        cursor.execute("""SELECT scroll_action_id FROM ScrollActions WHERE scroll_action_property_id = ? AND is_selected = 1""", (scroll_action_property_id,))
        selected_action_id = cursor.fetchone()[0]
        config_object = config_object
        def get_one_value(action_type):
            cursor.execute("""SELECT scroll_action_id FROM ScrollActions WHERE scroll_action_property_id = ? AND action_type = ?""", (scroll_action_property_id, action_type))
            result = cursor.fetchone()
            return result[0] if result is not None else None

        default = get_one_value("Default")
        nopress = get_one_value("NoPress")
        togglehiresscroll = get_one_value("ToggleHiresScroll")
        togglesmartshift = get_one_value("ToggleSmartShift")

        def get_multiple_values(action_type):
            cursor.execute("""SELECT scroll_action_id FROM ScrollActions WHERE scroll_action_property_id = ? AND action_type = ?""", (scroll_action_property_id, action_type))
            return cursor.fetchall()


        keypresses=Keypresses1.fetch_all(reference_ids=get_multiple_values("Keypress"), reference_id_type="ScrollActions", conn=conn, cursor=cursor)

        cycledpi=CycleDPI1.fetch_all(reference_ids=get_multiple_values("CycleDPI"), reference_id_type="ScrollActions", conn=conn, cursor=cursor)

        changedpi=ChangeDPI1.fetch_all(reference_ids=get_multiple_values("ChangeDPI"), reference_id_type="ScrollActions", conn=conn, cursor=cursor)

        axes = Axis1.fetch_all(reference_ids=get_multiple_values("Axis"), reference_id_type="ScrollActions", conn=conn, cursor=cursor)

        changehost = ChangeHost1.fetch_all(reference_ids=get_multiple_values("ChangeHost"), reference_id_type="ScrollActions", conn=conn, cursor=cursor)

        if close_db:
            execute_db_queries.close_without_committing_changes(conn)

        return cls(scroll_action_property_id, selected_action_id, config_object, default, nopress, togglesmartshift, togglehiresscroll, keypresses, axes, changehost, cycledpi, changedpi)

    def update_selected(self, new_selected_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE ScrollActions SET is_selected = 1 WHERE scroll_action_id = ?""", (new_selected_id,))
        execute_db_queries.commit_changes_and_close(conn)
        self.selected_action_id = new_selected_id

    def get_added_order(self):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""SELECT scroll_action_id FROM ScrollActions WHERE scroll_action_property_id = ? AND date_added IS NOT NULL ORDER BY date_added;""",(self.scroll_action_property_id,))
        result = cursor.fetchall()
        execute_db_queries.close_without_committing_changes(conn)
        return [i[0] for i in result]

    def add_new_axis_action(self, axis, axis_multiplier):
        new_scroll_action_id, conn, cursor = self.add_action("Axis")
        cursor.execute("""UPDATE Axes SET axis_button = ?, axis_multiplier = ? WHERE action_id = ? AND source_table = 'ScrollActions'""", (axis, axis_multiplier, new_scroll_action_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.axes[new_scroll_action_id] = Axis1(axis_button=axis, axis_multiplier=axis_multiplier, reference_id=new_scroll_action_id, reference_id_type="ScrollActions")
        return self.axes[new_scroll_action_id]

    def add_new_changehost_action(self, host_change):
        new_scroll_action_id, conn, cursor = self.add_action("ChangeHost")
        cursor.execute("""UPDATE ChangeHost Set host_change = ? WHERE action_id = ? AND source_table = 'ScrollActions'""", (host_change, new_scroll_action_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.changehost[new_scroll_action_id] = ChangeHost1(host_change=host_change, reference_id=new_scroll_action_id, reference_id_type="ScrollActions")
        return self.changehost[new_scroll_action_id]

    def add_new_changedpi_action(self, new_value):
        new_scroll_action_id, conn, cursor = self.add_action("ChangeDPI")
        cursor.execute("""UPDATE ChangeDPI Set increment = ? WHERE action_id = ? AND source_table = 'ScrollActions'""", (new_value, new_scroll_action_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.changedpi[new_scroll_action_id] = ChangeDPI1(increment=new_value, reference_id=new_scroll_action_id, reference_id_type="ScrollActions")
        return self.changedpi[new_scroll_action_id]

    def add_new_keypress_action(self, keypresses):
        new_scroll_action_id, conn, cursor = self.add_action("Keypress")
        cursor.execute("""UPDATE Keypresses SET keypresses = ? WHERE action_id = ? AND source_table = 'ScrollActions'""", (keypresses, new_scroll_action_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.keypresses[new_scroll_action_id] = Keypresses1(keypresses=keypresses, reference_id=new_scroll_action_id, reference_id_type="ScrollActions")
        return self.keypresses[new_scroll_action_id]

    def add_new_cycledpi_action(self, dpi_array):
        new_scroll_action_id, conn, cursor = self.add_action("CycleDPI")
        cursor.execute("""UPDATE CycleDPI SET dpi_array = ? WHERE action_id = ? AND source_table = 'ScrollActions'""", (dpi_array, new_scroll_action_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.cycledpi[new_scroll_action_id] = CycleDPI1(dpi_array=dpi_array, reference_id=new_scroll_action_id, reference_id_type="ScrollActions")
        return self.cycledpi[new_scroll_action_id]


    def delete_keypress_action(self, action_id):
        self.delete_action(action_id)
        del self.keypresses[action_id]

    def delete_axis_action(self, action_id):
        self.delete_action(action_id)
        del self.axes[action_id]

    def delete_changehost_action(self, action_id):
        self.delete_action(action_id)
        del self.changehost[action_id]

    def delete_cycledpi_action(self, action_id):
        self.delete_action(action_id)
        del self.cycledpi[action_id]

    def delete_changedpi_action(self, action_id):
        self.delete_action(action_id)
        del self.changedpi[action_id]


    def delete_action(self, action_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""DELETE FROM ScrollActions WHERE scroll_action_id = ?""",(action_id,))
        execute_db_queries.commit_changes_and_close(conn)

    def add_action(self, action_type):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""INSERT INTO ScrollActions (scroll_action_property_id, action_type) VALUES (?, ?)""",(self.scroll_action_property_id, action_type))

        cursor.execute(
            """
            SELECT last_insert_rowid();
            """
            )
        return cursor.fetchone()[0], conn, cursor



class ScrollProperties:
    def __init__(self, configuration_id, scroll_direction, scroll_action_property_id, threshold, mode, config_object=None, actions={}):
        self.configuration_id = configuration_id
        self.scroll_direction = scroll_direction
        self.scroll_action_property_id = scroll_action_property_id
        self.threshold = threshold
        self.mode = mode
        self.actions = actions
        self.config_object = config_object

    def update_threshold(self, new_threshold):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE ScrollActionProperties
                       SET threshold = ?
                       WHERE scroll_action_property_id = ?""", (new_threshold, self.scroll_action_property_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.threshold = new_threshold

    def save_new_mode(self, new_mode):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE ScrollActionProperties
                       SET mode = ? WHERE scroll_action_property_id = ?""", (new_mode, self.scroll_action_property_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.mode = new_mode



class TouchTapProxy():
    def __init__(self, configuration_id, ttp, config_object=None, selected_action_id=None, default=None, nopress=None, togglesmartshift=None, togglehiresscroll=None, keypresses={}, axes={}, changehost={}, cycledpi={}, changedpi={}):
        self.configuration_id = configuration_id
        self.ttp = ttp 
        self.config_object = config_object
        self.selected_action_id = selected_action_id
        self.default =None
        self.nopress = nopress
        self.togglesmartshift = togglesmartshift
        self.togglehiresscroll = togglehiresscroll
        self.keypresses = keypresses
        self.axes = axes
        self.changehost = changehost
        self.cycledpi = cycledpi
        self.changedpi = changedpi
    @classmethod
    def fetch_from_configuration_id(cls, configuration_id, ttp, config_object, cursor=None, conn=None):
        close_db = False
        if cursor is None or conn is None:
            close_db = True
            conn, cursor = execute_db_queries.create_db_connection()

        instance = cls(configuration_id, ttp)
        instance.config_object = config_object
        cursor.execute("""SELECT touch_tap_proxy_id FROM TouchTapProxy WHERE configuration_id = ? AND touch_tap_proxy = ? AND is_selected = 1""", (configuration_id, ttp))
        instance.selected_action_id = cursor.fetchone()[0]
        
        def select_single_actions(action_type):
            cursor.execute("""SELECT touch_tap_proxy_id FROM TouchTapProxy WHERE configuration_id = ? AND touch_tap_proxy = ? AND action_type = ?""",(configuration_id,ttp,action_type))
            return cursor.fetchone()[0]

        instance.nopress = select_single_actions("NoPress")
        instance.togglesmartshift = select_single_actions("ToggleSmartShift")
        instance.togglehiresscroll = select_single_actions("ToggleHiresScroll")

        def get_multiple_values(action_type):
            cursor.execute("""SELECT touch_tap_proxy_id FROM TouchTapProxy WHERE configuration_id = ? AND touch_tap_proxy = ? AND action_type = ?""", (configuration_id,ttp,action_type))
            return cursor.fetchall()

        instance.keypresses = Keypresses1.fetch_all(reference_ids=get_multiple_values("Keypress"), reference_id_type="TouchTapProxy", conn=conn, cursor=cursor)
        instance.cycledpi = CycleDPI1.fetch_all(reference_ids=get_multiple_values("CycleDPI"), reference_id_type="TouchTapProxy", conn=conn, cursor=cursor)
        instance.changehost = ChangeHost1.fetch_all(reference_ids=get_multiple_values("ChangeHost"), reference_id_type="TouchTapProxy", conn=conn, cursor=cursor)
        instance.changedpi = ChangeDPI1.fetch_all(reference_ids=get_multiple_values("ChangeDPI"), reference_id_type="TouchTapProxy", conn=conn, cursor=cursor)
        instance.axes = Axis1.fetch_all(reference_ids=get_multiple_values("Axes"), reference_id_type="TouchTapProxy", conn=conn, cursor=cursor)

        if close_db:
            execute_db_queries.close_without_committing_changes(conn)

        return instance


    def update_selected(self, new_selected_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE TouchTapProxy SET is_selected = 1 WHERE touch_tap_proxy_id = ?""", (new_selected_id,))
        execute_db_queries.commit_changes_and_close(conn)
        self.selected_action_id = new_selected_id


    def add_new_changehost_action(self, host_change):
        new_touch_tap_proxy_id, conn, cursor = self.add_action("ChangeHost")
        cursor.execute("""UPDATE ChangeHost Set host_change = ? WHERE action_id = ? AND source_table = 'TouchTapProxy'""", (host_change, new_touch_tap_proxy_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.changehost[new_touch_tap_proxy_id] = ChangeHost1(host_change=host_change, reference_id=new_touch_tap_proxy_id, reference_id_type="TouchTapProxy")
        return self.changehost[new_touch_tap_proxy_id]



    def add_new_axis_action(self, axis, axis_multiplier):
        new_touch_tap_proxy_id, conn, cursor = self.add_action("Axis")
        cursor.execute("""UPDATE Axes SET axis_button = ?, axis_multiplier = ? WHERE action_id = ? AND source_table = 'TouchTapProxy'""", (axis, axis_multiplier, new_touch_tap_proxy_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.axes[new_touch_tap_proxy_id] = Axis1(axis_button=axis, axis_multiplier=axis_multiplier, reference_id=new_touch_tap_proxy_id, reference_id_type="TouchTapProxy")
        return self.axes[new_touch_tap_proxy_id]

    def add_new_keypress_action(self, keypresses):
        new_touch_tap_proxy_id, conn, cursor = self.add_action("Keypress")
        cursor.execute("""UPDATE Keypresses SET keypresses = ? WHERE action_id = ? AND source_table = 'TouchTapProxy'""", (keypresses, new_touch_tap_proxy_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.keypresses[new_touch_tap_proxy_id] = Keypresses1(keypresses=keypresses, reference_id=new_touch_tap_proxy_id, reference_id_type="TouchTapProxy")
        return self.keypresses[new_touch_tap_proxy_id]

    def add_new_cycledpi_action(self, dpi_array):
        new_touch_tap_proxy_id, conn, cursor = self.add_action("CycleDPI")
        cursor.execute("""UPDATE CycleDPI SET dpi_array = ? WHERE action_id = ? AND source_table = 'TouchTapProxy'""", (dpi_array, new_touch_tap_proxy_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.cycledpi[new_touch_tap_proxy_id] = CycleDPI1(dpi_array=dpi_array, reference_id=new_touch_tap_proxy_id, reference_id_type="ScrollActions")
        return self.cycledpi[new_touch_tap_proxy_id]

    def add_new_changedpi_action(self, new_value):
        new_touch_tap_proxy_id, conn, cursor = self.add_action("ChangeDPI")
        cursor.execute("""UPDATE ChangeDPI Set increment = ? WHERE action_id = ? AND source_table = 'TouchTapProxy'""", (new_value, new_touch_tap_proxy_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.changedpi[new_touch_tap_proxy_id] = ChangeDPI1(increment=new_value, reference_id=new_touch_tap_proxy_id, reference_id_type="ScrollActions")
        return self.changedpi[new_touch_tap_proxy_id]


    def delete_keypress_action(self, action_id):
        self.delete_action(action_id)
        del self.keypresses[action_id]

    def delete_axis_action(self, action_id):
        self.delete_action(action_id)
        del self.axes[action_id]

    def delete_changehost_action(self, action_id):
        self.delete_action(action_id)
        del self.changehost[action_id]

    def delete_cycledpi_action(self, action_id):
        self.delete_action(action_id)
        del self.cycledpi[action_id]

    def delete_changedpi_action(self, action_id):
        self.delete_action(action_id)
        del self.changedpi[action_id]


    def delete_action(self, action_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""DELETE FROM TouchTapProxy WHERE touch_tap_proxy_id = ?""",(action_id,))
        execute_db_queries.commit_changes_and_close(conn)

    def add_action(self, action_type):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type) VALUES (?, ?, ?)""",(self.configuration_id, self.ttp, action_type))

        cursor.execute(
            """
            SELECT last_insert_rowid();
            """
            )
        return cursor.fetchone()[0], conn, cursor



class ScrollDirections(dict):
    def __init__(self, configuration_id):
        self.configuration_id = configuration_id
        self.scroll_directions_dict = {}

    @classmethod
    def fetch_from_configuration_id(cls, configuration_id, config_object=None, cursor=None, conn=None):
        close_db = False
        if cursor is None or conn is None:
            close_db = True
            conn, cursor = execute_db_queries.create_db_connection()

        instance = cls(configuration_id)

        cursor.execute("""
        SELECT scroll_direction, scroll_action_property_id, threshold, mode
        FROM ScrollActionProperties
        WHERE configuration_id = ?;
        """, (configuration_id,))

        scroll_actions = cursor.fetchall()

        for i in scroll_actions:
            instance[i[0]] = ScrollProperties(
                configuration_id=configuration_id,
                config_object=config_object,
                scroll_direction=i[0],
                scroll_action_property_id=i[1],
                threshold=i[2],
                mode=i[3],
                actions=ScrollActions.create_from_scroll_action_property_id(conn=conn, cursor=cursor, config_object=config_object, scroll_action_property_id=i[1])
            )

        if close_db:
            execute_db_queries.close_without_committing_changes(conn)
        
        key_order = ["Up", "Down", "Left", "Right"]
        instance.scroll_directions_dict = {key: instance[key] for key in key_order if key in instance}
        return instance



class ButtonSettings1:
    def __init__(
            self,
            button_id,
            button_cid,
            button_name,
            selected_action_id=None,
            keypresses=None,
            changehost=None,
            cycledpi=None,
            changedpi=None,
            axes=None,
            default=None,
            nopress=None,
            config_object=None,
            togglehiresscroll=None,
            togglesmartshift=None,
            gestures=None,
            # gesture_dict=None,
            gesture_support=None
            
    ):
        
        self.button_id=button_id
        self.button_cid=button_cid
        self.button_name=button_name
        self.config_object = config_object
        self.selected_action_id = selected_action_id
        self.default = default
        self.nopress = nopress
        self.togglesmartshift = togglesmartshift
        self.togglehiresscroll = togglehiresscroll
        self.keypresses = keypresses
        self.axes = axes
        self.changehost = changehost
        self.cycledpi = cycledpi
        self.changedpi = changedpi
        self.gestures=gestures
        # self.gesture_dict = gesture_dict
        self.gesture_support = gesture_support

    @classmethod
    def create_object(cls, config_object, button_id, button_cid, button_name, gesture_support, conn=None, cursor=None):
        configuration_id = config_object.configuration_id
        button = cls(button_id=button_id, button_cid=button_cid, button_name=button_name, gesture_support=gesture_support, config_object=config_object)


        close_db = False
        if conn == None:
            close_db = True
            conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
                        SELECT button_config_id
                        FROM ButtonConfigs
                        WHERE is_selected = 1
                        AND configuration_id = ?
                        AND button_id = ?
                        """, (configuration_id, button_id))

        button.selected_action_id = cursor.fetchone()[0]

        one_config_values = {"Default":None, "Gestures":None, "NoPress":None, "ToggleHiresScroll":None, "ToggleSmartShift":None}
        for key in one_config_values:
            cursor.execute("""
                        SELECT button_config_id
                        FROM ButtonConfigs
                        WHERE button_id = ? AND action_type = ? AND configuration_id = ?
            """, (button_id, key, configuration_id))
            result = cursor.fetchone()

            if result:
                one_config_values[key] = result[0]

        button.default = one_config_values["Default"]
        button.gestures = one_config_values["Gestures"]
        button.nopress = one_config_values["NoPress"]
        button.togglehiresscroll = one_config_values["ToggleHiresScroll"]
        button.togglesmartshift = one_config_values["ToggleSmartShift"]


        def get_multiple_values(action_type):
            cursor.execute("""SELECT button_config_id FROM ButtonConfigs WHERE configuration_id = ? AND button_id = ? AND action_type = ?""", (configuration_id,button_id,action_type))
            return cursor.fetchall()

        button.keypresses = Keypresses1.fetch_all(reference_ids=get_multiple_values("Keypress"), reference_id_type="ButtonConfigs", conn=conn, cursor=cursor)
        button.cycledpi = CycleDPI1.fetch_all(reference_ids=get_multiple_values("CycleDPI"), reference_id_type="ButtonConfigs", conn=conn, cursor=cursor)
        button.changehost = ChangeHost1.fetch_all(reference_ids=get_multiple_values("ChangeHost"), reference_id_type="ButtonConfigs", conn=conn, cursor=cursor)
        button.changedpi = ChangeDPI1.fetch_all(reference_ids=get_multiple_values("ChangeDPI"), reference_id_type="ButtonConfigs", conn=conn, cursor=cursor)
        button.axes = Axis1.fetch_all(reference_ids=get_multiple_values("Axis"), reference_id_type="ButtonConfigs", conn=conn, cursor=cursor)    
        button.gestures = GestureDict.create_object(button=button, configuration=config_object, button_config_id=button.gestures, conn=conn, cursor=cursor)


        if close_db == True:
            execute_db_queries.close_without_committing_changes(conn)
        return button


    def get_added_order(self):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""SELECT button_config_id FROM ButtonConfigs WHERE button_id = ? AND configuration_id = ? AND date_added IS NOT NULL ORDER BY date_added;""",(self.button_id, self.config_object.configuration_id))
        result = cursor.fetchall()
        execute_db_queries.close_without_committing_changes(conn)
        return [i[0] for i in result]


    def update_selected(self, new_selected_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE ButtonConfigs SET is_selected = 1 WHERE button_config_id = ?""", (new_selected_id,))
        execute_db_queries.commit_changes_and_close(conn)
        self.selected_action_id = new_selected_id


    def add_new_axis_action(self, axis, axis_multiplier):
        new_button_config_id, conn, cursor = self.add_action("Axis")
        cursor.execute("""UPDATE Axes SET axis_button = ?, axis_multiplier = ? WHERE action_id = ? AND source_table = 'ButtonConfigs'""", (axis, axis_multiplier, new_button_config_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.axes[new_button_config_id] = Axis1(axis_button=axis, axis_multiplier=axis_multiplier, reference_id=new_button_config_id, reference_id_type="ButtonConfigs")
        return self.axes[new_button_config_id]

    def add_new_changehost_action(self, host_change):
        new_button_config_id, conn, cursor = self.add_action("ChangeHost")
        cursor.execute("""UPDATE ChangeHost Set host_change = ? WHERE action_id = ? AND source_table = 'ButtonConfigs'""", (host_change, new_button_config_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.changehost[new_button_config_id] = ChangeHost1(host_change=host_change, reference_id=new_button_config_id, reference_id_type="ButtonConfigs")
        return self.changehost[new_button_config_id]

    def add_new_changedpi_action(self, new_value):
        new_button_config_id, conn, cursor = self.add_action("ChangeDPI")
        cursor.execute("""UPDATE ChangeDPI Set increment = ? WHERE action_id = ? AND source_table = 'ButtonConfigs'""", (new_value, new_button_config_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.changedpi[new_button_config_id] = ChangeDPI1(increment=new_value, reference_id=new_button_config_id, reference_id_type="ButtonConfigs")
        return self.changedpi[new_button_config_id]

    def add_new_keypress_action(self, keypresses):
        new_button_config_id, conn, cursor = self.add_action("Keypress")
        cursor.execute("""UPDATE Keypresses SET keypresses = ? WHERE action_id = ? AND source_table = 'ButtonConfigs'""", (keypresses, new_button_config_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.keypresses[new_button_config_id] = Keypresses1(keypresses=keypresses, reference_id=new_button_config_id, reference_id_type="ButtonConfigs")
        return self.keypresses[new_button_config_id]

    def add_new_cycledpi_action(self, dpi_array):
        new_button_config_id, conn, cursor = self.add_action("CycleDPI")
        cursor.execute("""UPDATE CycleDPI SET dpi_array = ? WHERE action_id = ? AND source_table = 'ButtonConfigs'""", (dpi_array, new_button_config_id))
        execute_db_queries.commit_changes_and_close(conn)
        self.cycledpi[new_button_config_id] = CycleDPI1(dpi_array=dpi_array, reference_id=new_button_config_id, reference_id_type="ButtonConfigs")
        return self.cycledpi[new_button_config_id]


    def delete_keypress_action(self, action_id):
        self.delete_action(action_id)
        del self.keypresses[action_id]

    def delete_axis_action(self, action_id):
        self.delete_action(action_id)
        del self.axes[action_id]

    def delete_changehost_action(self, action_id):
        self.delete_action(action_id)
        del self.changehost[action_id]

    def delete_cycledpi_action(self, action_id):
        self.delete_action(action_id)
        del self.cycledpi[action_id]

    def delete_changedpi_action(self, action_id):
        self.delete_action(action_id)
        del self.changedpi[action_id]


    def delete_action(self, action_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""DELETE FROM ButtonConfigs WHERE button_config_id = ?""",(action_id,))
        execute_db_queries.commit_changes_and_close(conn)

    def add_action(self, action_type):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""INSERT INTO ButtonConfigs (configuration_id, button_id, action_type) VALUES (?, ?, ?)""",(self.config_object.configuration_id, self.button_id, action_type))

        cursor.execute(
            """
            SELECT last_insert_rowid();
            """
            )
        return cursor.fetchone()[0], conn, cursor

    def request_selected_type(self):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
            SELECT action_type
            FROM ButtonConfigs
            WHERE button_config_id = ?
""", (self.selected_action_id,))
        selected = cursor.fetchone()[0]
        execute_db_queries.close_without_committing_changes(conn)
        return selected


















class ButtonSettings:
    def __init__(
                    self,
                    button_id,
                    button_cid, 
                    button_name,
                    gesture_support,
                    selected_button_config_id,
                    button_keypresses,
                    button_changehost = {},
                    button_cycledpi = {},
                    button_changedpi = {},
                    button_axes = {},
                    device_id = None,
                    configuration_id = None,
                    button_default = None,
                    button_nopress = None,
                    button_togglesmartshift = None,
                    button_togglehiresscroll = None,
                    button_gestures = None,
                    gesture_dict = {},
                    configuration_object = None
    ):

        self.button_id = button_id
        self.button_cid = button_cid
        self.button_name = button_name
        self.configuration_id = configuration_id
        self.device_id = device_id
        self.gesture_support = gesture_support
        self.selected_button_config_id = selected_button_config_id
        self.button_default = button_default
        self.button_nopress = button_nopress
        self.button_togglesmartshift = button_togglesmartshift
        self.button_togglehiresscroll = button_togglehiresscroll
        self.button_gestures = button_gestures
        self.button_keypresses = button_keypresses
        self.button_axes = button_axes
        self.button_changehost = button_changehost
        self.button_cycledpi = button_cycledpi
        self.button_changedpi = button_changedpi
        self.gesture_dict = gesture_dict
        self.configuration_object = configuration_object


    @classmethod
    def create_object(cls, cursor, configuration_id, device_id, button_id, button_name, button_cid, gesture_support, configuration_object):

        button = cls(cursor, configuration_id, button_id, button_name, button_cid, gesture_support)
        button.button_id = button_id
        button.button_name = button_name
        button.button_cid = button_cid
        button.gesture_support = gesture_support
        button.device_id = device_id
        button.configuration_id = configuration_id
        button.configuration_object = configuration_object

        one_config_values = {"Default":None, "Gestures":None, "NoPress":None, "ToggleHiresScroll":None, "ToggleSmartShift":None}
        for key in one_config_values:
            cursor.execute("""
                        SELECT button_config_id
                        FROM ButtonConfigs
                        WHERE button_id = ? AND action_type = ? AND configuration_id = ?
            """, (button_id, key, configuration_id))
            result = cursor.fetchone()

            if result:
                one_config_values[key] = result[0]



        button.button_default = one_config_values["Default"]
        button.button_gestures = one_config_values["Gestures"]
        button.button_nopress = one_config_values["NoPress"]
        button.button_togglehiresscroll = one_config_values["ToggleHiresScroll"]
        button.button_togglesmartshift = one_config_values["ToggleSmartShift"]

        button.button_keypresses = {}
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
                        """, (configuration_id, button_id))

        keypress_list = cursor.fetchall()
        if len(keypress_list) != 0:
            for i in keypress_list:
                button.button_keypresses[i[0]] = ButtonKeypress(button_config_id=i[0], keypress_id=i[1], keypresses=i[2])


        button.button_changehost = {}
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
                            AND ButtonConfigs.action_type = 'ChangeHost'
                            AND ChangeHost.source_table = 'ButtonConfigs';
                        """, (configuration_id, button_id))
        changehost_list = cursor.fetchall()
        if len(changehost_list) != 0:
            for i in changehost_list:
                button.button_changehost[i[0]] = ChangeHost(button_config_id=i[0], host_id=i[1], host_change=i[2])




        button.button_changedpi = {}
        cursor.execute("""
                        SELECT
                            ButtonConfigs.button_config_id,
                            ChangeDPI.change_dpi_id,
                            ChangeDPI.increment
                        FROM
                            ButtonConfigs
                        JOIN
                            ChangeDPI ON ChangeDPI.action_id = ButtonConfigs.button_config_id
                        WHERE
                            ButtonConfigs.configuration_id = ?
                            AND ButtonConfigs.button_id = ?
                            AND ButtonConfigs.action_type = 'ChangeDPI'
                            AND ChangeDPI.source_table = 'ButtonConfigs';
                        """, (configuration_id, button_id))
        changedpi_list = cursor.fetchall()
        if len(changedpi_list) != 0:
            for i in changedpi_list:
                button.button_changedpi[i[0]] = ChangeDPI(button_config_id=i[0], change_dpi_id=i[1], increment=i[2])


        button.button_cycledpi = {}
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
                        """, (configuration_id, button_id))
        cycledpi_list = cursor.fetchall()
        if len(cycledpi_list) != 0:
            for i in cycledpi_list:
                button.button_cycledpi[i[0]] = CycleDPI(button_config_id=i[0], cycle_dpi_id=i[1], dpi_array=i[2])







        button.button_axes = {}

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
                            AND ButtonConfigs.action_type = 'Axis'
                            AND Axes.source_table = 'ButtonConfigs';
                        """, (configuration_id, button_id))
        axes_list = cursor.fetchall()
        if len(axes_list) != 0:
            for i in axes_list:
                button.button_axes[i[0]] = Axis(button_config_id=i[0], axis_id=i[1], axis_button=i[2], axis_multiplier=i[3])



        cursor.execute("""
                        SELECT button_config_id
                        FROM ButtonConfigs
                        WHERE is_selected = 1
                        AND configuration_id = ?
                        AND button_id = ?
                        """, (configuration_id, button_id))

        button.selected_button_config_id = cursor.fetchone()[0]

        button.gesture_dict = {}
        for i in ["Up", "Down", "Left", "Right", "None"]:

            button.gesture_dict[i] = GestureSettings.create_object(cursor=cursor, button_config_id=button.button_gestures, direction=i)
            # button_to_add = ButtonSettings.create_object(cursor=cursor, device_id=config.device_id, configuration_id=configuration_id, button_id=i[0], button_name=i[1], button_cid=i[2], gesture_support=bool(i[3]))


        return button


    def add_action(self, cursor, action_type):
        cursor.execute(
            """
            INSERT INTO ButtonConfigs (device_id, button_id, configuration_id, action_type)
            VALUES (?, ?, ?, ?)
            """, (self.device_id, self.button_id, self.configuration_id, action_type)
        )

        cursor.execute(
            """
            SELECT last_insert_rowid();
            """
            )
        return cursor.fetchone()[0]

    def add_new_cycledpi(self, dpi_array):

        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="CycleDPI")
        cursor.execute(
            """
            UPDATE CycleDPI
            SET dpi_array = ?
            WHERE action_id = ? and source_table = "ButtonConfigs";
            """, (dpi_array, inserted_row_button_config_id)
        )
        cursor.execute("""
                        SELECT cycle_dpi_id
                        FROM CycleDPI
                        WHERE action_id = ? AND source_table = 'ButtonConfigs';
                        """, (inserted_row_button_config_id,))
        new_cycledpi_id = cursor.fetchone()[0]
        self.button_cycledpi[inserted_row_button_config_id] = CycleDPI(button_config_id=inserted_row_button_config_id, cycle_dpi_id=new_cycledpi_id, dpi_array=dpi_array)

        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_button_config_id


    def add_new_axis(self, axis, axis_multiplier):

        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="Axis")

        cursor.execute(
            """
            UPDATE Axes
            SET axis_button = ?, axis_multiplier = ?
            WHERE action_id = ? and source_table = "ButtonConfigs";
            """, (axis, axis_multiplier, inserted_row_button_config_id)
        )
        cursor.execute("""
                        SELECT axis_id
                        FROM Axes
                        WHERE action_id = ? AND source_table = 'ButtonConfigs';
                        """, (inserted_row_button_config_id,))
        new_axis_id = cursor.fetchone()[0]
        self.button_axes[inserted_row_button_config_id] = Axis(button_config_id=inserted_row_button_config_id, axis_id=new_axis_id, axis_button=axis, axis_multiplier=axis_multiplier)
        
        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_button_config_id




    def add_new_changedpi(self, increment):

        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="ChangeDPI")

        cursor.execute(
            """
            UPDATE ChangeDPI
            SET increment = ?
            WHERE action_id = ? and source_table = "ButtonConfigs";
            """, (increment, inserted_row_button_config_id)
        )
        cursor.execute("""
                        SELECT change_dpi_id
                        FROM ChangeDPI
                        WHERE action_id = ? AND source_table = 'ButtonConfigs';
                        """, (inserted_row_button_config_id,))
        new_changedpi_id = cursor.fetchone()[0]
        self.button_changedpi[inserted_row_button_config_id] = ChangeDPI(button_config_id=inserted_row_button_config_id, change_dpi_id=new_changedpi_id, increment=increment)

        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_button_config_id


    def add_new_changehost(self, host):
        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="ChangeHost")
        cursor.execute(
            """
            UPDATE ChangeHost
            SET host_change = ?
            WHERE action_id = ? and source_table = "ButtonConfigs";
            """, ("prev" if host == "Previous" else "next" if host == "Next" else host, inserted_row_button_config_id)
        )

        cursor.execute("""
                        SELECT host_id
                        FROM ChangeHost
                        WHERE action_id = ? AND source_table = 'ButtonConfigs';
                        """, (inserted_row_button_config_id,))
        new_changehost_id = cursor.fetchone()[0]
        self.button_changehost[inserted_row_button_config_id] = ChangeHost(button_config_id=inserted_row_button_config_id, host_id=new_changehost_id, host_change=host)

        execute_db_queries.commit_changes_and_close(conn)
        return inserted_row_button_config_id

    def add_new_keypress_action(self, keypresses):
        conn, cursor = execute_db_queries.create_db_connection()
        inserted_row_button_config_id = self.add_action(cursor=cursor, action_type="Keypress")

        cursor.execute("""
                            UPDATE Keypresses
                            SET keypresses = ?
                            WHERE action_id = ? and source_table = 'ButtonConfigs';
                    """, (keypresses, inserted_row_button_config_id))

        cursor.execute("""
                        SELECT keypress_id
                        FROM Keypresses
                        WHERE action_id = ? AND source_table = 'ButtonConfigs';
                        """, (inserted_row_button_config_id,))
        new_keypress_id = cursor.fetchone()[0]
        self.button_keypresses[inserted_row_button_config_id] = ButtonKeypress(button_config_id=inserted_row_button_config_id, keypress_id=new_keypress_id, keypresses=keypresses)

        execute_db_queries.commit_changes_and_close(conn)

        return inserted_row_button_config_id


    def delete_axis(self, button_config_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                        DELETE FROM ButtonConfigs
                        WHERE button_config_id = ?;
                        """, (button_config_id,))
        execute_db_queries.commit_changes_and_close(conn)
        del self.button_axes[button_config_id]


    def delete_cycledpi(self, button_config_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                        DELETE FROM ButtonConfigs
                        WHERE button_config_id = ?;
                        """, (button_config_id,))
        execute_db_queries.commit_changes_and_close(conn)
        del self.button_cycledpi[button_config_id]


    def delete_changedpi(self, button_config_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                        DELETE FROM ButtonConfigs
                        WHERE button_config_id = ?;
                        """, (button_config_id,))
        execute_db_queries.commit_changes_and_close(conn)
        del self.button_changedpi[button_config_id]


    def delete_changehost(self, button_config_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                        DELETE FROM ButtonConfigs
                        WHERE button_config_id = ?;
                        """, (button_config_id,))
        execute_db_queries.commit_changes_and_close(conn)
        del self.button_changehost[button_config_id]


    def delete_keypresses(self, button_config_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
                    DELETE FROM ButtonConfigs
                    WHERE button_config_id = ?;
                        """, (button_config_id,))

        execute_db_queries.commit_changes_and_close(conn)
        del self.button_keypresses[button_config_id]

    def request_selected_type(self):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
            SELECT action_type
            FROM ButtonConfigs
            WHERE button_config_id = ?
""", (self.selected_button_config_id,))
        selected = cursor.fetchone()[0]
        execute_db_queries.close_without_committing_changes(conn)
        return selected




class Configuration:
    def __init__(
        self,
        device_id=None,
        user_device_object=None,
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
        scroll_directions=None,
        date_device_added=None,
        date_device_last_edited=None,
        touch=None,
        tap=None,
        proxy=None
    ):
        self.device_id=device_id
        self.device_name=device_name
        self.user_device_object = user_device_object
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
        self.scroll_directions=scroll_directions
        self.touch = touch
        self.tap = tap
        self.proxy = proxy

    @classmethod
    def create_from_configuration_id(cls, configuration_id, user_device_object = None, cursor=None, conn=None):

        close_db = False
        
        if cursor == None:
            close_db = True
            conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
        SELECT *
        FROM Configurations AS C
        JOIN Devices AS D ON C.device_id = D.device_id
        WHERE C.configuration_id = ?;
        """, (configuration_id,))

        configuration_query_result = cursor.fetchone()


        config = cls()
        config.user_device_object = user_device_object
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
            SELECT button_id, button_name, button_cid, gesture_support
            FROM Buttons
            WHERE device_id = ? AND reprog = 1 AND accessible = 1
        """, (config.device_id,))
        button_id_list = cursor.fetchall()

        config.buttons = {}

        for i in button_id_list:
            button_to_add = ButtonSettings1.create_object(cursor=cursor, button_id=i[0], button_name=i[1], button_cid=i[2], gesture_support=bool(i[3]), config_object=config)
            config.buttons[i[0]]=button_to_add

        if config.has_scrollwheel == True or config.has_thumbwheel == True:
            config.scroll_directions = ScrollDirections.fetch_from_configuration_id(configuration_id, config_object=config, conn=conn, cursor=cursor)

        if config.thumbwheel_touch_support:
            config.touch = TouchTapProxy.fetch_from_configuration_id(configuration_id=configuration_id, config_object=config, ttp="Touch")
        if config.thumbwheel_tap_support:
            config.tap = TouchTapProxy.fetch_from_configuration_id(configuration_id=configuration_id, config_object=config, ttp="Tap")

        if config.thumbwheel_proxy_support:
            config.proxy = TouchTapProxy.fetch_from_configuration_id(configuration_id=configuration_id, config_object=config, ttp="Proxy")

        if close_db == True:
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

        execute_db_queries.commit_changes_and_close(conn)


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


    def update_dpi(self, new_value):
        self.dpi = new_value

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

    def update_smartshift_threshold(self, new_value):
        self.smartshift_threshold = new_value

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

    def update_smartshift_torque(self, new_value):
        self.smartshift_torque = new_value

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

class Device:
    def __init__(self, device_name, device_id, is_activated):
        self.device_name = device_name
        self.device_id = device_id
        self.is_activated = is_activated

class NonUserDevice(Device):
    def __init__(self, device_id, device_name, is_activated):
        super().__init__(device_id, device_name, is_activated)

        self.device_id = device_id
        self.device_name = device_name
        self.is_activated = is_activated

    @classmethod
    def delete_user_device(cls, user_device):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE Devices SET is_user_device = 0 WHERE device_id=?""", (user_device.device_id,))
        execute_db_queries.commit_changes_and_close(conn)
        return cls(
        device_id=user_device.device_id,
        device_name=user_device.device_name,
        is_activated=user_device.is_activated
    )

class UserDevice(Device):

    def __init__(
      self,
      device_id,
      device_name,
      is_activated,
      configurations={},
      selected_config = None,
    ):
        self.device_id = device_id
        self.device_name = device_name
        self.is_activated = is_activated
        self.configurations = configurations
        self._selected_config = selected_config

#     @classmethod
#     def create_from_device_id(cls, device_id, conn=None, cursor=None):
#         close_db = True if conn == None else False

#         if not conn:
#             conn, cursor = execute_db_queries.create_db_connection()
#         cursor.execute("""SELECT device_name, is_activated FROM Devices WHERE device_id = ?""",(device_id,))
#         device_result=cursor.fetchone()
#         device_name=device_result[0]
#         is_activated=device_result[1]

#         cursor.execute("""SELECT configuration_id FROM Configurations WHERE is_selected = 1 AND device_id = ?""", (device_id,))
#         selected_config = cursor.fetchone()[0]
        
#         cursor.execute("""SELECT configuration_id FROM Configurations WHERE device_id = ?""", (device_id,))
#         configurations = {}
#         for i in cursor.fetchall():
#             configurations[i[0]] = Configuration.create_from_configuration_id(i[0], user_device_object=cls)
#         if close_db == True:
#             execute_db_queries.close_without_committing_changes(conn)
        
#         return cls(
#             device_id=device_id,
#             device_name=device_name,
#             is_activated=is_activated,
#             selected_config = selected_config,
#             configurations = configurations
#         )


    @classmethod
    def create_from_device_id(cls, device_id, conn=None, cursor=None):
        close_db = True if conn is None else False

        if not conn:
            conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""SELECT device_name, is_activated FROM Devices WHERE device_id = ?""", (device_id,))
        device_result = cursor.fetchone()
        device_name = device_result[0]
        is_activated = device_result[1]

        cursor.execute("""SELECT configuration_id FROM Configurations WHERE is_selected = 1 AND device_id = ?""", (device_id,))
        selected_config = cursor.fetchone()[0]
        
        configurations = {}
        device_instance = cls(  # Instantiate the UserDevice object
            device_id=device_id,
            device_name=device_name,
            is_activated=is_activated,
            selected_config=selected_config
        )

        cursor.execute("""SELECT configuration_id FROM Configurations WHERE device_id = ?""", (device_id,))
        for i in cursor.fetchall():
            configurations[i[0]] = Configuration.create_from_configuration_id(i[0], user_device_object=device_instance)  # Pass the instance

        device_instance.configurations = configurations  # Set the configurations attribute
        if close_db:
            execute_db_queries.close_without_committing_changes(conn)
        
        return device_instance


    def delete_configuration(self, configuration_id):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""DELETE FROM Configurations WHERE configuration_id = ?""", (configuration_id,))
        execute_db_queries.commit_changes_and_close(conn)
        if configuration_id == self.selected_config:
            conn, cursor = execute_db_queries.create_db_connection()
            cursor.execute("""SELECT configuration_id FROM Configurations WHERE device_id = ? AND is_selected = 1""", (self.device_id,))
            self.selected_config = cursor.fetchone()[0]
            execute_db_queries.close_without_committing_changes(conn)
        del self.configurations[configuration_id]

    def add_new_configuration(self):
        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""
                    SELECT configuration_name
                    FROM Configurations
                    WHERE device_id = ? AND configuration_name LIKE ? || '%'
    """, (self.device_id, self.device_name))
        
        similar_names = cursor.fetchall()
        
        similar_names_as_strings = [str(row[0]) for row in similar_names]

        next_config_name = self.get_next_sequential_name(self.device_name, similar_names_as_strings)

        cursor.execute("""
                    SELECT smartshift_support, hires_scroll_support, has_thumbwheel
                    FROM Devices
                    WHERE device_id = ?
    """, (self.device_id,))

        smartshift_support, hires_scroll_support, has_thumbwheel = cursor.fetchone()

        if bool(smartshift_support) == True:
            smartshift_on = 1
            smartshift_threshold = smartshift_torque = 10
        else:
            smartshift_on = smartshift_threshold = smartshift_torque = None


        if bool(hires_scroll_support) == True:
            hiresscroll_hires = hiresscroll_invert = hiresscroll_target = True

        else:
            hiresscroll_hires = hiresscroll_invert = hiresscroll_target = None

        if bool(has_thumbwheel) == True:
            thumbwheel_divert = thumbwheel_invert = True

        else:
            thumbwheel_divert = thumbwheel_invert = None

        cursor.execute("""
        INSERT INTO Configurations (
            device_id,
            configuration_name,
            last_modified,
            is_selected,
            smartshift_on,
            smartshift_threshold,
            smartshift_torque,
            hiresscroll_hires,
            hiresscroll_invert,
            hiresscroll_target,
            thumbwheel_divert,
            thumbwheel_invert
        ) VALUES (?, ?, NULL, 0, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (self.device_id, next_config_name, smartshift_on, smartshift_threshold, smartshift_torque, hiresscroll_hires, hiresscroll_invert, hiresscroll_target, thumbwheel_divert, thumbwheel_invert)) 

        newest_configuration_id = cursor.lastrowid

        # cursor.execute("""UPDATE Configurations SET is_selected = 1 WHERE configuration_id = ?""", (newest_configuration_id,))

        execute_db_queries.commit_changes_and_close(conn)
        
        self.configurations[newest_configuration_id] = Configuration.create_from_configuration_id(newest_configuration_id, user_device_object=self)
        # self.selected_config = newest_configuration_id

        return newest_configuration_id


    @staticmethod
    def get_next_sequential_name(name_to_match, similar_names):
        if len(similar_names) == 0 or name_to_match not in similar_names:
            return name_to_match

        else:
            pattern = rf'{re.escape(name_to_match)}(?: \((\d+)\))?'
            numbers = []

            for similar_name in similar_names:
                match = re.match(pattern, similar_name)
                if match:
                    number_str = match.group(1)
                    if number_str:
                        number = int(number_str)
                        if number >= 2:
                            numbers.append(number)

            if len(numbers) == 0:
                return f"{name_to_match} (2)"

            numbers.sort()

            for i in range(1):
                if numbers[0] < 2:
                    del numbers[0]
                    if len(numbers) == 0:
                        return f"{name_to_match} (2)"

            new_highest_number = 2
                
            for i in numbers:
                if i == new_highest_number:
                    new_highest_number += 1
                    continue
                else:
                    break

            return f"{name_to_match} ({new_highest_number})"

































        
        # TODO

    @property
    def selected_config(self):
        return self._selected_config

    @selected_config.setter
    def selected_config(self, value):
        self._selected_config = value

        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""
        UPDATE Configurations
        SET is_selected = 1
        WHERE configuration_id = ?
        """, (value,))

        conn.commit()
        conn.close()


class Devices():
    def __init__(self):
        self.user_devices = {}
        self.ignored_devices = {}
        self.non_user_devices = {}

    @classmethod
    def get_all_devices(cls):
        instance = cls()
        instance.non_user_devices, ignored_non_user_devices = cls.get_all_non_user_devices()
        instance.user_devices = cls.get_all_user_devices()
        # TODO FINISH

        return instance

    @classmethod
    def get_all_user_devices(cls):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""SELECT device_id FROM Devices WHERE is_user_device = 1 AND is_activated = 1 ORDER BY date_added DESC""")
        devices = {}
        for i in cursor.fetchall():
            devices[i[0]] = UserDevice.create_from_device_id(i[0], conn=conn, cursor=cursor)
        execute_db_queries.close_without_committing_changes(conn)
        return devices


    @classmethod
    def get_all_non_user_devices(cls):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""SELECT device_id, device_name, is_activated FROM Devices WHERE is_user_device = 0 ORDER BY device_id DESC""")
        non_user_devices ={}
        ignored_non_user_devices = {}
        for i in cursor.fetchall():
            device = NonUserDevice(device_id=i[0], device_name=i[1], is_activated=bool(i[2]))
            non_user_devices[device.device_id] = device
            if device.is_activated == False:
                ignored_non_user_devices[device.device_id] = device
        execute_db_queries.close_without_committing_changes(conn)
        return non_user_devices, ignored_non_user_devices

    def remove_ignored_device(self, device):
        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE Devices SET is_activated = 1 WHERE device_id = ?""",(device.device_id,))
        execute_db_queries.commit_changes_and_close(conn)
        if isinstance(device, "UserDevice"):
            device.is_activated = True
            self.user_devices[device.device_id] = device
        del self.ignored_devices[device.device_id]

    def add_new_user_device_given_name(self, new_device_name):

        conn, cursor = execute_db_queries.create_db_connection()
        cursor.execute("""UPDATE Devices SET is_user_device = 1, is_activated = 1 WHERE device_name = ?""", (new_device_name,))
        cursor.execute("""SELECT device_id FROM Devices WHERE device_name = ?""", (new_device_name,))
        new_device_id = cursor.fetchone()[0]

        execute_db_queries.commit_changes_and_close(conn)
        new_device = UserDevice.create_from_device_id(new_device_id)

        del self.non_user_devices[new_device.device_id]
        self.user_devices[new_device.device_id] = new_device

        return new_device


    def delete_user_device(self, device):
        self.non_user_devices[device.device_id] = NonUserDevice.delete_user_device(device)
        self.non_user_devices = {k: self.non_user_devices[k] for k in sorted(self.non_user_devices, reverse=True)}
        del self.user_devices[device.device_id]


    def add_ignored_device(self, device):
        # TODO 
        pass


def main():
    devices = Devices.get_all_devices()
    print(devices)
    print(devices.non_user_devices)


if __name__=="__main__":
    main()