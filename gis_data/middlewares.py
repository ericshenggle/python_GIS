from django.utils.deprecation import MiddlewareMixin


class CorsMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "GET" or request.method == "POST":
            return

    def process_response(self, request, response):
        if request.method == "GET":
            # 不能加*
            response["Access-Control-Allow-Headers"] = "XMLHttpRequest"
        response["Access-Control-Allow-Origin"] = "http://localhost:8080"
        return response
