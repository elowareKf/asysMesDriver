import socket
import xml.etree.ElementTree as ElementTree


def receive_message(connection: socket.socket, client: any):
    data = connection.recv(2048).decode('utf-8')
    response = parse_message(data)
    connection.send(response)
    pass


def parse_message(message: str) -> bytes:
    tree = ElementTree.fromstring(message)
    if tree.tag != 'ASYS':
        return '<ERROR>Invalid message</ERROR>'.encode('utf-8')

    response = ElementTree.Element('ASYS')
    for child in tree:
        response.append(process(child))

    return ElementTree.tostring(response)


def process(message: ElementTree.Element) -> ElementTree.Element or None:
    print(message.tag)

    if message.tag == 'ALIVE_REQ':
        message.tag = 'ALIVE_RES'
        message.attrib.pop('version', None)
        return message

    if message.tag == 'STATE_CHANGE':
        return message

    if message.tag == 'INFO':
        return message

    if message.tag == 'ORDER_REQ':
        return message

    if message.tag == 'LOAD_SETUP_REQ':
        return message

    if message.tag == 'PANEL_IN_REQ':
        return message

    if message.tag == 'ITEM_IN_REQ':
        return message

    if message.tag == 'ITEM_OUT_REQ':
        return message

    if message.tag == 'PANEL_OUT_REQ':
        return message


    return None


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 3056))
    server.listen()
    while True:
        connection, client_address = server.accept()
        receive_message(connection, client_address)


main()
