=====
Message
=====

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "message" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'message',
    ]

2. Include the staff URLconf in your project urls.py like this::

    path('message/', include('message.urls')),

3. Run `python manage.py migrate` to create the staff models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a message (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/message/ to participate in the message.
