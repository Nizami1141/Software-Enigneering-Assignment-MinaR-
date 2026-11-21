from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


@dataclass(frozen=True)
class User:
    id: str
    is_admin: bool = False

    def can_access(self, owner_id: str) -> bool:
        return self.is_admin or self.id == owner_id


USERS_BY_TOKEN = {
    "user-a-token": User("user-a"),
    "user-b-token": User("user-b"),
    "admin-token": User("admin", is_admin=True),
}

bearer_scheme = HTTPBearer(auto_error=False, scheme_name="MockToken")


def require_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if credentials is not None:
        user = USERS_BY_TOKEN.get(credentials.credentials)
        if user is not None:
            return user

    raise HTTPException(
        status_code=401,
        detail="Provide a valid token in the Authorization header.",
        headers={"WWW-Authenticate": "Bearer"},
    )


CurrentUser = Annotated[User, Depends(require_user)]
