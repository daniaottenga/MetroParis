from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM fermata")
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def hasconn(u: Fermata, v: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM connessione "
                 "WHERE id_stazP = %s and id_stazA = %s ")
        cursor.execute(query, (u.id_fermata, v.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0 # se la len è >0 avrò TRUE altrimenti FALSE


    @staticmethod
    def getVicini(u):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM connessione "
                 "WHERE id_stazP = %s")
        cursor.execute(query, (u.id_fermata,))

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM connessione ")
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT id_stazP, id_stazA, count(*) as peso "
                 "FROM connessione c "
                 "GROUP BY id_stazP, id_stazA "
                 "ORDER BY peso DESC")
        cursor.execute(query)

        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["peso"]))
        cursor.close()
        conn.close()
        return result