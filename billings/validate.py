from hashlib import md5
from django.contrib.sessions.serializers import PickleSerializer
from django.core.exceptions import SuspiciousOperation
from billings.models import ValidatedTransaction

class TransactionValidator(PickleSerializer):
    """
    Simple service to keep transactions validated

    Yeah, i wrote the service in the service, so you can research a service when researching a service
    """
    def _encode(self, obj):
        return self.dumps(obj)

    def _decode(self, data):
        return self.loads(data)

    def sign_data(self, data):
        m = md5()
        m.update(data)
        return m.hexdigest()

    def construct_sign(self, trz_data):
        enc_data = self._encode(trz_data)
        trz_sign = self.sign_data(enc_data)
        return (trz_sign + ":" + enc_data).encode("base64")

    def validate_sign(self, data_hash, trz_data):
        expected_hash = self.sign_data(trz_data)
        if data_hash != expected_hash:
            raise SuspiciousOperation("Transaction data corrupted")
        else:
            return True

    def get_sign_data(self, cookie_data):
        decoded_data = cookie_data.decode("base64")
        return decoded_data.split(":", 1)

    def invalidate(self, username, sign):
        transaction = ValidatedTransaction(username=username,
                                        tranzaction_id=sign,
                                        is_validated=False)

        transaction.save()

        trz_data = {"id": sign, "status":"processing"}
        return self.construct_sign(trz_data)

    def check_data_status(self, transaction_data):
        return True if (transaction_data["status"] == "processing") else False

    def validate(self, transaction, cookie_data):
        tranzaction = transaction[0]
        _hash, data = self.get_sign_data(cookie_data)
        if self.validate_sign(_hash, data):
            transaction_from_sign = self._decode(data)
            if transaction_from_sign["id"] == tranzaction.tranzaction_id:
                if self.check_data_status(transaction_from_sign):
                    tranzaction.is_validated = True
                    tranzaction.save()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False