import random


class Participante:
    def __init__(self, nombre, pais) -> None:
        self.nombre = nombre
        self.pais = pais

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Participante):
            return self.nombre == other.nombre and self.pais == other.pais
        return False

    def __hash__(self) -> int:
        return hash((self.nombre, self.pais))


class Olimpiadas:
    def __init__(self) -> None:
        self.eventos = []
        self.participantes = {}
        self.resultados_evento = {}
        self.resultados_pais = {}

    def registar_evento(self):
        evento = input("Nombre del evento: ").strip()
        if evento in self.eventos:
            print(f"El evento '{evento}' ya existe. No se puede duplicar.")
        else:
            self.eventos.append(evento)
            print(f"Evento {evento} ha sido registrado.")

    def registrar_participante(self):
        if not self.eventos:
            print("No hay eventos registrados. Registra un evento primero.")
            return
        nombre = input("Nombre del participante: ").strip()
        pais = input("País del participante: ").strip()
        participante = Participante(nombre, pais)

        print("Selecciona un ev2ento para registrar al participante:")
        for i, evento in enumerate(self.eventos, start=1):
            print(f"{i}. {evento}")

        evento_seleccionado = int(input("Número del evento: ")) - 1

        if evento_seleccionado < 0 or evento_seleccionado >= len(self.eventos):
            print("Evento no válido. Intente de nuevo.")
            return
        else:
            evento = self.eventos[evento_seleccionado]

            if (
                evento in self.participantes
                and participante in self.participantes[evento]
            ):
                print(
                    f"El participante {nombre} de {pais} ya está registrado en el evento {evento}."
                )
                return
            else:
                if evento not in self.participantes:
                    self.participantes[evento] = []
                self.participantes[evento].append(participante)
                print(
                    f"El participante {nombre} de {pais} ha sido registrado en el evento {evento}."
                )

    def simular_eventos(self):
        if not self.eventos:
            print("No hay eventos registrados. Registra un evento primero.")
            return
        for evento in self.eventos:
            if len(self.participantes[evento]) < 3:
                print(
                    f"No hay suficientes participantes para el evento {evento}. Se requieren al menos 3."
                )
                continue
            ganadores = random.sample(self.participantes[evento], 3)
            random.shuffle(ganadores)
            oro = ganadores[0]
            plata = ganadores[1]
            bronce = ganadores[2]
            self.resultados_evento[evento] = [oro, plata, bronce]

            self.actualizar_resultados_pais(oro.pais, "oro")
            self.actualizar_resultados_pais(plata.pais, "plata")
            self.actualizar_resultados_pais(bronce.pais, "bronce")

            print(f"Oro: {oro.nombre} de {oro.pais}")
            print(f"Plata: {plata.nombre} de {plata.pais}")
            print(f"Bronce: {bronce.nombre} de {bronce.pais}")

    def actualizar_resultados_pais(self, pais, medalla):
        if pais not in self.resultados_pais:
            self.resultados_pais[pais] = {"oro": 0, "plata": 0, "bronce": 0}
        self.resultados_pais[pais][medalla] = +1

    def mostrar_reporte(self):
        if not self.resultados_evento:
            print("No hay resultados de eventos registrados.")

        else:
            print("Resultados de los eventos: ")
            for evento, ganadores in self.resultados_evento.items():
                print(f"Resultados de {evento}:")
                print(f"Oro: {ganadores[0].nombre} de {ganadores[0].pais}")
                print(f"Plata: {ganadores[1].nombre} de {ganadores[1].pais}")
                print(f"Bronce: {ganadores[2].nombre} de {ganadores[2].pais}")

        if self.resultados_pais:
            print("\nResultados por país:")
            sort_paises = sorted(
                self.resultados_pais.items(),
                key=lambda x: (x[1]["oro"], x[1]["plata"], x[1]["bronce"]),
                reverse=True,
            )
            print("\nResultados por país:")
            for pais, medallas in sort_paises:
                print(
                    f"{pais}: {medallas['oro']} oros, {medallas['plata']} platas, {medallas['bronce']} bronces"
                )
        else:
            print("No hay resultados por país registrados.")


olimpiadas = Olimpiadas()

print("Bienvenido a las olimpiadas")

while True:
    print()
    print("Elige una opción:")
    print("1. Crear evento")
    print("2. Registro de participantes")
    print("3. Simulacion de eventos")
    print("4. Creacion de informes")
    print("5. Salir")
    opcion = int(input("Seleccione una opción: "))

    match opcion:
        case 1:
            print("Crear evento")
            olimpiadas.registar_evento()
        case 2:
            print("Registro de participantes")
            olimpiadas.registrar_participante()
        case 3:
            print("Simulacion de eventos")
            olimpiadas.simular_eventos()
        case 4:
            print("Creacion de informes")
            olimpiadas.mostrar_reporte()
        case 5:
            print("Saliendo...")
            break
        case _:
            print("Opción no válida. Intente de nuevo con una opción válida.")
