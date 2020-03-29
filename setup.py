from setuptools import setup, find_packages

setup(
    name="Chatty-backend",
    version="1.0.3",
    packages=find_packages(),

    install_requires=['channels==2.2.0',
                      'channels-redis==2.4.0',
                      'Django==2.0',
                      'djangorestframework==3.8',
                      'django-cors-headers==2.2.0',
                      'psycopg2==2.7.4',
                      'gunicorn==19.7.1',
                      'django-push-notifications==1.6.1',
                      'swapper==1.1.2.post1'
                      ],

    package_data={
        '': ['*.txt', '*.rst'],
        'hello': ['*.msg'],
    },

    author="Akram",
    author_email="akram.ihab1992@gmail.com",
    description="A messaging system backend"
)
