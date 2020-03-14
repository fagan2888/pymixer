PyMixer
=======

.. image:: https://github.com/josuebrunel/pymixer/workflows/Python%20application/badge.svg
    :target: https://github.com/josuebrunel/pymixer/workflows/Python%20application/badge.svg
.. image:: https://travis-ci.org/josuebrunel/pymixer.svg?branch=master
    :target: https://travis-ci.org/josuebrunel/pymixer
.. image:: https://coveralls.io/repos/github/josuebrunel/pymixer/badge.svg?branch=master
    :target: https://coveralls.io/github/josuebrunel/pymixer?branch=master
.. image:: http://pepy.tech/badge/pymixer
    :target: http://pepy.tech/count/pymixer


**PyMixer** is a simple api client for the Mixer ( Streaming plateforme ).

Installation
------------

.. code:: python

    pip install pymixer

Quickstart
----------


.. code:: python

   In [1]: from pymixer import Client
   In [2]: mixer = Client(my_client_id, my_client_secret, 'https://httpbin.org/get', 'myappname')

You can test the client by using the **cli** method as follow

.. code:: python

   In [3]: mixer.cli()
   In [4]: session = mixer.get_session()
   In [5]: resp = session.get('users/current')

If you want to use it in a web project, the logic will be as follow

.. code:: python
 
   from pymixer.oauth import Client
  
   @url('/request-code/')
   def request_code(request, \*args, \*\*kwargs):
      mixer = Client(my_client_id, my_client_secret, 'https://myapp.com/userinfo/', 'myappname')
      # get the authorize url 
      authorize_url = mixer.authorize_url
      return redirect(authorize_url)

   @url('/userinfo/')
   def userinfo(request):
      mixer = Client(my_client_id, my_client_secret, 'https://myapp.com/userinfo/', 'myappname')
      code = request.get('code')
      # get access data
      access_data = mixer.get_access_data(code)
      # get userinfo
      resp = mixer.get_session().get('users/current')

