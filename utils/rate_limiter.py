from rest_framework.throttling import UserRateThrottle


class UserLoginLimiter(UserRateThrottle):
    """
    This class is to limit the rate at which users call the login endpoint
    in order to prevent brute force attack 
    """
    rate = '100/day'
