from microsoft_auth.backends import MicrosoftAuthenticationBackend

class CustomMicrosoftBackend(MicrosoftAuthenticationBackend):
    def get_or_create_user(self, token, claims):
        user, created = super().get_or_create_user(token, claims)

        email_domain = user.email.split('@')[-1]
        if email_domain != 'ramo.com.co':
            user.is_active = False
            user.save()

        return user, created
