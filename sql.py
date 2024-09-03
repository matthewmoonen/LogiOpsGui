import execute_db_queries

def update(cursor):
    cursor.execute("""
                
                
                
                
    UPDATE UserSettings SET value = 'False' WHERE key = 'overwrite'
                
                
                
                
                
                
                
                
    """)




def select1(cursor):
    cursor.execute("""
                
                
                
                
    
                
                
                
                
                
                
                
                
    """)
    print(cursor.fetchone()[0])




def main():
    conn, cursor = execute_db_queries.create_db_connection()

    update(cursor)
    # select1(cursor)


    execute_db_queries.commit_changes_and_close(conn)



if __name__=="__main__":
    main()