nombre = input("Nombre?")
ventas = input("ventas?")
ventas = float(ventas)

ganancia = ventas * 13 / 100
ganancia = round(ganancia, 2)

print(f"Ok, {nombre}. Este mes ganaste ${ganancia}.")
