from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.urls import re_path, reverse
from django.contrib.auth import get_user_model
from allauth.account.views import ConfirmEmailView
from django.views.generic.base import TemplateView, TemplateResponseMixin, View
from finin_test import app_settings
from finin_test import settings
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404, JsonResponse
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .forms import SignupForm
from django.urls import get_resolver
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import response, decorators, permissions, status
from .serializers import UserCreateSerializer



class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {
            'message': 'Hello World'
        }

        return Response(content)


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
        user = get_user_model().objects.get(email=self.object.email_address.email)
        redirect_url = reverse('user', args=(user.id, ))
        return redirect(redirect_url)

User = get_user_model()
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def signup(request, *args, **kwargs):

    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()

    user.refresh_from_db()            
    user.profile.is_active = False
    token = account_activation_token.make_token(user)             
    user.profile.token = token
    # user.profile.mobile=form_detail['mobile']
    user.is_active = False           
    user.profile.save()
    
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('core/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    req_email = request.data['email']
    email = EmailMessage(
                mail_subject, message, to=[req_email]
    )
    email.content_subtype = "html"
    email.send()

    refresh = RefreshToken.for_user(user) 
    res = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return Response(res, status.HTTP_201_CREATED)

    # if request.method == "POST":
    #     form = SignupForm(request.POST)
    #     form_detail = request.POST.dict()        
    #     if form.is_valid():            
    #         user = save(request, form)
    #         user.refresh_from_db()            
    #         user.profile.is_active = False
    #         token = account_activation_token.make_token(user)             
    #         user.profile.token = token
    #         user.profile.mobile=form_detail['mobile']
    #         user.is_active = False           
    #         user.profile.save()
            
    #         current_site = get_current_site(request)
    #         mail_subject = 'Activate your account.'
    #         message = render_to_string('core/acc_active_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token': token,
    #         })
            
    #         to_email = form.cleaned_data.get('email')
    #         email = EmailMessage(
    #                     mail_subject, message, to=[to_email]
    #         )
    #         email.content_subtype = "html"
    #         email.send()
    #         context = {
    #             "message": "Please confirm your email address to complete the registration."
    #         }
    #         return render(request, 'core/send_email.html', context)
    # else:
    #     form = SignupForm()
    # return render(request, 'signup.html', {'form': form})

def save(request, form):
    username = email = form.cleaned_data.get('email')
    first_name= form.cleaned_data.get('first_name')
    last_name = form.cleaned_data.get('last_name')
    password = form.cleaned_data.get('password')
    return User.objects.create_user(username, email=email, password=password, first_name=first_name, last_name=last_name)

@login_required
def profile(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id)
    profile = Profile.objects.filter(user=user).get()    

    if not profile.email_confirmed:
        messages.success(request, f'Account is created for {profile.user}! to need to confirm your email before login')
        return redirect('login')
    
    context = {
        "profile": profile
    }
    return render(request, 'profile.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)
        profile = Profile.objects.filter(user=user).get()
        
        if(user.profile.token == profile.token):
            profile.refresh_from_db()
            profile.is_active = True
            profile.email_confirmed = True
            profile.save()
            context = {
                "message": "Thank you for your email confirmation. Now you can login your account."
            }
            return render(request, 'core/send_email.html', context)
        else:
            context = {
                "message": "access denied."
            }
            return render(request, 'core/send_email.html', context)
        
    except(TypeError, ValueError, OverflowError):
        user = None
        return HttpResponse('Activation link is invalid!')


class ConfirmEmailView(TemplateResponseMixin, View):
    
    template_name = "account/email_confirm." + app_settings.TEMPLATE_EXTENSION

    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            if app_settings.CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        get_adapter(self.request).add_message(
            self.request,
            messages.SUCCESS,
            'account/messages/email_confirmed.txt',
            {'email': confirmation.email_address.email})
        if app_settings.LOGIN_ON_EMAIL_CONFIRMATION:
            resp = self.login_on_confirm(confirmation)
            if resp is not None:
                return resp
        # Don't -- allauth doesn't touch is_active so that sys admin can
        # use it to block users et al
        #
        # user = confirmation.email_address.user
        # user.is_active = True
        # user.save()
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        return redirect(redirect_url)

    def login_on_confirm(self, confirmation):
        """
        Simply logging in the user may become a security issue. If you
        do not take proper care (e.g. don't purge used email
        confirmations), a malicious person that got hold of the link
        will be able to login over and over again and the user is
        unable to do anything about it. Even restoring their own mailbox
        security will not help, as the links will still work. For
        password reset this is different, this mechanism works only as
        long as the attacker has access to the mailbox. If they no
        longer has access they cannot issue a password request and
        intercept it. Furthermore, all places where the links are
        listed (log files, but even Google Analytics) all of a sudden
        need to be secured. Purging the email confirmation once
        confirmed changes the behavior -- users will not be able to
        repeatedly confirm (in case they forgot that they already
        clicked the mail).
        All in all, opted for storing the user that is in the process
        of signing up in the session to avoid all of the above.  This
        may not 100% work in case the user closes the browser (and the
        session gets lost), but at least we're secure.
        """
        user_pk = None
        user_pk_str = get_adapter(self.request).unstash_user(self.request)
        if user_pk_str:
            user_pk = url_str_to_user_pk(user_pk_str)
        user = confirmation.email_address.user
        if user_pk == user.pk and self.request.user.is_anonymous:
            return perform_login(self.request,
                                 user,
                                 app_settings.EmailVerificationMethod.NONE,
                                 # passed as callable, as this method
                                 # depends on the authenticated state
                                 redirect_url=self.get_redirect_url)

        return None

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        if not emailconfirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                emailconfirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                raise Http404()
        return emailconfirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["confirmation"] = self.object
        site = get_current_site(self.request)
        ctx.update({'site': site})
        return ctx

    def get_redirect_url(self):
        return get_adapter(self.request).get_email_confirmation_redirect_url(
            self.request)


def createTokenUser(request, *args, **kwargs):
    user = request.user
    refresh = RefreshToken.for_user(user)

    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return JsonResponse(data)
