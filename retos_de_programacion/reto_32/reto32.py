import random

print("Batalla entre Wolverine y Deadpool \n")

wolverine_vida = int(input("Ingrese la vida de Wolverine: "))
deadpool_vida = int(input("Ingrese la vida de Deadpool: "))


class SuperHeroe:
    def __init__(self, nombre, vida, probabilidad_evitar, ataque_max):
        self.nombre = nombre
        self.vida = vida
        self.probalidad_evitar = probabilidad_evitar
        self.ataque_max = ataque_max

    def atacar(self, otro):
        if self.vida > 0:
            damage = random.randint(10, self.ataque_max)
            print(f"{self.nombre} ataca a {otro.nombre} y causa {damage} de daño.")
            return damage

    def evitar(self, otro):
        if self.vida > 0:
            evitar = random.random() < self.probalidad_evitar
            if evitar:
                print(f"{self.nombre} ha evitado el ataque de {otro.nombre}.")
            return evitar

def check_health(heroe):
    if heroe.vida <= 0:
        print(f"Vida de {heroe.nombre}: 0")
        print(f"{heroe.nombre} ha sido derrotado.")
        return True
    return False

contador_turnos = 1
# Crear instancias de los héroes
wolverine = SuperHeroe("Wolverine", wolverine_vida, 0.2, 120)
deadpool = SuperHeroe("Deadpool", deadpool_vida, 0.25, 100)

print()
# Mostrar la vida inicial de los héroes
print(f"Vida inicial de Wolverine: {wolverine.vida}")
print(f"Vida inicial de Deadpool: {deadpool.vida}")  


while True:
    regenerar = False

    print(f"\nTurno {contador_turnos}")

    #Wolverine ataca a Deadpool
    if not deadpool.evitar(wolverine) and not regenerar:
        damage = wolverine.atacar(deadpool)
        if damage == wolverine.ataque_max:
            print(f"¡{wolverine.nombre} ha hecho un ataque crítico! Deadpool debe regenerarse y no puede atacar.")
            regenerar = True
        # Restar el daño a la vida de Deadpool
        deadpool.vida -= damage
        if check_health(deadpool):
            break
    print(f"Vida de Deadpool: {deadpool.vida}")

    # Deadpool ataca a Wolverine
    if not wolverine.evitar(deadpool) and not regenerar:
        damage = deadpool.atacar(wolverine)
        if damage == deadpool.ataque_max:
            print(f"¡{deadpool.nombre} ha hecho un ataque crítico! Wolverine debe regenerarse y no puede atacar.")
            regenerar = True
        wolverine.vida -= damage
        if check_health(wolverine):
            break
    print(f"Vida de Wolverine: {wolverine.vida}")

    contador_turnos += 1
