class OrderAlreadyCancelledException(Exception):
    pass


class OrderAlreadyPaidException(Exception):
    pass


class PaymentNotVerifiedException(Exception):
    pass