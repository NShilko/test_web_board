def add_user_to_context(request):
    return {
        'is_user': request.user,
        'in_group_common': request.user.groups.filter(name='common').exists(),
        'in_group_admin': request.user.groups.filter(name='admin').exists(),
    }
