"""
    This appointments_utilities.py file contains all the async and sync functions needed for the appointments app to perform
    correctly.
"""
import calendar
import requests
from twilio.rest import Client
from django.utils import timezone
from appointments.models import Consult
from twilio.base.exceptions import TwilioRestException
from meditracker.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, NUMVERIFY_API_KEY

# Twilio Client instance
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Async Functions

# Since the power of asynchronous coroutines only come in handy when you yield the control to other coroutine
# in our loop, we will create two async functions and await for one of them.


async def close_consult(delayed_consults, tz, date):
    """
        DOCSTRING:
        This async function will be responsible to close all the consults that have been delayed or where never
        attended by the doctor. It will the set the status consult to 'CLOSED'. It expects three arguments,
        'delayed_consults' expects a queryset of consults which date is than today and the medical_status is False,
        'tz' is the timezone the user is in, 'date' is the current date.
    """
    for c in delayed_consults:
        if c.datetime.astimezone(tz).date() < date.date():
            c.status = 'CLOSED'
            c.save()


async def check_delayed_consults(user):
    """
        DOCSTRING:
        This async function will be the one responsible to retrieve the delayed consults, will collect the current
        date and the collect the timezone active for this user session. It only expects one argument, 'user', is the
        current user, it is used to collect the delayed consults. This async function will await for the close_consults()
        coroutine.
    """
    today = timezone.localtime()
    tzone = timezone.get_current_timezone()
    not_attended_consults = Consult.objects.filter(created_by=user, datetime__date__lte=today.date(), status="OPEN")
    await close_consult(not_attended_consults, tzone, today)


async def validate_number(phone_number):
    """
        DOCSTRING:
        This validate_number async function is used to validate that a phone number exists in the international number-
        ing plan database, this function will make a request to the NumVerify API, if the response contains the 'valid'
        key, then the success key will be set to it's value, else, it won't be affected, the success variable will be
        returned.
    """
    success = False
    payload = {'access_key': NUMVERIFY_API_KEY, 'number': phone_number}
    response = requests.get('http://apilayer.net/api/validate', params=payload).json()
    if 'valid' in response.keys():
        success = response['valid']
    return success


async def send_sms(consult):
    """
        DOCSTRING:
        This send_sms async function is used to send SMS to any client, whenever a phone number is registered in his
        information, the function will pass control to the validate_number function and wait for a response, depending
        on the response, the message will be sent using the Twilio API.
    """
    if consult.patient.phone_number:
        response = await validate_number(consult.patient.phone_number)
        if response:
            message = consult.generate_message()
            try:
                client.messages.create(from_='+12534997932', to=consult.patient.phone_number, body=message)
            except TwilioRestException:
                pass

# Sync Functions


def collect_months_names(consults_list, tz):
    """
        DOCSTRING: This function is used to collect each of the months in which there are consults pending. It takes
        two arguments, 'consults_list' which takes a consults querySet to evalutate and extract all it's months and
        'tz' which is the current timezone in which the user resides. It will return a list of months names. We will
        make use of the calendar module and the calendar.month_name function to collect the names of the months.
    """
    months_names = []
    for c in consults_list:
        month = calendar.month_name[c.datetime.astimezone(tz).month]
        if month not in months_names:
            months_names.append(month)
    return months_names


def filter_conditional_results(user, **kwargs):
    """
        DOCSTRING:
        This filter_conditional_results() function is used to filter appointments in the All Registers page, there can be
        three different type of individual filters: 'patient', 'month' and 'year', the same way you can mix them to get
        the results expected.
    """
    cleaned_data = kwargs.pop('cleaned_data')
    patient = cleaned_data.get('patient')
    month = int(cleaned_data.get('month'))
    year = int(cleaned_data.get('year'))
    if patient == '' and month == 0 and year == 1920:
        return Consult.objects.filter(Q(patient__first_names__icontains=patient) | Q(patient__last_names__icontains=patient), datetime__date__month=month, datetime__date__year=year, created_by=user)
    elif patient != '' and month == 0 and year == 1920:
        return Consult.objects.filter(Q(patient__first_names__icontains=patient)|Q(patient__last_names__icontains=patient), created_by=user)
    elif patient == '' and month != 0 and year == 1920:
        return Consult.objects.filter(datetime__date__month=month, created_by=user)
    elif patient == '' and month == 0 and year != 1920:
        return Consult.objects.filter(datetime__date__year=year, created_by=user)
    elif patient != '' and month != 0 and year == 1920:
        return Consult.objects.filter(Q(patient__first_names__icontains=patient)|Q(patient__last_names__icontains=patient),datetime__date__month=month, created_by=user)
    elif patient != '' and month == 0 and year != 1920:
        return Consult.objects.filter(Q(patient__first_names__icontains=patient) | Q(patient__last_names__icontains=patient), datetime__date__year=year, created_by=user)
    else:
        return Consult.objects.filter(datetime__date__month=month, datetime__date__year=year, created_by=user)


# def generate_pdf(user, consult):
#     """
#         DOCSTRING:
#         This generate_pdf() is used to generate the pdf's for each consult if necessary, this function will check if there
#         are any drugs, indications or actions to be followed, if so, it will generate a pdf and save it to the consult.
#         prescription field in the model, if not it will skip this process. The process is:
#         1. Grab the context to render the PDF
#         2. Render the HTML as a string
#         3. We make use of the HTML function from WeasyPrint and pass the python file object to it, this function will
#         check what type of file we are passing and will convert it to a pdf with the write.pdf() method.
#         4. We return the file as an HttpResponse object, and to make the browser treat this response as a file attachment
#         we set the content_type argument to the type of file we want to attach, in this case = 'application/pdf'
#         5. We set the Content-Disposition header to the filename of the file we want to set.
#         6. Lastly we just create a representation of this file using the SimpleUploadedFile function that will return us
#         a file, we set the following parameters: 'name' which is the name of the file, 'content' which is the content we
#         he are passing to this function in this case the pdf and finally the content_type.
#
#     """
#     if consult.indications != '' or consult.actions != '':
#         context = {'user': user, 'consult': consult}
#         template = render_to_string('appointments/pdf.html', context)
#         pdf = HTML(string=template).write_pdf()
#         prescription = HttpResponse(pdf, content_type='application/pdf')
#         prescription['Content-Disposition'] = 'filename={}{}.pdf'.format(consult.patient, consult.datetime.date())
#         return SimpleUploadedFile(name='prescrition-{}-{}.pdf'.format(consult.patient, consult.datetime.date()), content=pdf,content_type='application/pdf')
