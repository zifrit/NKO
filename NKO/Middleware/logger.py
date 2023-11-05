class TestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # print(request.method)
        # print(request.path)
        # print(request.GET)  # Параметры GET
        # print(request.POST)  # Параметры POST
        # print(request.headers)
        # print(request.user)
        # print(request.body)
        # print(response.content)
        # if request.method == "POST":

        # Если данные в формате JSON
        if request.content_type == "application/json":
            import json
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                print("JSON данные:", json_data)
            except json.JSONDecodeError as e:
                print("Ошибка JSON декодирования:", str(e))
        response = self.get_response(request)

        return response
