''' 
Carter Frost
For hosting a website for Santa Cruz Map for businesses a virtual downtown shopping experience, making it easier for locals to support local businesses. 
'''

import logging

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    businesses = list()
    with open('data/Eat.txt', 'r') as file:
            businesses = [(bID, *business.split(',')) for bID, business in enumerate(file.read().split('\n'), 1)]
    businesses.pop() # last one is not a real business #TODO double check after everything is working
    return render_template('index.html',businesses=businesses)

@app.route('/static/<name>')
def resource(name) :
    '''Load a file from the static directory and return it to the browser.''' 
    with open ('static/' + name, 'rb') as f :
        return f.read()

@app.errorhandler(500)
def server_error(e):
    ''' Just that it is an error handler'''
    print("Borked",e)
    return('I done borked up.', 500)
    
if __name__ == '__main__' : 
    app.run(host='0.0.0.0', port=8080)
