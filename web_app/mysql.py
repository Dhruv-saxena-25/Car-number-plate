import mysql.connector

# MySQL Connection

mydb= mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= 'root@123',
    database= 'car_yolov8'
)

my_cursor=mydb.cursor()
print("Connection Establish")

# text = "Lc64 EMF"
# if text == my_cursor.execute(f"select Name from car_num where Num_plate={text}"):
#                 my_cursor.execute("select Name from car_num")
#                 result= my_cursor.fetchone()
#                 print(f"Vechile Owner: {result}")
# else:
#     print(f'Vechile Ownwer : {"Unknown..."}')




try:
    query1 = 'SELECT Num_plate FROM car_num WHERE Num_plate = %s'
    my_cursor.execute(query1, (text,))
    result = my_cursor.fetchone()

    if result is not None:
        if text == str(result[0]):
            query = "SELECT Name FROM car_num WHERE Num_plate = %s"
            my_cursor.execute(query, (text,))
            result = my_cursor.fetchone()

            if result is not None:
                print(result[0])
            else:
                print("No matching name found")
        else:
            print("Text does not match Num_plate")
    else:
        print("No matching Num_plate found")

except mysql.connector.Error as err:
    print(f"Error executing query: {err}")
    
