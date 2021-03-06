
from dbquery import Dbquery
import csv
import sqlite3

class Init:

    @classmethod
    def inittables(cls, db, mycursor):


        query = "CREATE TABLE IF NOT EXISTS Country (CountryKey Varchar(3),CountryName VARCHAR(255) NOT NULL," \
                "GDPpercapita INT NOT NULL,TourismExpend Float NOT NULL,GDPIndustrailRatio float NOT NULL,population " \
                "Int not null,PRIMARY KEY(CountryKey)); "
        mycursor.execute(query)
        with open('countryData.csv') as csv_file:
            csv_file = csv.reader(csv_file, delimiter=',')
            all_value = []
            for row in csv_file:
                value = (row[0], row[1], row[2], row[3], row[4], row[5])
                all_value.append(value)
        query = "insert ignore into country(countrykey,countryname,gdppercapita,tourismexpend,gdpindustrailratio," \
                "population) values (%s,%s,%s,%s,%s,%s) "
        mycursor.executemany(query, all_value)
        db.commit()
        query = "CREATE TABLE IF NOT EXISTS Airport(AirportCode CHAR(4), AirportName VARCHAR(64),CountryID CHAR(2), " \
                "NSCoordinates float,EWCoordinates float, NearbyPopulation INT, MaximumRunWayLength INT,PRIMARY KEY (" \
                "AirportCode),FOREIGN KEY (CountryID) REFERENCES Country(CountryKey), CONSTRAINT CHKCoordinates CHECK " \
                "(NSCoordinates <= 180.0 AND NSCoordinates >=-180.0 AND EWCoordinates <= 180.0 AND EWCoordinates >= " \
                "-180.0)); "
        mycursor.execute(query)
        with open('airportdata.csv', encoding="utf8") as csv_file:
            csv_file = csv.reader(csv_file, delimiter=',')
            all_value = []
            for row in csv_file:
                value = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                all_value.append(value)
        query = "insert ignore into Airport(AirportCode,AirportName,CountryID,NSCoordinates,EWCoordinates," \
                "NearbyPopulation,MaximumRunWayLength) values (%s,%s,%s,%s,%s,%s,%s) "
        mycursor.executemany(query, all_value)
        db.commit()
        query = "CREATE TABLE IF NOT EXISTS Airplane(ModelName0 VARCHAR(63), Standard1 VARCHAR(20), PaxCap2 VARCHAR(" \
                "64),Pilots3 INT, Crew4 INT,Turnaround5 INT, Speed6 INT, PlaneRange7 VARCHAR(16),Fuel8 VARCHAR(16), " \
                "Available9 VARCHAR(16), Delivery10 VARCHAR(16), Runway11 INT, SizeClass12 VARCHAR(16), Conversion13 " \
                "VARCHAR(16), NoiseRating14 int, PRIMARY KEY (ModelName0)); "
        mycursor.execute(query)
        with open('Airplanes.csv') as csv_file:
            csv_file = csv.reader(csv_file, delimiter=',')
            all_value = []
            for row in csv_file:
                value = (
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                    row[12], row[13], row[14])
                all_value.append(value)
        query = "insert ignore into Airplane(ModelName0, Standard1, PaxCap2,Pilots3,Crew4,Turnaround5,Speed6," \
                "PlaneRange7,Fuel8,Available9,Delivery10,Runway11,SizeClass12,Conversion13, noiseRating14) values (" \
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        mycursor.executemany(query, all_value)
        db.commit()
        query = Dbquery.deleteTestAirportsTable()
        mycursor.execute(query)
        query = Dbquery.createTestAirportsTable()
        mycursor.execute(query)
        query = Dbquery.updateTestAirports()
        mycursor.execute(query)

        print("reached here")
        query = "CREATE TABLE IF NOT EXISTS Routes(CodeDeparture char(4),CodeArrival char(4),TouristDemand INTEGER," \
                "BuisnessDemand INTEGER,CargoDemand INTEGER,PRIMARY KEY (CodeDeparture, CodeArrival),FOREIGN KEY (" \
                "CodeDeparture) REFERENCES airport(AirportCode),FOREIGN KEY (CodeArrival) REFERENCES airport(" \
                "AirportCode)); "
        mycursor.execute(query)
        query = Dbquery.populateRoutesInnitial()
        mycursor.execute(query)
        db.commit()
        query = "CREATE TABLE IF NOT EXISTS Airline(AirlineName VARCHAR(64),CostStructure CHAR(64),Reputation INT, callsign char(2), PRIMARY KEY (AirlineName));"
        mycursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS Flight (FlightNumber VARCHAR(7) NOT NULL,DepartureTime INTEGER NOT NULL," \
                "Price INTEGER NOT NULL,ArrivalTime INTEGER NOT NULL,LoadFactor INTEGER NOT NULL,AirlineName VARCHAR(" \
                "100),FOREIGN KEY (AirlineName) REFERENCES Airline(AirlineName),AirplaneModelType VARCHAR(100) NOT " \
                "NULL,FOREIGN KEY (AirplaneModelType) REFERENCES Airplane(ModelName0),CodeDeparture CHAR(4)," \
                "CodeArrival CHAR(4),FOREIGN KEY (CodeDeparture) REFERENCES Routes(CodeDeparture),FOREIGN KEY (" \
                "CodeArrival) REFERENCES Routes(CodeArrival),PRIMARY KEY (FlightNumber, DepartureTime),CONSTRAINT " \
                "CHKTime CHECK (ArrivalTime > DepartureTime)); "
        mycursor.execute(query)
        query = "INSERT ignore INTO Airline (AirlineName, CostStructure, Reputation) VALUES ('Air Wayne', 'Flag', " \
                "100)"
        mycursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS BasesOps(AirlineName VARCHAR(64),BaseOfOperation VARCHAR(255), FOREIGN KEY (AirlineName) REFERENCES Airline(AirlineName),FOREIGN KEY (BaseOfOperation) REFERENCES Airport(AirportCode),PRIMARY KEY (AirlineName,BaseOfOperation));"
        mycursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS AirplaneModels(AirlineName VARCHAR(64),AirplaneOperated VARCHAR(255),PRIMARY KEY (AirlineName,AirplaneOperated),FOREIGN KEY (AirlineName) REFERENCES Airline(AirlineName),FOREIGN KEY (AirplaneOperated) REFERENCES Airplane(ModelName0));"
        mycursor.execute(query)

        query = "INSERT INTO Flight (FlightNumber, DepartureTime, Price , ArrivalTime, LoadFactor, AirlineName, " \
                "AirplaneModelType, CodeDeparture,CodeArrival)VALUES (1,1,90,2,70,'Air Wayne', 'BOEING 737-800', " \
                "'KALT', 'KLAX');INSERT INTO Flight (FlightNumber, DepartureTime, Price , ArrivalTime, LoadFactor, " \
                "AirlineName, AirplaneModelType, CodeDeparture,CodeArrival)VALUES (2,1,120,2,75,'Air Wayne', " \
                "'BOEING 737-800','KALT', 'KJFK');INSERT INTO Flight (FlightNumber, DepartureTime, Price , " \
                "ArrivalTime, LoadFactor, AirlineName, AirplaneModelType, CodeDeparture,CodeArrival)VALUES (3,1,140," \
                "2,60,'Air Wayne', 'BOEING 737-800', 'KALT', 'KMIA');INSERT INTO Flight (FlightNumber, DepartureTime, " \
                "Price , ArrivalTime, LoadFactor, AirlineName, AirplaneModelType, CodeDeparture,CodeArrival)VALUES (" \
                "4,1,165,2,90,'Air Wayne', 'BOEING 737-800', 'KALT', 'KORD');INSERT INTO Flight (FlightNumber, " \
                "DepartureTime, Price , ArrivalTime, LoadFactor, AirlineName, AirplaneModelType, CodeDeparture," \
                "CodeArrival)VALUES (5,1,170,2,100,'Air Wayne', 'BOEING 737-800','KORD', 'KJFK'); "
        mycursor.execute(query,multi=True)
        # Airlines start here
        query = "CREATE TABLE IF NOT EXISTS Airline(AirlineName VARCHAR(64), CostStructure CHAR(64), Reputation INT, PRIMARY KEY (AirlineName));"
        mycursor.execute(query)
        query = "INSERT ignore INTO Airline (AirlineName, CostStructure, Reputation, callsign) VALUES ('Air Wayne', 'HIGH', 100, 'AW');"
        mycursor.execute(query)
        query = "INSERT ignore INTO Airline (AirlineName, CostStructure, Reputation, callsign) VALUES ('Air Tim', 'HIGH', 100, 'AT');"
        mycursor.execute(query)
        query = "INSERT ignore INTO Airline (AirlineName, CostStructure, Reputation, callsign) VALUES ('Air Justin', 'MED', 80, 'AJ');"
        mycursor.execute(query)
        query = "INSERT ignore INTO Airline (AirlineName, CostStructure, Reputation, callsign) VALUES ('Air William', 'LOW', 80, 'WA');"
        mycursor.execute(query)
        db.commit()
        # BaseOPs start here (Give each airline 100 airports)
        query = "CREATE TABLE IF NOT EXISTS BasesOps(AirlineName VARCHAR(64), BaseOfOperation VARCHAR(255)" \
                ",FOREIGN KEY (AirlineName) REFERENCES Airline(AirlineName), FOREIGN KEY (BaseOfOperation) " \
                "REFERENCES Airport(AirportCode), PRIMARY KEY (AirlineName,BaseOfOperation));"
        mycursor.execute(query)
        for i in range(2, 343, 2):
            sql = "SELECT AirportCode From testAirports"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            codeValue = code[i]
            query = "INSERT ignore INTO BasesOps (AirlineName, BaseOfOperation) VALUES ('Air Wayne', %s);"
            mycursor.execute(query, codeValue)
        for i in range(5, 343, 5):
            sql = "SELECT AirportCode From testAirports"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            codeValue = code[i]
            query = "INSERT ignore INTO BasesOps (AirlineName, BaseOfOperation) VALUES ('Air Tim', %s);"
            mycursor.execute(query, codeValue)
        for i in range(9, 343, 9):
            sql = "SELECT AirportCode From testAirports"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            codeValue = code[i]
            query = "INSERT ignore INTO BasesOps (AirlineName, BaseOfOperation) VALUES ('Air Justin', %s);"
            mycursor.execute(query, codeValue)
        for i in range(13, 343, 13):
            sql = "SELECT AirportCode From testAirports"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            codeValue = code[i]
            query = "INSERT ignore INTO BasesOps (AirlineName, BaseOfOperation) VALUES ('Air William', %s);"
            mycursor.execute(query, codeValue)
        db.commit()
        # Airplane Models start here (Give each airline Different amounts)
        query = "CREATE TABLE IF NOT EXISTS AirplaneModels(AirlineName VARCHAR(64),AirplaneOperated VARCHAR(255)" \
                ",PRIMARY KEY (AirlineName,AirplaneOperated), FOREIGN KEY (AirlineName) " \
                "REFERENCES Airline(AirlineName), FOREIGN KEY (AirplaneOperated) REFERENCES tempAirplane(ModelName0));"
        mycursor.execute(query)
        for i in range(4, 600, 4):
            sql = "SELECT ModelName0 FROM Airplane"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            codeValue = code[i]
            query = "INSERT ignore INTO AirplaneModels(AirlineName, AirplaneOperated) VALUES ('Air Wayne', %s);"
            mycursor.execute(query, codeValue)
        for i in range(5, 600, 5):
            sql = "SELECT ModelName0 FROM Airplane"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            codeValue = code[i]
            query = "INSERT ignore INTO AirplaneModels(AirlineName, AirplaneOperated) VALUES ('Air Tim', %s);"
            mycursor.execute(query, codeValue)
        for i in range(7, 600, 7):
            sql = "SELECT ModelName0 FROM Airplane"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            codeValue = code[i]
            query = "INSERT ignore INTO AirplaneModels(AirlineName, AirplaneOperated) VALUES ('Air Justin', %s);"
            mycursor.execute(query, codeValue)
        for i in range(10, 600, 10):
            sql = "SELECT ModelName0 FROM Airplane"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            codeValue = code[i]
            query = "INSERT ignore INTO AirplaneModels(AirlineName, AirplaneOperated) VALUES ('Air William', %s);"
            mycursor.execute(query, codeValue)
        db.commit()






    @classmethod
    def fixairplanes(cls, db, mycursor):
        with open('Airplanes.csv', 'w', newline='\n') as f:
            writer = csv.writer(f)

            query = "CREATE TABLE IF NOT EXISTS Airplane(ModelName0 VARCHAR(63), Standard1 VARCHAR(20), PaxCap2 VARCHAR(" \
                    "64),Pilots3 INT, Crew4 INT,Turnaround5 INT, Speed6 INT, PlaneRange7 VARCHAR(16),Fuel8 VARCHAR(16), " \
                    "Available9 VARCHAR(16), Delivery10 VARCHAR(16), Runway11 INT, SizeClass12 VARCHAR(16), Conversion13 " \
                    "VARCHAR(16), NoiseRating14 int, PRIMARY KEY (ModelName0)); "
            mycursor.execute(query)
            query = "select * from tempairplane"
            mycursor.execute(query)
            for x in mycursor:
                y = ",".join(map(str, x))
                y = y.split(',')
                if ("kg" in y[1]) or ("Cargo" in y[1]):
                    y[1] = "0"
                if ("kg" in y[2]) or ("Cargo" in y[2]) or ((y[1]) == "0"):
                    y[2] = "0"
                if "-" in y[7]:
                    temp = y[7].split('-')
                    y[7] = temp[1]
                if "-" in y[8]:
                    temp = y[8].split('-')
                    y[8] = temp[1]
                if "-" in y[9]:
                    temp = y[9].split('-')
                    y[9] = temp[1]
                if " " in y[9]:
                    temp = y[9].split(' ')
                    y[9] = temp[1]
                if "(" in y[9]:
                    y[9] = y[9].strip("(")
                if ")" in y[9]:
                    y[9] = y[9].strip(")")
                if "/" in y[9]:
                    temp = y[9].split("/")
                    y[9] = temp[2]
                if "-" in y[10]:
                    temp = y[10].split('-')
                    y[10] = temp[1]
                if " " in y[10]:
                    temp = y[10].split(' ')
                    y[10] = temp[1]
                if "(" in y[10]:
                    y[10] = y[10].strip("(")
                if ")" in y[10]:
                    y[10] = y[10].strip(")")
                if "/" in y[10]:
                    temp = y[10].split("/")
                    y[10] = temp[1]
                joined = ','.join(y)
                joined.strip(",")
                print(joined)
                writer.writerow([y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8], y[9], y[10], y[11], y[12], y[13], y[14]])





