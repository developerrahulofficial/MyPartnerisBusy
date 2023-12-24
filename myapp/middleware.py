from .models import Visitor

class TrackVisitorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the visitor's IP address from the request's META data
        visitor_ip = request.META.get('REMOTE_ADDR')

        # Save the visitor's IP address in the database
        if visitor_ip:
            Visitor.objects.create(ip_address=visitor_ip)

        response = self.get_response(request)
        return response
