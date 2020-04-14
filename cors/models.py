from django.http import HttpResponse

class CORS(HttpResponse):

    def allow_all(self, auth = ""):
        self["Access-Control-Allow-Origin"] = "*"
        self["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        self["Access-Control-Max-Age"] = "1000"
        self["Access-Control-Allow-Headers"] = "*"
        self["Authorization"] = "Token-" + auth
        self["Content-Type"] = "application/json"


        return self