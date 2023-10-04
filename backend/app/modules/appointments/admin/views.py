from starlette_admin.contrib.sqla import ModelView

from app.modules.appointments.models import Appointment


class AppointmentAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = Appointment
        icon = "fa-regular fa-envelope"
        name = "Appointment"
        label = "Appointments"
        identity = None
        converter = None

        super().__init__(model, icon, name, label, identity, converter)

    fields = [
        Appointment.id,
        Appointment.name,
        Appointment.email,
        Appointment.phone,
        Appointment.created_at,
    ]
