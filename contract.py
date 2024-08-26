from pyteal import *

def approval_program():
    return Approve()

def clear_state_program():
    # Programa para limpiar el estado
    return Approve()

if __name__ == "__main__":
    # Compilar el contrato a TEAL
    approval_teal = compileTeal(approval_program(), mode=Mode.Application, version=2)
    clear_state_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=2)

    with open("aprobal.teal", 'w') as archivo:
        archivo.write(approval_teal)

    # Imprimir el código TEAL
    print("# Approval Program TEAL:")
    print(approval_teal)

    with open("clear.teal", 'w') as archivo:
        archivo.write(clear_state_teal)

    print("| #Clear State Program TEAL:")
    print(clear_state_teal)