from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, mapper
from datetime import datetime


class ClStorage:
    class Contacts:
        def __init__(self, connected_with):
            self.id = None
            self.connected_with = connected_with

    class MessageHistory:
        def __init__(self, send_from, send_to, msg_text):
            self.id = None
            self.sender = send_from
            self.receiver = send_to
            self.msg_text = msg_text
            self.created_at = datetime.now()

    def __init__(self, clname):
        self.database_engine = create_engine(f'sqlite:///{clname}_db.db3',
                                             echo=False, pool_recycle=3600,
                                             connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        tb_contacts = Table('Contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('connected_with', String, unique=True)
                         )

        tb_msg_history = Table('MessageHistory', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('sender', String),
                               Column('receiver', String),
                               Column('msg_text', String),
                               Column('created_at', DateTime)
                               )

        self.metadata.create_all(self.database_engine)
        mapper(self.Contacts, tb_contacts)
        mapper(self.MessageHistory, tb_msg_history)
        Database = sessionmaker(bind=self.database_engine)
        self.session = Database()
        self.session.commit()

    def create_contact(self, contname):
        if self.session.query(self.Contacts).filter_by(connected_with=contname).first():
            print('Такой контакт уже есть в вашей базе')
            return False
        else:
            return True

    def make_contact_from_serv(self, contactlist):
        self.session.query(self.Contacts).delete()
        for contact in contactlist:
            connect = self.Contacts(contact)
            self.session.add(connect)
        self.session.commit()

    def store_message_in_db(self, sender, receiver, message_text):
        add_message = self.MessageHistory(sender, receiver, message_text)
        self.session.add(add_message)
        self.session.commit()
        print(f"В бд сохранено сообщение пользователя {sender} к {receiver}")



if __name__ == '__main__':
    test_db = ClStorage()