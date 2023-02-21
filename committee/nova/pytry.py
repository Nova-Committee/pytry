from __future__ import annotations


def try_of(supplier):
    try:
        return Success(supplier())
    except Exception as e:
        return Failure(e)


def try_lazy(supplier):
    return Lazy(supplier)


class Try:

    def run(self):
        pass

    def is_success(self) -> bool:
        pass

    def is_failure(self) -> bool:
        pass

    def get(self):
        pass

    def get_or_else(self, default):
        pass

    def foreach(self, fun):
        pass

    def failed(self) -> Try:
        pass


class Success(Try):
    __value = None

    def __init__(self, value):
        self.__value = value

    def run(self) -> Success:
        return self

    def is_success(self) -> bool:
        return True

    def is_failure(self) -> bool:
        return False

    def get(self):
        return self.__value

    def get_or_else(self, default):
        return self.get()

    def foreach(self, fun):
        fun(self.__value)

    def failed(self) -> Failure:
        return Failure(TypeError("Cannot use failed in a Success!"))


class Failure(Try):
    __exception = None

    def __init__(self, exception):
        self.__exception = exception

    def run(self) -> Failure:
        return self

    def is_success(self) -> bool:
        return False

    def is_failure(self) -> bool:
        return True

    def get(self):
        raise self.__exception

    def get_or_else(self, default):
        return default

    def foreach(self, fun):
        pass

    def failed(self) -> Success:
        return Success(self.__exception)


class Lazy(Try):
    __supplier = None

    def __init__(self, supplier):
        self.__supplier = supplier

    def run(self) -> Try:
        return try_of(self.__supplier)

    def is_success(self) -> bool:
        return self.run().is_success()

    def is_failure(self) -> bool:
        return self.run().is_failure()

    def get(self):
        return self.run().get()

    def get_or_else(self, default):
        return self.run().get_or_else(default)

    def foreach(self, fun):
        return self.run().foreach(fun)

    def failed(self) -> Try:
        return self.run().failed()
