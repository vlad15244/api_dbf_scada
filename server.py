from flask import Flask, request, jsonify
import dbf

app = Flask(__name__)


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
    id_new = request.get_json()['ID']
    name_new = request.get_json()['VALUE']
  

    with dbf.Table('example.dbf') as some_table:
        some_table.open(dbf.READ_WRITE)
        some_table.append({'ID' : id_new, 'VALUE' : name_new})

    return jsonify({
        'id': id_new,
        'name' : name_new,
        'status': 'NEW'
    }), 201   

@app.route('/scada/update/<id>', methods=['POST'])
def get_update():
    id_new = request.get_json()['ID']
    name_new = request.get_json()['VALUE']
 
    with dbf.Table('example.dbf') as some_table:
        for record in some_table:
            if record.id == id_new:
                dbf.replace(record, name = name_new)
                break

    some_table.close()


    return jsonify({
        'id': id_new,
        'name' : name_new,
        'status': 'EDIT'
    }), 201 


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
