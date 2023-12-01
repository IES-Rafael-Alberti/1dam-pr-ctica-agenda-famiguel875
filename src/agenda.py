"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Función que limpia la consola cuando es invocada
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list):
    """ Función que carga los contactos iniciales de la agenda desde un fichero, en primer lugar a cada línea del fichero 
        se le eliminan sus espacios vacíos con el método strip() y se separan en partes teniendo en cuenta el carácter ';' 
        en cuatro campos (nombre, apellido, email y telefonos), después procesamos los cada uno de estos campos utilizando 
        el el método strip() y el método title para que puedan ser agregados correctamente a la lista 'contactos' mediante 
        el método append()
        :param contactos: lista de todos contactos
        :type contactos: list 
        :return: nueva lista de contactos con la adición de los contactos del fichero o FileNotFoundError, 
        excepcion creada si no se encuentra el archivo de contactos o sea crea una excepcion como si se produce 
        un error al cargar los archivos del fichero.
    ...
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...

    try:
        with open(RUTA_FICHERO, 'r') as fichero:
            for linea in fichero:
                # Dividir la línea en campos utilizando el punto y coma como separador
                campos = linea.strip().split(';')

                # Procesar los campos para construir el diccionario del contacto
                nombre = campos[0].strip().title()
                apellido = campos[1].strip().title()
                email = campos[2].strip()
                telefonos = [telefono.strip() for telefono in campos[3:] if telefono.strip()]

                # Agregar el contacto a la lista
                nuevo_contacto = {'nombre': nombre, 'apellido': apellido, 'email': email, 'telefonos': telefonos}
                contactos.append(nuevo_contacto)

        print("Contactos cargados correctamente.")
    except FileNotFoundError:
        print("El archivo de contactos no existe.")
    except Exception as e:
        print(f"Error al cargar contactos: {e}")


def buscar_contacto(contactos: list, email: str):
    """ Busca la posición de un contacto con un email determinado
        :param contactos: lista de todos contactos
        :type contactos: list 
        :param email: parámetro email referente a un contacto de la lista
        :type email: str
        :return: retorna el iterable del contacto cuyo email es el solicitado 
        en la lista de contacto enumerada o no retorna nada si el email introducido no coincide con ninguno de la lista contactos.
    ...
    """
    for i, contacto in enumerate(contactos):
        if contacto['email'] == email:
            return i
    return None


def modificar_contacto(contactos: list, email: str):
    """ Modifica un contacto de la agenda utilizando el iterable retornado de buscar_contacto() como posición para poder actualizar 
        los datos del contacto que queramos modificar
        :param contactos: lista de todos contactos
        :type contactos: list 
        :param email: parámetro email referente a un contacto de la lista
        :type email: str
        :return: retorna el contacto con los nuevos datos o un mensaje de salida indicando que no se ha encontrado el contacto 
        (si pos es igual a None), también puede retornar una excepción indicando que no se ha modificado ningún contacto.
    ...
    """
    try:
        pos = buscar_contacto(contactos, email)
        if pos != None:
            print("Contacto encontrado. Proporcione los nuevos datos:")
            nuevo_contacto = pedir_datos_contacto()
            contactos[pos] = nuevo_contacto
            print("Contacto modificado correctamente.")
        else:
            print("No se encontró el contacto para modificar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se modificó ningún contacto")


def eliminar_contacto(contactos: list, email: str):
    """ Elimina un contacto de la agenda utilizando el iterable retornado de buscar_contacto() como posición para poder encontrar 
        los datos del contacto que queramos eliminar, sabiendo la posición se utiliza 'del' para poder eliminar el contacto asociado
        :param contactos: lista de todos contactos
        :type contactos: list 
        :param email: parámetro email referente a un contacto de la lista
        :type email: str
        :return: retorna un mensaje de salida indicando la que se ha eliminado el contacto con existo o un mensaje de salida 
        indicando que no se ha encontrado el contacto (si pos es igual a None), también puede retornar una excepción indicando que no se ha modificado ningún contacto.
    ...
    """
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado
        pos = buscar_contacto(contactos, email)
        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")


def mostrar_menu():
    """ Muestra el menú de la agenda
    ...
    """
    print("""
    AGENDA
    ------
    1. Nuevo contacto
    2. Modificar contacto
    3. Eliminar contacto
    4. Vaciar agenda
    5. Cargar agenda inicial
    6. Mostrar contactos por criterio
    7. Mostrar la agenda completa
    8. Salir
    """)

def pedir_opcion():
    """ Pide al usuario que seleccione una opción del menú, mediante un bucle pide al usuario que introduzca 
        una opción que sea un número, además de que se encuentre dentro del conjunto 'OPCIONES_MENU'
        :return: Devuelve la opción numérica del conjunto seleccionada.
    ...
    """
    opcion = input("Seleccione una opción: ")
    while not opcion.isdigit() or int(opcion) not in OPCIONES_MENU:
        print("Opción no válida. Intente nuevamente.")
        opcion = input("Seleccione una opción: ")
    return int(opcion)


def pedir_email(contactos: list) -> str:
    """ Función en la que se introduce el parámetro email, y se devuelve la cadena.
        :param contactos: lista de todos contactos
        :type contactos: list 
        :return: La cadena email o un ValueError.
    ...
    """
    while True:
        email = input("Email: ").strip()

        try:
            validar_email(email, contactos)
            return email
        except ValueError as e:
            print(f"Error: {e}")


def validar_email(email: str) -> bool:
    """ Función que valida el parámetro email introducido y se asegura que cumpla las condiciones de este parámetro.
        :param email: parámetro email referente a un contacto de la lista
        :type email: str
        :return: False si el email es una cadena vacía o no incluye el símbolo '@' o '.' dentro de la cadena, True si 
        no se encuentra en ninguno de estos casos.
    ...
    """
    if not email:
        raise ValueError("El email no puede ser una cadena vacía")

    elif '@' not in email or '.' not in email:
        raise ValueError("El email no es un correo válido")
    
    else:
        return True


def validar_telefono(telefono: str) -> bool:
    """ Función que comprueba telefono, si este no tiene un prefijo o tiene un prefijo '+34' o '+34-' y si es una 
        cadena númerica de nueve digitos
        :param telefono: parámetro telefono referente a un contacto de la lista
        :type telefono: str
        :return: True si telefono cumple los requisitos, False en caso contrario.
    ...
    """
    if telefono.isdigit() and len(telefono) == 9:
        return True

    elif telefono[:3] == '+34':
        if len(telefono[3:]) == 9 and telefono[3:].isdigit():
            return True
        else:
            return False
    
    elif telefono[:4] == '+34-':
        if len(telefono[4:]) == 9 and telefono[4:].isdigit():
            return True
        else:
            return False

    else:
        return False


def agregar_contacto(contactos: list):
    """ Agrega un nuevo contacto a la agenda
        :param contactos: lista de todos contactos
        :type contactos: list 
    ...
    """
    nuevo_contacto = pedir_datos_contacto()
    contactos.append(nuevo_contacto)


def pedir_datos_contacto():
    """ Pide al usuario los datos para un nuevo contacto
    ...
    """
    nombre = input("Nombre: ").strip().title()
    apellido = input("Apellido: ").strip().title()
    email = input("Email: ")
    while not validar_email(email):
        print("Email no válido. Intente nuevamente.")
        email = input("Email: ")

    telefonos = []
    telefono = input("Teléfono (deje en blanco para terminar): ").strip().replace(" ", "")
    while telefono:
        while not validar_telefono(telefono):
            print("Teléfono no válido. Intente nuevamente.")
            telefono = input("Teléfono: ").strip().replace(" ", "")
        telefonos.append(telefono)
        telefono = input("Teléfono (deje en blanco para terminar): ").strip().replace(" ", "")

    return {'nombre': nombre, 'apellido': apellido, 'email': email, 'telefonos': telefonos}


def mostrar_contactos(contactos: list):
    """ Muestra todos los contactos de la agenda, primero se ordena la lista de contactos por nombre antes de mostrarlos,
        luego se muestra la cantidad de contactos ordenados, finalmente puede mostrar cada contacto con el formato requerido
        o mostrar un mensaje indicando que la agenda está vacía.
        :param contactos: lista de todos contactos
        :type contactos: list 
    ...
    """
    contactos_ordenados = sorted(contactos, key=lambda x: x['nombre'])

    print(f"AGENDA ({len(contactos_ordenados)})")
    print("------")

    for contacto in contactos_ordenados:
        print(f"Nombre: {contacto['nombre']} {contacto['apellido']} ({contacto['email']})")
        telefonos = " / ".join(contacto['telefonos']) if contacto['telefonos'] else "ninguno"
        print(f"Teléfonos: {telefonos}")
        print("......")

    if not contactos_ordenados:
        print("La agenda está vacía.")


def mostrar_contactos_por_criterio(contactos: list, criterio: str, valor: str):
    """ Muestra los contactos de la agenda que coinciden con un criterio específico
        :param contactos: lista de todos contactos
        :type contactos: list 
        :param criterio: nombre, apellido, email o telefono del contacto, escogido por el usuario para filtrar entre los contactos
        :type criterio: str
        :param valor: número/s o carácter/es introducidos por usario usado para buscar coincidencias con el criterio escogido por este
        :type valor: str
    ...
    """
    contactos_coincidentes = []

    for contacto in contactos:
        if criterio.lower() == 'nombre' and valor.lower() in contacto['nombre']:
            contactos_coincidentes.append(contacto)
        elif criterio.lower() == 'apellido' and valor.lower() in contacto['apellido']:
            contactos_coincidentes.append(contacto)
        elif criterio.lower() == 'email' and valor.lower() in contacto['email']:
            contactos_coincidentes.append(contacto)
        elif criterio.lower() == 'telefono' and any(valor in telefono for telefono in contacto['telefonos']):
            contactos_coincidentes.append(contacto)

    if contactos_coincidentes:
        print(f"Contactos que coinciden con el criterio '{criterio}':")
        mostrar_contactos(contactos_coincidentes)
    else:
        print(f"No se encontraron contactos que coincidan con el criterio '{criterio} {valor}'.")


def vaciar_agenda(contactos: list):
    """ Vacia la lista de contactos de la agenda usando el método .clear()
        :param contactos: lista de todos contactos
        :type contactos: list 
    ...
    """
    confirmacion = input("¿Está seguro de que desea vaciar la agenda? (S/N): ").strip().lower()
    if confirmacion == 's':
        contactos.clear()
        print("Agenda vaciada correctamente.")
    else:
        print("Operación cancelada.")


def cargar_agenda_inicial(contactos: list):
    """ Carga la agenda con contactos iniciales desde un archivo, primero se limpia la lista actual de contactos 
        con el método .clear() antes de cargar los nuevos, después de realiza un bucle for para cargar poder cargar los contactos 
        originales del archivo 
        :param contactos: lista de todos contactos
        :type contactos: list 
    ...
    """
    confirmacion = input("¿Está seguro de que desea cargar la agenda inicial? (S/N): ").strip().lower()
    if confirmacion == 's':
        try:
            with open(RUTA_FICHERO, 'r') as fichero:

                contactos.clear()

                for linea in fichero:
                    datos_contacto = linea.strip().split(';')  
                    
                    if len(datos_contacto) >= 3: 
                        nuevo_contacto = {
                            'nombre': datos_contacto[0],
                            'apellido': datos_contacto[1],
                            'email': datos_contacto[2],
                            'telefonos': datos_contacto[3:]
                        }
                        contactos.append(nuevo_contacto)
                    else:
                        print(f"Advertencia: La línea '{linea.strip()}' no tiene suficientes campos y será ignorada.")

            print("Agenda inicial cargada correctamente.")
        except FileNotFoundError:
            print("El archivo de contactos no existe.")
        except Exception as e:
            print(f"Error al cargar la agenda inicial: {e}")
    else:
        print("Operación cancelada.")


def agenda(contactos: list):
    """ Ejecuta el menú de la agenda con las opciones incluidas en el conjunto
        :param contactos: lista de todos contactos
        :type contactos: list 
    ...
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada...

    salir_de_agenda = False
    while salir_de_agenda == False:
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 6
        if opcion in OPCIONES_MENU:
            #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
            # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
            # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
            # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
            #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
            # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
            # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
            # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
            # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
            # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
            #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
            if opcion == 1:
                agregar_contacto(contactos)
            elif opcion == 2:
                email_a_modificar = input("Ingrese el email del contacto a modificar: ")
                modificar_contacto(contactos, email_a_modificar)
            #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
            elif opcion == 3:
                email_a_eliminar = input("Ingrese el email del contacto a eliminar: ")
                eliminar_contacto(contactos, email_a_eliminar)
            elif opcion == 4:
                vaciar_agenda(contactos)
            elif opcion == 5:
                cargar_agenda_inicial(contactos)
            elif opcion == 6:
                criterio = input("Ingrese el criterio de búsqueda (nombre, apellido, email o telefono): ").strip().lower()
                valor = input("Ingrese el valor a buscar: ").strip()
                mostrar_contactos_por_criterio(contactos, criterio, valor)
            #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
            # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
            #
            # AGENDA (6)
            # ------
            # Nombre: Antonio Amargo (aamargo@gmail.com)
            # Teléfonos: niguno
            # ......
            # Nombre: Daniela Alba (danalba@gmail.com)
            # Teléfonos: +34-600606060 / +34-670898934
            # ......
            # Nombre: Laura Iglesias (liglesias@gmail.com)
            # Teléfonos: 666777333 / 666888555 / 607889988
            # ......
            # ** resto de contactos **
            #
            #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
            elif opcion == 7:
                mostrar_contactos(contactos)
            elif opcion == 8:
                print("\n")
                print("Saliendo de la agenda . . . ")
                salir_de_agenda = True
        else:
            print("Opción no válida. Intente nuevamente.")

        pulse_tecla_para_continuar()
        borrar_consola()



def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda
    contactos = []

    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.
    cargar_contactos(contactos)

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    agenda(contactos)


if __name__ == "__main__":
    main()