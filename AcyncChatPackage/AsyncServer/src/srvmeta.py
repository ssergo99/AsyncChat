import dis


class ServerVerifier(type):
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for method in clsdict:
            try:
                dis_res = dis.get_instructions(clsdict[method])
            except TypeError:
                pass
            else:
                for dis_item in dis_res:
                    if dis_item.opname == 'LOAD_GLOBAL':
                        if dis_item.argval not in methods:
                            methods.append(dis_item.argval)
        if 'connect' in methods:
            raise TypeError('Нельзя вызывать connect !!!')

        if not ('SOCK_STREAM' in methods and 'AF_INET' in methods):
            raise TypeError('Создайте сокет для работы по TCP.')
        super().__init__(clsname, bases, clsdict)
