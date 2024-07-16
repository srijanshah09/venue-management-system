from django.core.mail import send_mail
from django.conf import settings
import re
from rest_framework_simplejwt.tokens import RefreshToken
import random as r


from .models import User, Otp


def validate_password(password):
    if len(password) < 6:
        return False
    return True


def is_email(input):
    pat = re.compile(
        "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    )
    m = pat.match(input)
    if m:
        return True
    return False


def is_mobile(mobile):
    if len(mobile) == 10:
        return str(mobile).isdigit()
    return False


def validate_data(data):
    """register function username, password, mobile, email"""
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")
    mobile = data.get("mobile")
    email = data.get("email")

    if name:
        name = name.strip()
    if username:
        username = username.strip()
    if password:
        password = password.strip()
    if mobile:
        mobile = mobile.strip()
    if email:
        email = email.strip()

    required_fields = [
        "name",
        "username",
        "password",
        "mobile",
    ]
    status = True
    msg = []
    for i in required_fields:
        v = data.get(i, None)
        if v is None or v.strip() == "":
            status = False
            msg.append(f"{i} is required!")

    if username and User.objects.filter(username__iexact=username).exists():
        status = False
        msg.append("Username is already taken")

    if email:
        if not is_email(email):
            status = False
            msg.append("Please make sure the email address is in correct format")
        if User.objects.filter(email__iexact=email).exists():
            status = False
            msg.append("Email address already taken")

    if mobile:
        if not is_mobile(mobile):
            status = False
            msg.append("Please make sure mobile number is 10 digits")
        if User.objects.filter(mobile__iexact=mobile).exists():
            status = False
            msg.append("Mobile number already exists")

    if password:
        st = validate_password(password)
        if not st:
            msg.append("Please enter a password with at least 6 characters")
        status = st

    return status, msg


def register_user(data):
    try:
        name = data.get("name")
        username = data.get("username")
        password = data.get("password")
        mobile = data.get("mobile")
        email = data.get("email")

        if name:
            name = name.strip()
        if username:
            username = username.strip()
        if password:
            password = password.strip()
        if mobile:
            mobile = mobile.strip()
        if email:
            email = email.strip()

        user = User(
            name=name,
            username=username,
            email=email,
            mobile=mobile,
        )
        user.save()
        user.set_password(password)
        user.save()
        return user

    except Exception as e:
        return None


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def generate_otp(mobile):
    otp = "".join(str(r.randint(1, 9)) for _ in range(4))
    otp = int(otp)
    if Otp.objects.filter(mobile=mobile).exists():
        instance = Otp.objects.filter(mobile=mobile).last()
        instance.otp = otp
    else:
        instance = Otp(mobile=mobile, otp=otp)
    instance.save()
    return otp


def send_sms(mobile):
    otp = generate_otp(mobile)
    send_otp_email(mobile, otp)


def send_otp_email(mobile, otp):
    user = User.objects.get(mobile=mobile)
    if user.email and user.email.strip() != "":
        send_mail(
            subject="OTP TO LOGIN",
            message=f"Hi {user.username}, Please enter the otp {otp} to login ",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


def send_reset_password_email(email, link):
    send_mail(
        subject="LINK TO RESET PASSWORD",
        message=f"Hi,\nPlease use the following link to regenerate the password:\n{link}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
