from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from .forms import DoctorSignUpForm, AssistantSignUpForm, ProfileForm, ProfilePictureForm, ProfileBackgroundForm, ChatForm
from django.contrib.auth.models import Group
from .models import UsersProfile, ContactRequest, Chat
from utilities.accounts_utilities import set_mailing_credentials, check_requests
from django.contrib.auth import get_user_model
from meditracker.settings import TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET_KEY, TWILIO_CHAT_SERVICE_SID
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
User = get_user_model()

# Create your views here.


class Login(LoginView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context=context, request=self.request)}
        return JsonResponse(data)

    def form_valid(self, form):
        super().form_valid(form)
        data = {'success': 'Login Successful'}
        return JsonResponse(data)

    def form_invalid(self, form):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context, request=self.request)}
        return JsonResponse(data)


class Logout(LogoutView):
    pass


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:change_password_done')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        data = {'html': render_to_string(self.template_name, context=context, request=self.request)}
        return JsonResponse(data)

    def form_valid(self, form):
        super().form_valid(form)
        data = {'success': True}
        return JsonResponse(data)

    def form_invalid(self, form):
        super().form_invalid(form)
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context, self.request)}
        return JsonResponse(data)


class ChangePasswordDone(PasswordChangeDoneView):
    template_name = 'accounts/change_password_done.html'


class PasswordReset(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context, self.request)}
        return JsonResponse(data)


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context, self.request)}
        return JsonResponse(data)


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


def signup(request):
    data = {}
    account_type = request.GET.get('account_type')
    form = DoctorSignUpForm if account_type == 'doctor' else AssistantSignUpForm
    if request.method == 'POST':
        doctor = Group.objects.get(name='Doctor')
        assistant = Group.objects.get(name='Assistant')
        form = DoctorSignUpForm(request.POST) if 'speciality' in request.POST else AssistantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('speciality'):
                user.roll = 'Doctor'
                user.save()
                user.groups.add(doctor)
                set_mailing_credentials(user.email, user)
            else:
                user.roll = 'Assistant'
                user.save()
                user.groups.add(assistant)
        else:
            data['error'] = True
    context = {'form': form}
    data['html'] = render_to_string('accounts/signup.html', context, request)
    return JsonResponse(data)


def profile(request, pk=None):
    user_profile = UsersProfile.objects.get(user__pk=pk) if pk else request.user.profile
    pending_request = check_requests(user_profile.user)
    context = {'profile': user_profile, 'pending_request': pending_request}
    return render(request, 'accounts/profile.html', context)


def profile_picture_change(request):
    form = ProfilePictureForm(instance=request.user.profile)
    template = 'accounts/profile_picture_change.html'
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            context = {'profile': request.user.profile}
            data = {'success': render_to_string('accounts/partial_profile.html', context=context, request=request)}
            return JsonResponse(data)
    context = {'form': form}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def profile_background_change(request):
    form = ProfileBackgroundForm(instance=request.user.profile)
    template = 'accounts/profile_background_change.html'
    if request.method == 'POST':
        form = ProfileBackgroundForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            context = {'profile': request.user.profile}
            data = {'success': render_to_string('accounts/partial_profile.html', context=context, request=request)}
            return JsonResponse(data)
    context = {'form': form}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def profile_change(request):
    form = ProfileForm(instance=request.user.profile)
    template = 'accounts/profile_change.html'
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            context = {'profile': request.user.profile}
            data = {'success': render_to_string('accounts/partial_profile.html', context=context, request=request)}
            return JsonResponse(data)
    context = {'form': form, 'profile': request.user.profile}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def user_lookup(request):
    query = request.GET.get('query')
    close_users = User.objects.filter(Q(username__startswith=query) | Q(first_name__startswith=query) | Q(last_name__startswith=query)).order_by('first_name')
    # other_users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)).order_by('first_name')
    users = close_users
    template = 'accounts/users_lookup_results.html'
    context = {'users': users}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def contacts(request):
    query = request.GET.get('query')
    contacts_list = UsersProfile.objects.filter(Q(user__first_name__startswith=query) | Q(user__last_name__startswith=query), contacts__in=[request.user])
    template = 'accounts/contacts.html'
    context = {'contacts': contacts_list}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def remove_contact(request, pk):
    contact = User.objects.get(pk=pk)
    chat = Chat.objects.filter(participants__in=[request.user, contact])
    request.user.profile.contacts.remove(contact)
    contact.profile.contacts.remove(request.user)
    chat.delete()
    data = {'success': 'Contact removed successfully'}
    return JsonResponse(data)


def chats(request):
    chats_list = Chat.objects.filter(participants__in=[request.user])
    template = 'accounts/chats.html'
    context = {'chats': chats_list}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def display_chat(request, pk):
    identity = request.user.username
    device_id = request.GET.get('device')
    account_sid = TWILIO_ACCOUNT_SID
    api_key = TWILIO_API_KEY
    secret_key = TWILIO_API_SECRET_KEY
    chat_service_sid = TWILIO_CHAT_SERVICE_SID
    token = AccessToken(account_sid, api_key, secret_key, identity=identity)
    endpoint = "PrivateChat:{}:{}".format(identity, device_id)
    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint, service_sid=chat_service_sid)
        token.add_grant(chat_grant)
    template = 'accounts/chat.html'
    form = ChatForm
    destination = User.objects.get(pk=pk)
    channel_name = str(Chat.objects.filter(participants__in=[request.user, destination])[0])
    context = {'chat_form': form, 'destination': destination}
    data = {'html': render_to_string(template, context, request), 'identity': identity, 'channel_name': channel_name,'token': token.to_jwt().decode('utf-8')}
    return JsonResponse(data)


def contact_requests(request):
    contact_requests_list = ContactRequest.objects.filter(to_user=request.user)
    template = 'accounts/requests.html'
    context = {'contact_requests': contact_requests_list}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def send_cancel_contact_request(request, pk):
    procedure = request.GET.get('procedure')
    sender = request.user
    receiver = User.objects.get(pk=pk)
    try:
        if procedure == 'send':
            contact_request = ContactRequest(to_user=receiver, from_user=sender)
            contact_request.save()
            data = {'success': 'Request sent successfully'}
        else:
            contact_request = ContactRequest.objects.get(to_user=receiver, from_user=sender)
            contact_request.delete()
            data = {'success': 'Request cancelled successfully'}
        return JsonResponse(data)
    except IntegrityError:
        data = {'unsuccessfulSending': 'Unsuccessful request sending'}
    except ContactRequest.DoesNotExist:
        data = {'unsuccessfulCancellation': 'Request has already been accepted'}
    return JsonResponse(data)


def contact_request_response(request, pk):
    response = request.GET.get('response')
    contact_request = ContactRequest.objects.get(pk=pk)
    sender = contact_request.from_user
    receiver = request.user
    if response == 'accepted':
        receiver.profile.contacts.add(contact_request.from_user)
        sender.profile.contacts.add(request.user)
        contact_request.delete()
        private_chat = Chat.objects.create()
        private_chat.participants.add(receiver)
        private_chat.participants.add(sender)
    else:
        contact_request.delete()
    contact_requests_list = ContactRequest.objects.filter(to_user=request.user)
    template = 'accounts/requests.html'
    context = {'contact_requests': contact_requests_list}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def generate_token(request):
    pass

