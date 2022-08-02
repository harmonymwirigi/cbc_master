# from flask import Flask, request
# from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
# from cbc import db
# from cbc.model import School
#
#
#
# school_put_agrs = reqparse.RequestParser()
# school_put_agrs.add_argument("school_name", type = str, help = "field required", required = True)
# school_put_agrs.add_argument("School_Email", type = str, help = "field required", required = True)
# school_put_agrs.add_argument("phone_number", type = str, help = "field required", required = True)
# school_put_agrs.add_argument("password", type = str, help = "field required", required = True)
# school_put_agrs.add_argument("confirm_password", type = str, help = "field required", required = True)
# school_put_agrs.add_argument("type", type = str, help = "field required", required = True)
#
# ResourceField = {
#     'school_name': fields.String,
#     'School_Email': fields.String,
#     'password': fields.String,
#     'confirm_password': fields.String,
#     'type': fields.String,
#     'phone_number': fields.String
#
# }
#
# class Skul(Resource):
#     @marshal_with(ResourceField)
#     def put(self, email):
#         arguments = school_put_agrs.parse_args()
#         result = School.query.filter_by(email = email).first()
#         if result:
#             abort(409, message = "the school already exist")
#         school = School(School_Name = arguments['school_name'],
#                         School_Email = arguments['School_Email'],
#                         Password = arguments['password'],
#                         Confirm_Password = arguments['confirm_password'],
#                         Phone_Number = arguments['confirm_password'],
#                         type = arguments['type']
#                         )
#         db.session.add(school)
#         db.session.commit()
#         return school, 201



