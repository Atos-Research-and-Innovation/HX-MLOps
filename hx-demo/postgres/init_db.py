import psycopg2


def create_table(connection, table_name):
    """
    Create a new table in the database.
    
    Args:
        connection (psycopg2.Connection): The connection to the database.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    connection INTEGER
                )
            """)
        # Commit the transaction
        connection.commit()
        print("Table created successfully.")
    except psycopg2.Error as e:
        # Rollback the transaction in case of error
        connection.rollback()
        print("Error creating table:", e)



if __name__ == "__main__":

    # Connect to the database
    connection = psycopg2.connect(
        dbname="ile",
        user="admin",
        password="admin",
        host="localhost",
        port="30098"
    )


    table_name="service_check"
    print(f"Creating table {table_name} if it does not exist...")
    create_table(connection, table_name)