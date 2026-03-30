from flask import Flask, request, jsonify
import dbf

app = Flask(__name__)


@app.route('/')
def get_ping():
    return 'Pong', 200

@app.route('/scada/list/', methods=['GET'])
def get_list():
    """получение всех список из базы данных"""
    with dbf.Table('example.dbf') as table:
        field_names = table.field_names
        result = {}

        # Итерируем по записям с индексами (id)
        for i, record in enumerate(table, start=1):
            record_dict = {}
            for field_name in field_names:
                value = record[field_name]
                # Обрабатываем bytes, если есть
                if isinstance(value, bytes):
                    value = value.decode('utf-8', errors='ignore').strip()
                record_dict[field_name] = value
            # Добавляем запись в итоговый словарь с ключом‑id
            result[i] = record_dict

    data = {}
    data['len'] = len(result)   
    data['response'] = result
    return data, 200

@app.route('/scada/new/', methods=['POST'])
def get_new():

    data = request.get_json()
    id_new = data['ID']
    name_new = data['VALUE']
  
    with dbf.Table('example.dbf') as some_table:
        some_table.open(dbf.READ_WRITE)
        some_table.append({'ID' : id_new, 'VALUE' : name_new})

    return jsonify({
        'id': id_new,
        'name' : name_new,
        'status': 'NEW'
    }), 201   

@app.route('/scada/update/<id>', methods=['POST'])
def get_update(id):

    name_new = request.get_json()['VALUE']

    table = dbf.Table('example.dbf')
    table.open(mode=dbf.READ_WRITE)

    for record in dbf.Process(table):
        if str(record.id) == str(float(id)):
            record.value = name_new

    return jsonify({
        'id': id,
        'name' : name_new,
        'status': 'EDIT'
    }), 201 


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
