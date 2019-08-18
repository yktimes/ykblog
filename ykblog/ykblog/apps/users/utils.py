
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'user_name': user.username,
        'user_avatar':user.avatar,
        'permissions':user.is_staff
    }