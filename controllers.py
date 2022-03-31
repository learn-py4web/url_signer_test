"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', auth, url_signer)
def index():
    print("User:", get_user_email())
    return dict(url_signer=url_signer)

@action('other')
@action.uses('other.html', url_signer.verify())
def other():
    return dict()

@action('somepath')
@action.uses(url_signer)
def somepath():
   # This controller signs a URL.
   signed_url = URL('anotherpath', signer=url_signer)
   print("Signed URL:", type(signed_url), signed_url)
   return (
        "<html><body><br><h4>Go to a signed url</h4><br><br>"
        + '<a class="button" href="%s">Go</a><br><br>'
        + '<form><button type="submit" formaction="%s">T R Y</button></form>'
        + "</body></html>"
    ) % (signed_url, signed_url)

@action('anotherpath')
@action.uses(url_signer.verify())
def anotherpath():
   # The signature has been verified.
   return ("<html><body><br><h3>This is ANOTHERPATH !!</h3></body></html>")