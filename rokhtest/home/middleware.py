class RequestCountMiddleware(MiddlewareMixin):
    """
    یک کلاس middleware که با هر درخواست اجرا می‌شود و تعداد درخواست‌ها را به تعداد قبلی اضافه می‌کند.
    """
    def process_request(self, request):
        request.session['request_count'] = request.session.get('request_count', 0) + 1