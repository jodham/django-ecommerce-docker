import base64
import requests

from datetime import datetime

from django.conf import settings



class MpesaClient:


    def __init__(self):

        self.consumer_key = settings.MPESA_CONSUMER_KEY

        self.consumer_secret = settings.MPESA_CONSUMER_SECRET

        self.shortcode = settings.MPESA_SHORTCODE

        self.passkey = settings.MPESA_PASSKEY

        self.callback_url = settings.MPESA_CALLBACK_URL


        self.base_url = (
            "https://sandbox.safaricom.co.ke"
        )



    def get_access_token(self):

        url = (
            f"{self.base_url}"
            "/oauth/v1/generate"
            "?grant_type=client_credentials"
        )


        response = requests.get(

            url,

            auth=(

                self.consumer_key,

                self.consumer_secret

            )

        )


        response.raise_for_status()


        return response.json()["access_token"]




    def normalize_phone(self, phone):

        phone = phone.replace(
            "+",
            ""
        ).replace(
            " ",
            ""
        )


        if phone.startswith("0"):

            phone = "254" + phone[1:]


        elif phone.startswith("7"):

            phone = "254" + phone


        return phone





    def generate_password(self):

        timestamp = datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )


        data = (

            self.shortcode

            +

            self.passkey

            +

            timestamp

        )


        password = base64.b64encode(

            data.encode()

        ).decode()


        return password, timestamp





    def stk_push(
        self,
        phone,
        amount,
        order_number
    ):


        access_token = self.get_access_token()


        phone = self.normalize_phone(
            phone
        )


        password, timestamp = (
            self.generate_password()
        )


        url = (
            f"{self.base_url}"
            "/mpesa/stkpush/v1/processrequest"
        )


        payload = {

            "BusinessShortCode":
                self.shortcode,

            "Password":
                password,

            "Timestamp":
                timestamp,

            "TransactionType":
                "CustomerPayBillOnline",

            "Amount":
                int(amount),

            "PartyA":
                phone,

            "PartyB":
                self.shortcode,

            "PhoneNumber":
                phone,

            "CallBackURL":
                self.callback_url,

            "AccountReference":
                str(order_number).replace("&", ""),

            "TransactionDesc":
                "LUXE AND CO Order Payment"

        }



        headers = {


            "Authorization":

                f"Bearer {access_token}",


            "Content-Type":

                "application/json"

        }



        response = requests.post(

            url,

            json=payload,

            headers=headers

        )


        if response.status_code != 200:

            print(response.text)


        response.raise_for_status()


        return response.json()