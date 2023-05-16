import dis


class ClientVerifier(type):
    def __init__(cls, clsname, bases, clsdict):
        chk_methods = []
        chk_socket = []
        for method in clsdict:
            try:
                dis_res = dis.get_instructions(clsdict[method])
            except TypeError:
                pass
            else:
                for dis_item in dis_res:
                    if dis_item.opname == 'LOAD_GLOBAL':
                        print(dis_item)
                        if dis_item.argval not in chk_methods:
                            chk_methods.append(dis_item.argval)
                    if dis_item.opname == 'LOAD_ATTR':
                        if dis_item.argval not in chk_socket:
                            chk_socket.append(dis_item.argval)
        if 'accept' in chk_methods or 'listen' in chk_methods:
            raise TypeError('Нельзя вызывать accept или listen !!!')
        if 'socket' in chk_methods:
            raise TypeError('Нельзя создавать сокеты на уровне класса !!!')
        if not 'socket' in chk_socket:
            raise TypeError('Используйте сокеты для работы по TCP.')
        super().__init__(clsname, bases, clsdict)
