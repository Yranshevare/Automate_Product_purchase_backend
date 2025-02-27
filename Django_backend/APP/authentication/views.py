from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import UserModel
from utils.utils import encrypt_data, decrypt_data
from django.core.mail import send_mail
from APP import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMessage

import json
import random
import threading


@csrf_exempt
def registerUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            required_fields = ['username', 'email', 'mobileNo', 'proffesion', 'password', 'gender']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
            

            user = UserModel.objects.filter(username=data['username']).first() 

            if user:
                return JsonResponse({'error': 'User already exists'}, status=400)


            if not data.get('password'):
                return JsonResponse({'error': 'Password not provided'}, status=400)
            
            user = UserModel(
                username=data['username'],
                email=data['email'],
                mobile=data['mobileNo'],
                profession=data['proffesion'],
                password=make_password(data['password']),
                gender=data['gender'],
                isEmailVerified=data.get('isEmailVerified', False)  # Default to False
            )
            # print(user.gender)

            try:
                user.save()
            except Exception as e:
                return JsonResponse({'error': f"Error saving user: {e}"}, status=400)


            return JsonResponse({
                'message': 'User registered successfully',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'mobileNo': str(user.mobile),
                    'proffesion': user.profession,
                    'gender': user.gender,
                    'isEmailVerified': user.isEmailVerified
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': 'error while registering user'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt   
def login(request):
    if request.method == 'GET':
        try:

            if 'access_token' in request.COOKIES:
                return JsonResponse({"message":'already login'},status=200)
            
            data = json.loads(request.body)
    

            user = UserModel.objects.filter(username=data['username']).first() 

            if not user:
                return JsonResponse({"message":'user not found'}, status=404)

            if not check_password( data['password'],user.password):
                return JsonResponse({"message":'invalid password'},status=400)
            
            encrypted_data = encrypt_data(user.username,user.email,user._id)
        
            response = JsonResponse({"message":'login successfully'},status=200)

            # setting cookies
            response.set_cookie('access_token', encrypted_data)

            return response
        except Exception as e:
            return JsonResponse({'error': 'error while login'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt   
def logout(request):
    if request.method == 'GET':
        try:
            if 'access_token' not in request.COOKIES:
                return JsonResponse({"message":"user doesn't exist"},status=200)
            response = JsonResponse({"message":'logout successfully'},status=200)
            response.delete_cookie('access_token')

            if 'process_token' in request.COOKIES:
                response.delete_cookie('process_token')
            return response 
        except Exception as e:
            return JsonResponse({'error': 'error while logout'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

otp = None
def resetOTP():
    global otp
    otp = None

@csrf_exempt    
def generateOTP(request):
    if request.method == 'GET':
        try:
            if 'access_token' not in request.COOKIES:
                return JsonResponse({"message":"user doesn't exist"},status=200)
            
            # get access token from cookies
            access_token = request.COOKIES['access_token']
            # decrypt access token
            decrypted_data = decrypt_data(access_token)
            
            
            
            # Generate the 4 digit OTP
            global otp
            otp = random.randint(100000, 999999)

            # send email with otp
            subject = "verifying your email"
            # message = "your verifying opt is \n " + str(otp) + "\n it will be valid for 5 minutes only"

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [decrypted_data['email']]

           
            
            # HTML content of the email
            html_content = f"""
            <html>
                <body>
                  <h1>Welcome to Automate Product Purchase Platform!</h1>
                  <p>Thank you for registering with us! We're excited to have you on board.</p>

                  <p>To complete your registration and start using our website, please verify your email address by entering the One-Time Password (OTP) below:</p>

                  <h2>Your OTP: <strong>{otp}</strong></h2>

                  <p><b>Note: This OTP is valid for the next 5 minutes. Once verified, you can fully enjoy all our services.</b></p>

                  <p>If you did not create an account on Automate Product Purchase Platform, please ignore this email or contact our support team.</p>

                  <p>Thank you for joining us, and we look forward to having you as part of our community!</p>

                  
                  <p>Best regards,</p>
                  <p>The Automate Product Purchase Platform Team</p>

                  <p><em> please do not reply.</em></p>
                </body>
            </html>
            """

            email = EmailMessage(subject, html_content, from_email, recipient_list)
            email.content_subtype = "html"  # Mark content as HTML
            email.send()


            # reset the otp after 5 minutes
            threading.Timer(60*5, resetOTP).start()
            
            return JsonResponse({"message":'otp generated successfully'},status=200)
        except Exception as e:
            return JsonResponse({'error': 'error while generating otp'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt    
def verifyOTP(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            # Ensure OTP is provided in the request
            if 'otp' not in data:
                return JsonResponse({"message": "OTP is required"}, status=400)
            
            if data['otp'] != otp:
                return JsonResponse({"message":"invalid otp"},status=400)
            
            if 'access_token' not in request.COOKIES:
                return JsonResponse({"message":"Unauthorized requested"},status=401)
            
             # get access token from cookies
            access_token = request.COOKIES['access_token']
            # decrypt access token
            decrypted_data = decrypt_data(access_token)

            # get user by email
            user = UserModel.objects.filter(email=decrypted_data['email']).first()

            if not user:
                return JsonResponse({"message":"user doesn't exist"},status=404)
            
            
            # change isEmailVerified to true
            user.isEmailVerified = True
            user.save()

            # reset the otp
            resetOTP()

            return JsonResponse({"message":'otp verified successfully'},status=200)
        except Exception as e:
            return JsonResponse({'error': 'error while verifying otp',"message":str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)