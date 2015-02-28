# coding:utf-8

from peewee import (Proxy,
                    Model,
                    MySQLDatabase,
                    PostgresqlDatabase)
from playhouse.pool import PooledMySQLDatabase

db_proxy = Proxy()


def before_request_handler():
    db_proxy.connect()


def after_request_handler():
    db_proxy.close()


def use_mysql_database(config):
    """
    use peewee MySQLDatabase with Proxy
    """
    mysql_db = MySQLDatabase(
        database=config.mysql.get("database"),
        host=config.mysql.get("host"),
        port=config.mysql.get("port"),
        user=config.mysql.get("user"),
        password=config.mysql.get("password"),
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
        database=config.mysql.get("database"),
        host=config.mysql.get("host"),
        port=config.mysql.get("port"),
        user=config.mysql.get("user"),
        password=config.mysql.get("password"),

    )
    db_proxy.initialize(mysql_db)


def use_pgsql_database(config):
    """
    use peewee PostgresqlDatabase with Proxy
    """
    pgsql_db = PostgresqlDatabase(
        database=config.pgsql.get("database"),
        host=config.pgsql.get("host"),
        port=config.pgsql.get("port"),
        user=config.pgsql.get("user"),
        password=config.pgsql.get("password"),
    )
    db_proxy.initialize(pgsql_db)


class BaseModel(Model):

    class Meta:
        database = db_proxy
