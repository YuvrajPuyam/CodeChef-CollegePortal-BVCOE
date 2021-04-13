from .models import pastcontest
from ccp.settings import CLIENT_ID
from ccp.settings import CLIENT_SECRET
from ccp.settings import REDIRECTION_URL
import random 
import string
def contest_list(request):
    contests = pastcontest.objects.all()[:10]
    state = ''.join(random.choices(string.ascii_letters + string.digits, k = 16))
    return {
        "contestlb" : contests,
        "is_authenticated": request.user.is_authenticated,
        'client_id': CLIENT_ID, 
        'redirection_url': REDIRECTION_URL,
        'state': state
    }