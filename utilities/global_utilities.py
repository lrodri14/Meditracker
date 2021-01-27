"""
    This global_utilities.py file contains all the data storage for information that is used across several applications
    in the project as well as functions.
    Important Note:
    LOCATION_CHOICES - Holds a tuple containing a set tuples which are composed of an code and their value code. These
                       values are used across several modelForms in the application, they are used to store the current
                       location in which a user is residing.

    ORIGIN_CHOICES - Holds a tuple containing a set tuples which are composed of an code and their value code. These
                     values are used across several modelForms in the application, they are used to store the birth-
                     place of the user.

    We separated this information in two different containers, for better understanding of what information we are sto-
    ring in the form field.

    country_number_codes is a dictionary containing all the country number codes, used for validation and dynamic display
    of country codes in our form fields.

    canadian_area_codes is a list of area codes used to validate if the number stored in the db is a canadian phone
    number or an american one, also used for further correct dynamic flag icon display.
"""

from django.http.response import JsonResponse


LOCATION_CHOICES = (
    ('AR', 'Argentina'),
    ('BR', 'Brazil'),
    ('BZ', 'Belize'),
    ('CA', 'Canada'),
    ('CL', 'Chile'),
    ('CO', 'Colombia'),
    ('CR', 'Costa Rica'),
    ('GT', 'Guatemala'),
    ('HN', 'Honduras'),
    ('MX', 'Mexico'),
    ('NI', 'Nicaragua'),
    ('PA', 'Panama'),
    ('SV', 'El Salvador'),
    ('US', 'United States'),
)

ORIGIN_CHOICES = (
    ('AR', 'Argentina'),
    ('BR', 'Brazil'),
    ('BZ', 'Belize'),
    ('CA', 'Canada'),
    ('CL', 'Chile'),
    ('CO', 'Colombia'),
    ('CR', 'Costa Rica'),
    ('GT', 'Guatemala'),
    ('HN', 'Honduras'),
    ('MX', 'Mexico'),
    ('NI', 'Nicaragua'),
    ('PA', 'Panama'),
    ('SV', 'El Salvador'),
    ('US', 'United States'),
)


country_number_codes = {
    'AR': '+54',
    'BR': '+55',
    'BZ': '+501',
    'CA': '+1',
    'CL': '+56',
    'CO': '+57',
    'CR': '+506',
    'GT': '+502',
    'HN': '+504',
    'MX': '+52',
    'NI': '+505',
    'PA': '+507',
    'SV': '+503',
    'US': '+1',
}

canadian_area_codes = [
    403, 587, 780, 825, 236, 250, 604, 672, 778, 204,
    431, 506, 709, 782, 902, 226, 249, 289, 343, 365,
    416, 437, 519, 548, 613, 647, 705, 807, 905, 367,
    418, 438, 450, 514, 579, 581, 819, 873, 306, 639,
    867
]


def collect_north_american_country_code(phone_number):
    """
        DOCSTRING:
        The collect_north_american_country_code() function returns the correct country code based on a phone
        number validation, this function will check if the phone number contains a canadian area code and return the
        canadian country code, if the condition is not fulfilled, the american country code will be returned.
    """
    for area_code in canadian_area_codes:
        if str(area_code) in phone_number:
            return 'CA'.lower()
    return 'US'.lower()


def collect_country_code(phone_number, user):
    """
        DOCSTRING:
        The collect_country_code() function returns the country code based on a phone number validation, the
        function will check if the phone number contains '+1' as their first characters, if this condition is fulfilled
        the collect_north_american_country_code function will be called, if the condition is not fulfilled, an iteration
        over the country_number_codes dict keys will be perform, the country code will be returned.
    """
    try:
        if phone_number.startswith('+1'):
            return collect_north_american_country_code(phone_number)
        else:
            for key in country_number_codes.keys():
                if country_number_codes[key] in phone_number:
                    return key.lower()
                else:
                    return user.profile.location.lower()
    except AttributeError:
        return user.profile.location.lower()

# Country Code view


def collect_country_number_code(request):
    """
        DOCSTRING:
        The collect_country_number_code view is used to retrieve the country number code, the response is return in
        JSON format.
    """
    country_code = request.GET.get('country_code')
    data = {'dialling_code': country_number_codes[country_code]}
    return JsonResponse(data)

