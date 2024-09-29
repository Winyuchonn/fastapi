from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

app = FastAPI()


class TemperatureData(BaseModel):
    sensor1: float
    sensor2: float
    sensor3: float
    sensor4: float


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="34.143.223.232",        
            user="admin",            
            password=":pnolvhX+pQ{DkDC",
            database="iot_test",     
        )
    except Error as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    return connection


def insert_temperature(sensor_id: int, temperature: float, table_name: str):
    connection = create_connection()
    cursor = connection.cursor()
    
    try:
        
        if temperature == -127.00:
            temperature = 0.0

        query = f"""
            INSERT INTO `{table_name}` (`sensor_id`, `temperature`) 
            VALUES (%s, %s)
        """
        cursor.execute(query, (sensor_id, temperature))
        connection.commit()
    except Error as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        cursor.close()
        connection.close()


def insert_mean_temperature(mean_temperature: float, table_name: str, column_name: str):
    connection = create_connection()
    cursor = connection.cursor()
    
    try:
        query = f"""
            INSERT INTO `{table_name}` (`{column_name}`) 
            VALUES (%s)
        """
        cursor.execute(query, (mean_temperature,))
        connection.commit()
    except Error as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        cursor.close()
        connection.close()


@app.post("/temperature")
async def receive_temperature(data: TemperatureData):
   
    insert_temperature(1, data.sensor1, 'temperature_outside')
    insert_temperature(2, data.sensor2, 'temperature_outside')
    insert_temperature(3, data.sensor3, 'temperature_outside')
    insert_temperature(4, data.sensor4, 'temperature_outside')
    
    
    temperatures = [data.sensor1, data.sensor2, data.sensor3, data.sensor4]
    valid_temperatures = [temp if temp != -127.00 else 0.0 for temp in temperatures]  
    mean_temperature = sum(valid_temperatures) / len(valid_temperatures)
    
   
    insert_mean_temperature(mean_temperature, 'mean_outside', 'mean_out')
    
    return {"message": "รับข้อมูลอุณหภูมิเรียบร้อยแล้ว คำนวณค่าเฉลี่ยและบันทึกสำเร็จ"}


@app.post("/temperature2")
async def receive_temperature_inside(data: TemperatureData):
    
    insert_temperature(1, data.sensor1, 'temperature_inside')
    insert_temperature(2, data.sensor2, 'temperature_inside')
    insert_temperature(3, data.sensor3, 'temperature_inside')
    insert_temperature(4, data.sensor4, 'temperature_inside')
    
    
    temperatures = [data.sensor1, data.sensor2, data.sensor3, data.sensor4]
    valid_temperatures = [temp if temp != -127.00 else 0.0 for temp in temperatures]  
    mean_temperature = sum(valid_temperatures) / len(valid_temperatures)
    
    
    insert_mean_temperature(mean_temperature, 'mean_inside', 'mean_in')
    
    return {"message": "รับข้อมูลอุณหภูมิภายในเรียบร้อยแล้ว คำนวณค่าเฉลี่ยและบันทึกสำเร็จ"}
