from abc import ABC, abstractmethod

class SendOTPGateway(ABC):

    def __init__(self, recipient):
        self.recipient = recipient
    
    @abstractmethod
    def send_otp(self, otp):
        pass


class SmsGateway(SendOTPGateway):

    def send_otp(self, otp):
        pass

class EmailGateway(SendOTPGateway):

    def send_otp(self, otp):
        pass