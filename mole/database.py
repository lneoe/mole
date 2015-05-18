# coding:utf-8

import logging
from peewee import (Proxy,
                    Model,
                    MySQLDatabase,
                    PostgresqlDatabase)
from playhouse.pool import PooledMySQLDatabase

db_proxy = Proxy()


def before_request_handler():
    logging.debug("before_request_handler run db_proxy.connect()")
    db_proxy.connect()

db_conn = before_request_handler


def after_request_handler():
    logging.debug("after_request_handler run db_proxy.close()")
    db_proxy.close()

db_close = after_request_handler


def use_mysql_database(config):
    """
    use peewee MySQLDatabase with Proxy
    """
    mysql_db = MySQLDatabase(
        database=config.MYSQL.get("DATABASE"),
        host=config.MYSQL.get("HOST"),
        port=config.MYSQL.get("PORT"),
        user=config.MYSQL.get("USER"),
        password=config.MYSQL.get("PASSWORD"),
        threadlocals=True,
    )
    db_proxy.initialize(mysql_db)


def use_mysql_database_with_pool(config, max_connections=20,
                                 stale_timeout=300):
    """
    use peewee MySQLDatabase with Proxy
    """
    mysql_db = PooledMySQLDatabase(
        max_connections=max_connections,
        stale_timeout=stale_timeout,
        database=config.MYSQL.get("DATABASE"),
        host=config.MYSQL.get("HOST"),
        port=config.MYSQL.get("PORT"),
        user=config.MYSQL.get("USER"),
        password=config.MYSQL.get("PASSWORD"),

    )
    db_proxy.initialize(mysql_db)


def use_pgsql_database(config):
    """
    use peewee PostgresqlDatabase with Proxy
    """
    pgsql_db = PostgresqlDatabase(
        database=config.PGSQL.get("DATABASE"),
        host=config.PGSQL.get("HOST"),
        port=config.PGSQL.get("PORT"),
        user=config.PGSQL.get("USER"),
        password=config.PGSQL.get("PASSWORD"),
    )
    db_proxy.initialize(pgsql_db)


class BaseModel(Model):

    class Meta:
        database = db_proxy

    @property.getter
    def pk(self):
        return self.get_id()

    @property.setter
    def pk(self, value):
        return self.set_id(value)
