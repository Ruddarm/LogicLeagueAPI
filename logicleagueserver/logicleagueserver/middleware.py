from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken


class PrintRequestHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.authenticator = JWTAuthentication()
        
    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        if token:
            try:
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
                # Validate token using the JWTAuthenticator
                # JWTAuthentication will validate the token and set the user
                user,_ = self.authenticator.authenticate(request)
                request.user = user  # Attach user to request
            except AuthenticationFailed as e:
                print("err")
                response = self.get_response(request)
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")
                return response

        response = self.get_response(request)
        return response
