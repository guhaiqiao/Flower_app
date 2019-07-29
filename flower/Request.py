import json


class Request:
    def __init__(self, request, method='POST', *names):
        self.method = method
        self.names = names
        self.request = request

    def load(self):
        if self.method == 'POST':
            self.form = json.loads(self.request.data)
            values = []
            for name in self.names:
                value = self.form[name]
                if value.isdigit():
                    values.append(int(value))
                else:
                    values.append(value)

            return values

        elif self.method == 'GET':
            self.args = self.request.args
            args = []
            for name in self.names:
                var = self.args.get(name)
                if var.isdigit():
                    args.append(int(var))
                else:
                    args.append(var)

            return args


if __name__ == "__main__":
    request = 11
    r = Request(request, 'p_id', 'hh00')
    print(r.method)
    print(r.names)
