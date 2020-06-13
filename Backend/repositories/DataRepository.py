from .Database import Database
from datetime import datetime


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_Actuator_by_id(id):
        sql = "SELECT ActuatorWaarde FROM Project.historiek WHERE Actuatorid = %s order by Datum desc limit 1;"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_status_Sensor_by_id(id):
        sql = "SELECT SensorWaarde FROM Project.Historiek WHERE Sensorid = %s"
        params = [id]
        return Database.get_one_row(sql, params)
   
    @staticmethod
    def insert_status_Sensor_by_id( sensorid, SensorWaarde):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO historiek (datum, sensorid, actuatorid, SensorWaarde, ActuatorWaarde) VALUES (%s,%s,%s,%s,%s);"
        params = [formatted_date, sensorid, 0, SensorWaarde, 0]
        return Database.execute_sql(sql, params)

    @staticmethod
    def insert_status_Actuator_by_id(actuatorid, ActuatorWaarde):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO historiek (datum, sensorid, actuatorid, SensorWaarde, ActuatorWaarde) VALUES (%s,%s,%s,%s,%s);"
        params = [formatted_date, 0, actuatorid, 0, ActuatorWaarde]
        return Database.execute_sql(sql, params)

    @staticmethod
    def Get_historiek_temperatuur():
        sql = "SELECT Datum, SensorWaarde FROM Project.historiek where Sensorid=1 order by Datum desc limit 8;"
        return Database.get_rows(sql)

    @staticmethod
    def Get_historiek_Vochtigheid():
        sql = "SELECT Datum, SensorWaarde FROM Project.historiek where Sensorid=2 order by Datum desc limit 8;"
        return Database.get_rows(sql)
    
    @staticmethod
    def Get_historiek_CO():
        sql = "SELECT Datum, SensorWaarde FROM Project.historiek where Sensorid=3 order by Datum desc limit 8;"
        return Database.get_rows(sql)

    @staticmethod
    def Get_historiek_Watertank():
        sql = "SELECT Datum, SensorWaarde FROM Project.historiek where Sensorid=4 order by Datum desc limit 8;"
        return Database.get_rows(sql)
  
