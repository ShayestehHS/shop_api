import json

import requests
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response

from order.models import Order


def send_request_to_zp(request, order: Order, amount, email, mobile=None, description=settings.DEFAULT_ZP_DESCRIPTION):
    req_data = {
        "merchant_id": settings.MERCHANT,
        "amount": amount,  # Rial / Required
        "callback_url": request.build_absolute_uri(reverse('order:zp_verify')),
        "description": description,
        "metadata": {"email": email}
    }
    if mobile:
        req_data['metadata']['mobile'] = mobile

    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=settings.ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)

    try:
        authority = req.json()['data']['authority']
    except TypeError:
        print("-- WE HAVE PROBLEM IN AUTHORITY IN (send_request_to_zp) --")
        print(f"-- (req) IS: {req} --")
        print(f"-- (req.json) IS: {req.json()} --")
        print(f"-- (req.json()['data']) IS: {req.json()['data']} --")
        return Response({'ERROR': 'Error in getting authority'}, status=500)

    if len(req.json()['errors']) != 0:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return Response({"Error code": e_code, "Error Message": e_message}, status=500)

    order.authority = authority
    order.save(update_fields=['authority'])
    return redirect(settings.ZP_API_START_PAY.format(authority=authority))


def create_response_base_on_post_res(res_post):
    if len(res_post.json()['errors']) != 0:
        e_code = res_post.json()['errors']['code']
        e_message = res_post.json()['errors']['message']

        return Response({"Error code": e_code, "Message": e_message}, status=400)

    request_data = res_post.json()['data']  # https://docs.zarinpal.com/paymentGateway/guide/
    t_status = request_data['code']
    if t_status == 100:
        ref_id = str(request_data["ref_id"])
        response = Response({'Result': "Transaction success.", "RefID": ref_id}, status=200)

    elif t_status == 101:
        message = str(request_data['message'])
        response = Response({'Result': "Transaction submitted", "Message": message}, status=204)

    else:
        message = str(request_data['message'])
        response = Response({'Result': 'Transaction failed.', 'Message': message}, status=400)
    return response
