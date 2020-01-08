import socket
import xml.etree.ElementTree as ElementTree
from datetime import datetime
import ErpConnection


def receive_message(connection: socket.socket, client: any):
    data = connection.recv(2048).decode('utf-8')
    try:
        response = parse_message(data)
        if response is not None:
            connection.send(response)

    except Exception as error:
        print(error)
        log(data)


def parse_message(message: str) -> bytes or None:
    tree = ElementTree.fromstring(message)
    if tree.tag != 'ASYS':
        return '<ERROR>Invalid message</ERROR>'.encode('utf-8')

    response = ElementTree.Element('ASYS')
    for child in tree:
        processed = process(child)
        if processed is not None:
            response.append(processed)

    if ElementTree.tostring(response).__len__() > 13:
        return ElementTree.tostring(response)

    return None


def log(entry: str):
    when = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(when + ' - ' + entry)


def process(message: ElementTree.Element) -> ElementTree.Element or None:
    log(ElementTree.tostring(message).decode('UTF-8').replace('\r', '').replace('\n', '').replace('\t', ''))

    station = message.attrib['station']
    message_id = message.attrib['messageid']

    answer = ElementTree.Element('INSERT_TAG')
    answer.attrib['messageid'] = message_id
    answer.attrib['station'] = station

    if message.tag == 'ALIVE_REQ':
        message.tag = 'ALIVE_RES'
        message.attrib.pop('version', None)
        return message

    if message.tag == 'STATE_CHANGE':
        return None

    if message.tag == 'INFO':
        return None

    if message.tag == 'ORDER_REQ':
        return message

    if message.tag == 'LOAD_SETUP_REQ':
        answer.tag = 'LOAD_SETUP_RES'
        erp = ErpConnection.Erp()
        program = erp.get_program(message.attrib['refcode'])
        if program is not None:
            answer.attrib['program'] = program
            answer.attrib['state'] = '1'
        else:
            answer.attrib['state'] = '0'
            answer.attrib['error_text'] = 'Kein Programm im ERP angegeben'

        return answer

    if message.tag == 'PANEL_IN_REQ':
        return message

    if message.tag == 'ITEM_IN_REQ':
        answer.tag = 'ITEM_IN_RES'
        answer.attrib['state'] = '1'
        return answer

    if message.tag == 'ITEM_OUT_REQ':
        answer.tag = 'ITEM_OUT_RES'
        answer.attrib['state'] = '1'
        return answer

    if message.tag == 'PANEL_OUT_REQ':
        answer.tag = 'PANEL_OUT_RES'
        answer.attrib['state'] = '1'
        return answer

    return None


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 3056))
    server.listen()
    while True:
        connection, client_address = server.accept()
        receive_message(connection, client_address)


main()
