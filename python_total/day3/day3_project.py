text = input("Ingresa un texto a analizar: ")
text_lower = text.lower()

letra1 = input("Ahora ingresa 3 letras. Ingresa la primera: ")
letra2 = input("Ingresa la segunda: ")
letra3 = input("Ingresa la tercera: ")


letra1_lower = letra1.lower()
letra2_lower = letra2.lower()
letra3_lower = letra3.lower()

print(
    f"La primer letra '{letra1}' aparece {text_lower.count(letra1_lower)} veces en el texto"
)
print(
    f"La segunda letra '{letra2}' aparece {text_lower.count(letra2_lower)} veces en el texto"
)
print(
    f"La tercer letra '{letra3}' aparece {text_lower.count(letra3_lower)} veces en el texto"
)


total_palabras = len(text.split())

print(f"Hay un total de {total_palabras} palabras en el texto.")

print(f"La primer letra del texto es '{text[0]}' y la ultima es '{text[-1]}'.")

lista_palabras = text.split()
lista_palabras = lista_palabras[::-1]
orden_inverso = " ".join(lista_palabras)
print(f"Las palabras en orden inverso son: '{orden_inverso}'.")

python_in_text = "Python".lower() in text_lower

python_dict = {True: "Si", False: "No"}

print(f"Aparece la palabra 'Python' en el texto? --> {python_dict[python_in_text]}")
