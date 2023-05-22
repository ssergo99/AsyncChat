from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, mapper
from datetime import datetime


class Storage:
    class Users:
        def __init__(self, username):
            self.id = None
            self.username = username
            self.last_login = datetime.now().ctime()

    class UsersInChat:
        def __init__(self, user_id, login_at):
            self.id = None
            self.user = user_id
            self.login_at = login_at

    class Connections:
        def __init__(self, user, connected_with, connected_at):
            self.id = None
            self.user = user
            self.connected_with = connected_with
            self.connected_at = connected_at

    class ClientHistory:
        def __init__(self, name, login, cl_ip):
            self.id = None
            self.name = name
            self.login = login
            self.cl_ip = cl_ip

    def __init__(self):
        self.database_engine = create_engine('sqlite:///srv_db.db3',
                                             echo=False, pool_recycle=3600)
        self.metadata = MetaData()

        tb_users = Table('Users', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('username', String, unique=True),
                         Column('last_login', String)
                         )

        tb_users_in_chat = Table('UsersInChat', self.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('user', ForeignKey('Users.id'), unique=True),
                                 Column('login_at', String)
                                 )

        tb_connections = Table('Connections', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('user', ForeignKey('Users.id')),
                               Column('connected_with', String),
                               Column('connected_at', String)
                               )

        tb_logins = Table('ClientHistory', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('name', ForeignKey('Users.id')),
                               Column('login', String),
                               Column('cl_ip', String)
                               )

        self.metadata.create_all(self.database_engine)
        mapper(self.Users, tb_users)
        mapper(self.UsersInChat, tb_users_in_chat)
        mapper(self.Connections, tb_connections)
        mapper(self.ClientHistory, tb_logins)
        Database = sessionmaker(bind=self.database_engine)
        self.session = Database()
        self.session.query(self.UsersInChat).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):
        try:
            user = self.session.query(self.Users).filter_by(username=username).first()
            user.last_login = datetime.now().ctime()
        except AttributeError:
            self.session.rollback()
            user = self.Users(username)
            self.session.add(user)
            self.session.commit()
        add_user_in_chat = self.UsersInChat(user.id, datetime.now().ctime())
        add_login = self.ClientHistory(user.id, datetime.now().ctime(), ip_address)
        self.session.add(add_login)
        self.session.add(add_user_in_chat)
        self.session.commit()
        print(f"Подключен пользователь {username} - {ip_address}:{port}")

    def make_contact(self, username, contact):
        user = self.session.query(self.Users).filter_by(username=username).first()
        rez = self.session.query(self.Connections).filter_by(user=user.id, connected_with=contact).first()
        if not rez:
            connect = self.Connections(user.id, contact, datetime.now().ctime())
            self.session.add(connect)
            self.session.commit()
            print(f"Создан контакт {contact} для пользователя {username}")

    def user_logout(self, username):
        user = self.session.query(self.Users).filter_by(username=username).first()
        self.session.query(self.UsersInChat).filter_by(user=user.id).delete()
        self.session.commit()
        print(f"Отключен пользователь {username}")

    def get_users_in_chat(self):
        query = self.session.query(
            self.Users.username,
            self.UsersInChat.login_at
        ).join(self.Users)
        return query.all()

    def get_list_connections(self, username):
        query = self.session.query(self.Users.username,
                                   self.Connections.connected_with,
                                   self.Connections.connected_at
                                   ).join(self.Users)
        query = query.filter(self.Users.username == username)
        return query.all()

    def get_list_logins(self, username):
        query = self.session.query(self.Users.username,
                                   self.ClientHistory.login,
                                   self.ClientHistory.cl_ip
                                   ).join(self.Users)
        query = query.filter(self.Users.username == username)
        return query.all()


if __name__ == '__main__':
    test_db = Storage()

