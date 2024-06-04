from odoo import http
from odoo.http import request

from werkzeug.wrappers import Response
import json


class CallCenterCrmController(http.Controller):
    @http.route('/api/v1/crm/create', type='http', auth='none', methods=['POST'], csrf=False)
    def api_create_leads(self):
        try:
            request_body = json.loads(http.request.httprequest.data.decode('latin1'))
            client_ip = request.httprequest.remote_addr

            # Find source record based on client IP
            source_rec = http.request.env['source.source'].sudo().search([('ips_from_source_ids.name', '=', client_ip)],
                                                                         limit=1)

            if not source_rec:
                return Response(json.dumps({'error': 'You are not eligible to use our API!'}),
                                content_type='application/json;charset=utf-8', status=401)

            # Find or create person record
            person_name = request_body['person']['name']
            person_rec = http.request.env['person.person'].sudo().search([('name', '=', person_name)], limit=1)

            if not person_rec:
                person_rec = http.request.env['person.person'].sudo().create(request_body['person'])

            # Update phone number and email records with source and person IDs
            phone_number_data = request_body['phone_number_id']
            phone_number_data.update({'source': source_rec.id, 'person_id': person_rec.id})
            email_data = request_body['person_email_id']
            email_data.update({'source': source_rec.id, 'person_id': person_rec.id})

            # Create phone number record if not exists
            phone_number = http.request.env['phone.number'].sudo().search(
                [('phone_number', '=', phone_number_data['phone_number']), ('person_id', '=', person_rec.id)], limit=1)
            if not phone_number:
                http.request.env['phone.number'].sudo().create(phone_number_data)

            # Create email record if not exists
            email = http.request.env['person.email'].sudo().search(
                [('email', '=', email_data['email']), ('person_id', '=', person_rec.id)], limit=1)
            if not email:
                http.request.env['person.email'].sudo().create(email_data)

            # Return success response
            return Response(json.dumps({'message': 'Lead created successfully'}),
                            content_type='application/json;charset=utf-8', status=200)

        except ValueError as ve:
            return Response(json.dumps({'error': 'Invalid JSON data: {}'.format(ve)}),
                            content_type='application/json;charset=utf-8', status=400)

        except Exception as exc:
            return Response(json.dumps({'error': str(exc)}), content_type='application/json;charset=utf-8', status=500)

    # @http.route('/api/v1/generate_token', type='http', auth='none', methods=['POST'], csrf=False)
    # def api_create_user(self):
    #     body = {
    #         "__last_update": False,
    #         "image_1920": False,
    #         "company_ids": [
    #             [
    #                 6,
    #                 False,
    #                 [
    #                     1
    #                 ]
    #             ]
    #         ],
    #         "company_id": 1,
    #         "sel_groups_1_10_11": 1,
    #         "sel_groups_19": False,
    #         "sel_groups_2_4": False,
    #         "in_group_12": False,
    #         "in_group_18": False,
    #         "in_group_17": False,
    #         "in_group_8": False,
    #         "in_group_16": False,
    #         "in_group_9": False,
    #         "in_group_6": False,
    #         "in_group_5": False,
    #         "in_group_7": True,
    #         "in_group_3": False,
    #         "in_group_14": False,
    #         "in_group_13": False,
    #         "in_group_15": False,
    #         "active": True,
    #         "lang": "en_US",
    #         "tz": "Europe/Berlin",
    #         "action_id": False,
    #         "notification_type": "email",
    #         "odoobot_state": False,
    #         "signature": "<p data-o-mail-quote=\"1\">--<br data-o-mail-quote=\"1\">151</p>"
    #     }
    #     response_content = {'message': 'Ok'}
    #     try:
    #         # Create a new phone number record
    #         request_body = json.loads(http.request.httprequest.data.decode('latin1'))
    #         body.update(request_body)
    #         user_rec = http.request.env['res.users'].sudo().create(body)
    #         key_rec = http.request.env['res.users.apikeys'].sudo().create(
    #             {'user_id': user_rec.id, 'name': user_rec.name, 'scope': 0})
    #         a = key_rec.sudo(user_rec.id)._generate(key_rec.scope, key_rec.name)
    #         print()
    #         print()
    #         print()
    #         # Return a JSON response
    #         return Response(json.dumps(response_content), content_type='application/json;charset=utf-8', status=200)
    #     except Exception as exc:
    #         return Response(json.dumps({"error": str(exc)}), content_type='application/json;charset=utf-8', status=500)
    #
    #
# self.write({'vat': False, 'fromDate': False, 'toDate': False, 'party': False, 'fic': self.fic})
