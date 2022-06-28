from flask import Flask, jsonify, request, send_from_directory, render_template, abort, json, make_response, flash, \
    session, redirect, url_for, g
import sqlite3
from Database import Database

# Flask Config
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.from_object(__name__)

# DataBase Config
DB_MAIN = 'main.db'
dbaseItems = Database(sqlite3.connect(DB_MAIN))
dbaseSchedule = Database(sqlite3.connect(DB_MAIN))

# Отрисовка Json из БД
@app.route('/getJson', methods=['GET'])
def get_json():
    result = []
    table = dbaseItems.get_items()
    schedule = dbaseSchedule.get_schedule()
    for item in table:
        item_json = {'id': item[0], 'name': item[1], 'isBuyed': item[2], 'schedule': []}

        for i in schedule:
            if(i[1] == item[0]):
                schedule_json = {'id': i[0], 'relativeItemId': i[1], 'status': i[2],
                                 'startH': i[3], 'startM': i[4], 'endH': i[5], 'endM': i[6]}

                item_json['schedule'].append(schedule_json)

        result.append(item_json)

    return jsonify(result)

# Покупка предмета по id
@app.route('/buy/<id>', methods=['GET'])
def buy(id):
    dbaseItems.insert_state_by_id(id, 1)

    #Отрисовка Json
    return get_json()

# Продажа предмета по id
@app.route('/sell/<id>', methods=['GET'])
def sell(id):
    dbaseItems.insert_state_by_id(id, 0)

    # Отрисовка Json
    return get_json()

if __name__ == '__main__':
    # dbaseItems.create_db(DB_MAIN, "sq_db.sql")
    # dbaseItems.add_item('John')
    # dbaseItems.add_item('Ben')
    # dbaseItems.add_item('Alex')
    #
    # dbaseSchedule.create_db(DB_MAIN, "sq_db_schedule.sql")
    # dbaseSchedule.add_item_schedule(1, 'working', 8, 0, 18, 0)
    # dbaseSchedule.add_item_schedule(1, 'sleeping', 23, 0, 6, 0)
    #
    # dbaseSchedule.add_item_schedule(2, 'working', 6, 0, 12, 0)
    # dbaseSchedule.add_item_schedule(2, 'sleeping', 14, 0, 3, 0)
    #
    # dbaseSchedule.add_item_schedule(3, 'working', 12, 0, 18, 0)
    # dbaseSchedule.add_item_schedule(3, 'sleeping', 20, 0, 8, 0)

    app.run(debug=True, port=5000, host='0.0.0.0')