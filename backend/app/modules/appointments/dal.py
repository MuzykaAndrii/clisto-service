from app.db.dal import BaseDAL
from app.modules.appointments.models import Appointment


class AppointmentDAL(BaseDAL):
    model = Appointment
