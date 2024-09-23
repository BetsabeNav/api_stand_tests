import  sender_stand_request
import data
from data import user_body


# esta función cambia los valores en el parámetro "firstName"
def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body


## Función de prueba positiva
def positive_assert(first_name):
    user_body = get_user_body(first_name)  # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_response = sender_stand_request.post_new_user(user_body) # El resultado de la solicitud para crear un/a nuevo/a usuario/a se guarda en la variable user_response

    assert user_response.status_code == 201 # Comprueba si el código de estado es 201
    assert user_response.json()["authToken"] != ""  # Comprueba que el campo authToken está en la respuesta y contiene un valor

    users_table_response = sender_stand_request.get_users_table()  # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"] # String que debe estar en el cuerpo de respuesta

    assert users_table_response.text.count(str_user) == 1 # Comprueba si el usuario o usuaria existe y es único/a

def negative_assert_symbol(first_name): # Función de prueba negativa
    user_body = get_user_body(first_name)  # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    response = sender_stand_request.post_new_user(user_body) # Comprueba si la variable "response" almacena el resultado de la solicitud.

    assert response.status_code == 400 # Comprueba si la respuesta contiene el código 400.
    assert response.json()["code"] == 400 # Comprueba si el atributo "code" en el cuerpo de respuesta es 400.
    assert response.json()["message"] == "El nombre que ingresaste es incorrecto. " \
                                         "Los nombres solo pueden contener caracteres latinos,  "\
                                         "los nombres deben tener al menos 2 caracteres y no más de 15 caracteres" # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400  # Comprueba si la respuesta contiene el código 400.
    assert response.json()["code"] == 400  # Comprueba si el atributo "code" en el cuerpo de respuesta es 400.
    assert response.json()["message"] == "No se enviaron todos los parámetros necesarios"


# Prueba 1. Creación de un nuevo usuario o usuaria: El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Prueba 2. Creación de un nuevo usuario o usuaria: El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Prueba 3. Error: El parámetro "firstName" contiene un carácter
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Prueba 4. Error: El parámetro "firstName" contiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")

# Prueba 5. Error: El parámetro "firstName" contiene palabras con espacios
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")

# Prueba 6. Error: El parámetro "firstName" contiene un string de caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

# Test 7. Error: El parámetro "firstName" contiene un string de números
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Prueba 8. Error: La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy() # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body",
                                      # De lo contrario, se podrían perder los datos del diccionario de origen
    user_body.pop("firstName") # El parámetro "firstName" se elimina de la solicitud
    negative_assert_no_first_name(user_body) # Comprueba la respuesta


# Prueba 9. Error: El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")  # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    negative_assert_no_first_name(user_body) # Comprueba la respuesta

# Prueba 10. Error: El tipo del parámetro "firstName" es un número
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12) # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    response = sender_stand_request.post_new_user(user_body) # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    assert response.status_code == 400 # Comprobar el código de estado de la respuesta








