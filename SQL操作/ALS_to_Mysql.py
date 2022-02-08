import pymysql
import csv
import sys

host = '3.113.29.214'  # '3.113.29.214'
user = 'eric'  # 'eric'
passwd = '123456'  # '123456'
port = 3306
conninfo = {'host' : host ,'port' : port,'user' : user , 'passwd' : passwd, 'db' : 'recommendation_system','charset' : 'utf8mb4'}

def add_csv(path):
    try:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        csv_data = csv.reader(open(path))
        for row in csv_data:
            cursor.execute('INSERT INTO als(household_key, recommendations)'\
                           'VALUES("%s", "%s")',row)
        # close the connection to the database.
        conn.commit()
        print("Done")
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()
        print("db close")
def show_recommendation(customer_id):
    try:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        try:
            recommendation = f"""select recommendations from als where household_key = '{customer_id}'"""
            cursor.execute(recommendation)
            recommendation_item = cursor.fetchall()
            rec_list = []
            for i in recommendation_item[0][0].split(','):
                rec_list.append(i)
            return rec_list
        except:
            # 這邊丟內容協同過濾
            #err = "no history records"
            return False
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()
        print("db close")

def show_recommendation_item(commodity_desc):
    try:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        try:
            recommendation = f"""select recommendations from item_cf where commodity_desc like '%{commodity_desc}%'
                                 order by rand() limit 1 """
            cursor.execute(recommendation)
            recommendation_item = cursor.fetchall()
            rec_list = []
            for i in recommendation_item[0][0].split(','):
                rec_list.append(i)
            return rec_list
        except:
            # 這邊丟內容協同過濾
            err = "no history records"
            return err
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()
        print("db close")


def recommendation_detail(item_list):
    rec_list = []
    for i in item_list:
        rec_list.append(i)
    try:
        conn = pymysql.connect(host='3.113.29.214', user='eric', password='123456', port=3306, \
                             database="store_db", charset='utf8mb4')
        cursor = conn.cursor()
        item_dict = {}
        for i in rec_list:
            i = i.strip()
            try:
                item = f"""select * from product where commodity = '{i}' ORDER BY RAND() LIMIT 1"""
                cursor.execute(item)
                recommendation_item = cursor.fetchall()
                item_dict[i] = recommendation_item
            except:
                 item_dict[i] = 'no item record'
        return item_dict
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()
        print("db close")

def find_householdkey(customer_id):
    try:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        try:
            recommendation = f"""select household_key from als where household_key = '{customer_id}' """
            cursor.execute(recommendation)
            recommendation_item = cursor.fetchall()
            return 'True'
        except:
            return 'False'
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()
        print("db close")



if __name__ == '__main__':
    add_csv(path)
    show_recommendation(customer_id)
    show_recommendation_item(commodity_desc)
    recommendation_detail(item_list)
    find_householdkey(customer_id)
















