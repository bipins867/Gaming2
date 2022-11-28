import razorpay



key_id='rzp_test_roQ5X0haCDK1Gh'
key_sec='wjtRN0Li8cC8AEJKnC4WM5eB'

client=razorpay.Client(auth=(key_id,key_sec))


class Razor:


    def __init__(self):
        pass


    def createPaymentLink(self,amount,name=None,email=None,contact=None,callback_url="http://localhost:5000/dassboard/paymentSuccess",desc='Gaming Event'):
        #try:
            amount=amount*100
            if name is None:

                xr=client.payment_link.create({
                  "amount": amount,
                  "currency": "INR",
                  "description": desc,
                  "callback_url": callback_url,
                  "callback_method": "get"
                })
            else:

                xr=client.payment_link.create({
                  "amount": amount,
                  "currency": "INR",
                  "description": desc,
                  "customer": {
                    "name": name,
                    "email": email,
                    "contact": contact
                  },

                  "callback_url": callback_url,
                  "callback_method": "get"
                })
            return xr

        #except:

            return None


    def fetchPaymentByLinkId(self,link_id):

        data=client.payment_link.fetch(link_id)
        return data

    def fetchPayemtnById(self,p_id):

        data=client.payment.fetch(p_id)
        return data

    def fetchPaymentStatusByPLink(self,plink):
        data=self.fetchPaymentByLinkId(plink)
        return data['status']

    def fetchPaymentIdByPLink(self,plink):
        data=self.fetchPaymentByLinkId(plink)
        payment=data['payments']
        if payment is not None:
            return payment[0]['payment_id']


    def fetchPaymentLinkUrl(self,p_id):
        data=self.fetchPaymentByLinkId(p_id)
        return data['short_url']
