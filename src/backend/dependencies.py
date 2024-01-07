from auth.auth import fastapi_users

current_active_user = fastapi_users.current_user(active=True)
