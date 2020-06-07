# ridelectric.pl
> It's Website present Photovoltaic installation Offers and e-store with electromobility 
> and photovoltaics components.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Instruction](#Instructions)
* [CodeExamples](#CodeExamples)
* [Features](#features)
* [Status](#status)
* [Contact](#contact)

## General info
Project presents Website with description  of why it's worth to have photovoltaic installation and kind
 of installations. Also Internet store with products of photovoltaic and electromobility parts

## Technologies
* Python - version 3.8
* Python Django - version 3.0.6
* HTML/CSS 
* JavaScript 

## Instructions
#### Tab home contains carousel with link to "Photovoltaic installation", e-store and contact tabs.
#### Tab About short discription of company, e-shop and photowoltaic installation offer
#### Tab "Photovoltaic installation" more precise discription of offer, like type of installation
#### Tab Shop is temperarily closed because of pandemic(comming soon)
#### Tab Contact contains simple contact form using database, with obligatory Firstname form, Email
#### and Question form. Forms Surname and Company are optional.The contact form contains options
####  for sending copy of the form to the email adress. Also contains contact details

## Code Examples
##### 'if confirmation == 'on':                         # if checkbox confirmation checked on/off def... variable send
#####    send            = 'Kopia formularza kontaktowego została wysłana na adres e-mail: {}'.format(email)
#####    subject         = 'Formularz kontaktowy ridelectric.pl - kopia'                      # subject of email
#####    message         = 'Dziękujemy za skorzystanie z Formularza Kontaktowego ridelectric.pl'       # reserve messego
#####    from_email      = settings.EMAIL_HOST_USER                      # adres from send and details from settings
#####    recipient_list  = email                                         # delivery email
#####    html_message    = loader.render_to_string('emailsend.html',
#####                                                {
#####                                                     'name': name.capitalize(),
#####                                                     'surname': surname.capitalize(),
#####                                                     'question': question
#####                                                }
#####                                                )     # render body from html(templates)
#####    send_mail(subject, message, from_email, [recipient_list], fail_silently=True, auth_user=None,
#####                auth_password=None, html_message=html_message      # send_mail function
#####                )
##### else:
#####      send = ''
#####    confirmation_text = 'Dziękujemy {} {} za skorzystanie z Formularza Kontaktowego!'.format(name.capitalize(),
#####                                                                                 surname.capitalize()
#####                                                                                 )`

## Features
List of features ready and TODOs for future development
* contact

## Status
Project is: _in progress

## Contact
Created by [DiddyChriss] (http://chriss.pythonanywhere.com/) - feel free to contact me!
