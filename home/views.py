from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
from django.views import View

from .forms import *


class Contact_View(View):
    template_name = 'contact.html'
    def get(self,request, pk=None,  *args, **kwargs):
        contact_form = ContactForms()
        context = {
            'contact_form': contact_form,
        }
        return render(self.request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        contact_form = ContactForms(self.request.POST or None)
        if self.request.POST and contact_form.is_valid():
            confirmation = contact_form.cleaned_data.get('confirmation')
            email = contact_form.cleaned_data.get('email')
            name = contact_form.cleaned_data.get('name')
            surname = contact_form.cleaned_data.get('surname')
            question = contact_form.cleaned_data.get('question')
            if confirmation == True:
                send = 'Kopia formularza kontaktowego została wysłana na adres e-mail: {}'.format(email)

                subject = 'Formularz kontaktowy ridelectric.pl - kopia'                      # subject of email

                message = 'Dziękujemy za skorzystanie z Formularza Kontaktowego ridelectric.pl'  # reserve messego
                from_email = settings.EMAIL_HOST_USER                     # adres from send and details from settings

                recipient_list = [email, 'diddychriss@gmail.com']           # delivery email
                html_message = loader.render_to_string('emailsend.html',
                                                          {
                                                              'name': name.capitalize(),
                                                              'surname': surname.capitalize(),
                                                              'question': question
                                                          }
                                                        )     # render body from html(templates)

                send_mail(subject, message, from_email, recipient_list, fail_silently=True, auth_user=None,
                          auth_password=None, html_message=html_message      # send_mail function
                          )
            else:
                send = ''

            confirmation_text = 'Dziękujemy {} {} za skorzystanie z Formularza Kontaktowego!'.format(
                                                                                     name.capitalize(),
                                                                                     surname.capitalize()
                                                                                                    )
            contact_form.save()

        contact_form = ContactForms()
        context = {
            'contact_form': contact_form,
            'send': send,
            'confirmation_text' : confirmation_text,
        }
        return render(self.request, self.template_name, context)

def home(request):
    return render(request, 'index.html', {})    #create home view

def polityka_prywatnosci(request):
    return render(request, 'pp.html', {})

def regulamin(request):
    return render(request, 'regulamin.html', {})

