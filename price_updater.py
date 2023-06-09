import csv
import json
import redis
from datetime import datetime

def read_price_data():
    with open('price_data.csv') as f:
        print('price_data file found!')
        reader = csv.DictReader(f)
        data = {'stock1': {'time': [], 'price': []},
                'stock2': {'time': [], 'price': []},
                'stock3': {'time': [], 'price': []}}
        for row in reader:
            time_str = row['Time'].zfill(6)
            time_obj = datetime.strptime(time_str, '%H%M%S')
            if time_obj < datetime.strptime('090000', '%H%M%S'):
                continue
            if time_obj > datetime.strptime('095947', '%H%M%S'):
                break
            stock = row['Stock'].lower()
            price = int(row['Price'])
            data[stock]['time'].append(time_str)
            data[stock]['price'].append(price)
        return data


def update_redis(data):
    r = redis.Redis(host='localhost', port=6379)
    for stock, values in data.items():
        stock_data = r.get(stock)
        if stock_data is None:
            stock_data = {'time': [], 'price': []}
        else:
            stock_data = json.loads(stock_data)
        stock_data['time'].extend(values['time'])
        stock_data['price'].extend(values['price'])
        r.set(stock, json.dumps(stock_data))


if __name__ == '__main__':
    data = read_price_data()
    update_redis(data)
    print('Successfully updated prices')
