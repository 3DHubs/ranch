from flask import Flask, request, Response
from ranch import Address, AddressParts, InvalidAddressException
from ranch.json import JSONEncoder

PORT = 8000


app = Flask(__name__)
json = JSONEncoder()


@app.route('/address', methods=['GET', 'POST'])
def address():
    a = Address()

    if request.method == 'GET':
        data = json.encode(a.get_field_types())

    elif request.method == 'POST':
        in_address = request.get_json()
        significant = list(AddressParts.significant())
        significant += [AddressParts.postal_code, AddressParts.sorting_code]

        sorted_fields = sorted(
            in_address.items(),
            key=lambda i: significant.index(AddressParts.from_string(i[0]))
        )
        for part, value in sorted_fields:
            try:
                a.set_field(part, value)
            except InvalidAddressException as e:
                return Response(
                    json.encode({'message': str(e)}),
                    mimetype='application/json',
                    status=400
                )

        data = json.encode(a.get_field_types())

    return Response(data, mimetype='application/json')


@app.route('/')
def index():
    with open('index.html', 'r') as index_f:
        return index_f.read()


if __name__ == '__main__':
    app.run(debug=True)
