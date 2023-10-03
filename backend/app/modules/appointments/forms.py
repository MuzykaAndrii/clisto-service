from fastapi import Form


class AppointmentForm:
    name_filed = Form(min_length=3, max_length=30)
    email_filed = Form(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone_filed = Form(pattern=r"^[\d\+\(\)\s]+$")
