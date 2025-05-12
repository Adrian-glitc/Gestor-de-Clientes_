import sys

DATABASE_PATH = 'clientes.csv'

if 'pytest' in sys.argv[0]:
    DATABASE_PATH = 'gestor/tests/clientes_test.csv'
    
