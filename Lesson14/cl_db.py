from time import time

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Boolean, DateTime, Text
from sqlalchemy.orm import sessionmaker, mapper
from datetime import datetime


class ClStorage:
    class Contacts:
        def __init__(self, connected_with):
            self.id = None
            self.connected_with = connected_with

    class Users:
        def __init__(self, username):
            self.id = None
            self.username = username

    class MessageHistory:
        def __init__(self, send_from, inc_flag, msg_text):
            self.id = None
            self.sender = send_from
            self.incoming_msg = inc_flag
            self.msg_text = msg_text
            self.created_at = datetime.now()

    def __init__(self, clname):
        self.database_engine = create_engine(f'sqlite:///{clname}_db.db3',
                                             echo=False, pool_recycle=3600,
                                             connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        tb_contacts = Table('Contacts', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('connected_with', String, unique=True),
                            )

        tb_users = Table('Users', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('username', String, unique=True)
                         )

        tb_msg_history = Table('MessageHistory', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('sender', String),
                               Column('incoming_msg', Boolean),
                               Column('msg_text', String),
                               Column('created_at', DateTime)
                               )

        self.metadata.create_all(self.database_engine)
        mapper(self.Contacts, tb_contacts)
        mapper(self.Users, tb_users)
        mapper(self.MessageHistory, tb_msg_history)
        Database = sessionmaker(bind=self.database_engine)
        self.session = Database()
        self.session.commit()

    def check_contact(self, contname):
        if self.session.query(self.Contacts).filter_by(connected_with=contname).first():
            print('Такой контакт есть в вашей базе')
            return True
        else:
            return False

    def add_contact(self, contact):
        connect = self.Contacts(contact)
        self.session.add(connect)
        self.session.commit()

    def del_contact(self, contact1):
        self.session.query(self.Contacts).filter_by(connected_with=contact1).delete()

    # def make_contact_from_serv(self, contactlist):
    #     self.session.query(self.Contacts).delete()
    #     for contact in contactlist:
    #         connect = self.Contacts(contact)
    #         self.session.add(connect)
    #     self.session.commit()

    def fill_users_from_serv(self, userslist):
        self.session.query(self.Users).delete()
        for user in userslist:
            connect1 = self.Users(user)
            self.session.add(connect1)
        self.session.commit()

    def store_message_in_db(self, contact, msg_flag, message_text):
        add_message = self.MessageHistory(contact, msg_flag, message_text)
        self.session.add(add_message)
        self.session.commit()

    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacts.connected_with).all()]

    def get_users(self):
        return [user[0] for user in self.session.query(self.Users.username).all()]

    def get_message_from_db(self, username):
        query = self.session.query(self.MessageHistory).filter_by(sender=username)
        return [(message.sender, message.incoming_msg, message.msg_text, message.created_at)
                for message in query.all()]


if __name__ == '__main__':
    test_db = ClStorage()
