from __future__ import annotations

import typing
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.conf import settings
from django.http import HttpRequest

if typing.TYPE_CHECKING:
    from lifetracker.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, Any],
    ) -> Any:
        """
        Populates user information from social provider info.

        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Set first_name and last_name from social data
        if not user.first_name:
            if name := data.get("name", ""):
                # Try to split full name into first and last name
                parts = name.split(maxsplit=1)
                user.first_name = parts[0]
                if len(parts) > 1:
                    user.last_name = parts[1]
            elif first_name := data.get("first_name"):
                user.first_name = first_name
                if last_name := data.get("last_name"):
                    user.last_name = last_name
        
        return user
