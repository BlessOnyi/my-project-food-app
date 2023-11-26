from django.conf import settings
import paystackapi
# import requests

# class Paystack:
#     PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
#     base_url = "https://api.paystack.co/"

#     def verify_payment(self, ref, *args, **kwargs):
#         path = f'transaction/verify/{ref}'
#         headers = {
#             "Authorization": f"Bearer {self.PAYSTACK_SK}",
#             "Content-Type": "application/json",
#         }
#         url = self.base_url + path
#         response = requests.get(url, headers=headers)

#         if response.status_code == 200:
#             response_data = response.json()
#             return response_data['status'], response_data['data']

#         response_data = response.json()

#         return response_data['status'], response_data['message']



from django.conf import settings
class PaystackClient:
    def _init_(self):
        self.secret_key =settings.PAYSTACK_SECRET_KEY
        self.api = paystackapi.Paystack(secret_key=self.secret_key)