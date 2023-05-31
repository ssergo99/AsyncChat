import json


def get_msg(client):
    encoded_response = client.recv(1024)
    return encoded_response


def send_msg(new_socket, message_to_send):
    json_message = json.dumps(message_to_send)
    enc_message_to_send = json_message.encode('utf-8')
    new_socket.send(enc_message_to_send)
