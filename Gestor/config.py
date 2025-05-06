import sys

DATABASE_PATH = 'clientes.db'

if 'pytest' in sys.argv[0]:
    DATABASE_PATH = 'gestor/tests/clientes_test.db'