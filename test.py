import pytest
import requests

def test_ping_pong(client):
    response = client.get('/')
    assert response.data.decode('utf-8') == 'Pong', "Не корректное подключение"
    assert response.status_code == 200, "Неверный код ответа"    

def test_void_list(client, mock_dbf_table, mocker):
    mock_dbf_table.__iter__.return_value = iter([])
    mocker.patch('dbf.Table', return_value=mock_dbf_table)
    response = client.get('/scada/list/')
    assert response.status_code == 200, "Неверный код ответа"
    data = response.json
    assert data['len'] == 0, "Неверная длина ответа"
    assert data['response'] == {}, "Ответ содержит какие-то данные"

def test_list_of_one_string(client, mock_dbf_table, mocker):
    mock_record1 = mocker.MagicMock()
    mock_record1.__getitem__.side_effect = lambda x: 1 if x == 'ID' else 'Value1'
    mock_dbf_table.__iter__.return_value = iter([mock_record1])
    mocker.patch('dbf.Table', return_value=mock_dbf_table)
    response = client.get('/scada/list/')
    assert response.status_code == 200, "Неверный код ответа"
    data = response.json
    print("Содержимое data['response']:", data['response'])
    assert data['len'] == 1, "Неверная длина ответа"
    if isinstance(data['response'], list):
        assert data['response'][0]['ID'] == 1
    elif isinstance(data['response'], dict):
        assert '1' in data['response'], "Ключ '1' отсутствует в response"
        assert data['response']['1']['ID'] == 1, "Значение Ключа '1' отсутствует в response или некорректно"
        assert data['response']['1']['VALUE'] == 'Value1', "Значение Value '1' отсутствует в response или некорректно"        
    else:
        raise ValueError("Неизвестный тип response")
    
def test_list_of_two_string(client, mock_dbf_table, mocker):
    mock_record1 = mocker.MagicMock()
    mock_record1.__getitem__.side_effect = lambda x: 1 if x == 'ID' else 'Value1'
    mock_record2 = mocker.MagicMock()
    mock_record2.__getitem__.side_effect = lambda x: 2 if x == 'ID' else 'Value2'    
    mock_dbf_table.__iter__.return_value = iter([mock_record1,mock_record2 ])
    mocker.patch('dbf.Table', return_value=mock_dbf_table)
    response = client.get('/scada/list/')
    assert response.status_code == 200, "Неверный код ответа"
    data = response.json
    print("Содержимое data['response']:", data['response'])
    assert data['len'] == 2, "Неверная длина ответа"
    if isinstance(data['response'], list):
        assert data['response'][0]['ID'] == 1
    elif isinstance(data['response'], dict):
        assert '1' in data['response'], "Ключ '1' отсутствует в response"
        assert data['response']['1']['ID'] == 1, "Значение Ключа '1' отсутствует в response или некорректно"
        assert data['response']['1']['VALUE'] == 'Value1', "Значение Value '1' отсутствует в response или некорректно"  
        assert '2' in data['response'], "Ключ '2' отсутствует в response"
        assert data['response']['2']['ID'] == 2, "Значение Ключа '1' отсутствует в response или некорректно"
        assert data['response']['2']['VALUE'] == 'Value2', "Значение Value '2' отсутствует в response или некорректно"                
    else:
        raise ValueError("Неизвестный тип response")







