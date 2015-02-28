# coding: utf-8

import pickle
import logging


class Session(object):
    __slots__ = ("_store", "_sessionid", "_data", "_loaded")

    def __init__(self, store):
        self._store = store
        self._loaded = False
        self._data = dict()

    @property
    def sessionid(self):
        return self._sessionid

    @sessionid.setter
    def sessionid(self, value):
        self._sessionid = value

    def save(self, sessionid, expires_days=None):
        rtn = self._store.save(
            sessionid=sessionid,
            data=self._data,
            expires_days=expires_days
        )
        return rtn

    def load(self, sessionid):
        self._sessionid = sessionid
        self._data = self._store.load(sessionid)
        self._loaded = True
        return self

    def clear(self, sessionid):
        rtn = self._store.clear(sessionid)
        return rtn

    def get(self, name, default=None):
        try:
            return self.__getitem__(name)
        except KeyError:
            return default

    def __setattr__(self, name, value):
        if name in self.__slots__:
            object.__setattr__(self, name, value)
        else:
            self._data.__setitem__(name, value)

    def __getattr__(self, name):
        return self._data.__getitem__(name)

    def __setitem__(self, name, value):
        self._data.__setitem__(name, value)

    def __getitem__(self, name):
        return self._data.__getitem__(name)

    def __delattr__(self, name):
        self._data.__delattr__(name)


class SessionDataNotExist(Exception):
    pass


class SessionStore(object):

    def __init__(self, *args, **kwargs):
        pass

    def load(self, sessionid):
        """
        return session data
            type(data), dict
        if session was expired you must do something
        """
        print("This is SessionStore load-function")
        raise NotImplementedError

    def save(self, sessionid, data, expires_days=None):
        """
        store session data to Storage like redis or memacache
        """
        raise NotImplementedError

    def clear(self, sessionid):
        """
        clear session data
        """
        raise NotImplementedError


class RedisStore(SessionStore):

    def __init__(self, redis):
        self.redis = redis

    def load(self, sessionid):
        data = self.redis.get(sessionid)
        if not data:
            logging.debug("[RedisStore] Session Data was empty[{0}]"
                          .format(sessionid))
            return dict(username=None)

        logging.debug("[RedisStore]Session [{0}]: {1}"
                      .format(sessionid, pickle.loads(data)))
        return pickle.loads(data)

    def save(self, sessionid, data, expires_days=None):
        # dumplicate data use pickle or json, I used pickle
        session_data = pickle.dumps(data)
        logging.debug("[RedisStore]Save Session [{0}]: {1}, expires_days:{2}"
                      .format(sessionid, data, expires_days))

        done = self.redis.set(sessionid, session_data)
        if done and expires_days:
            self.redis.expire(sessionid, expires_days * 24 * 3600)
        # else:
        #     self.redis.expire(sessionid, 1 * 24 * 3600)
        return done

    def clear(self, sessionid):
        return self.redis.delete(sessionid)
