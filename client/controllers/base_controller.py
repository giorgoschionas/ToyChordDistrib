from cement import Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'

    @ex(help='Inserts a new song to the chord dht')
    def insert(self, song):
        print('Inside Base.cmd1()')

    @ex(help='Query a song from the network')
    def query(self):
        print('Inside query')

    @ex(help='Delete a song from the network')
    def delete(self):
        print('Inside query')
    
    @ex(help='Display the topology of the network')
    def overlay(self):
        print('I')

    @ex(help='Leave the chord network')
    def depart(self, id):
        print('K')