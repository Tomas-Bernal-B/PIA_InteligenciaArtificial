import csv
from queue import Queue
import time


start_time = time.time()



def calcular_total(subtema, actividades):
    duracion_total = sum(int(fila[4]) for fila in actividades if fila[2] == subtema)
    valor_total = sum(int(fila[5]) for fila in actividades if fila[2] == subtema)
    return duracion_total, valor_total


def seleccionar_actividades(subtema, kmin, kmax, actividades):
    actividades_subtema = [fila for fila in actividades if fila[2] == subtema]
    actividades_subtema.sort(key=lambda x: int(x[5]), reverse=True)  # Ordenar actividades por valor descendente
    actividades_seleccionadas = []
    duracion_total = 0
    valor_total = 0

    cola = Queue()
    cola.put((0, 0, []))  # (duracion_actual, valor_actual, seleccion_actual)

    while not cola.empty():
        duracion_actual, valor_actual, seleccion_actual = cola.get()

        if valor_actual >= kmin and valor_actual <= kmax:
            actividades_seleccionadas = seleccion_actual
            duracion_total = duracion_actual
            valor_total = valor_actual
            break

        for i, actividad in enumerate(actividades_subtema):
            duracion = int(actividad[4])
            valor = int(actividad[5])

            if duracion_actual + duracion <= kmax and actividad[3] not in seleccion_actual:
                nueva_duracion = duracion_actual + duracion
                nueva_valor = valor_actual + valor
                nueva_seleccion = seleccion_actual + [actividad[3]]

                cola.put((nueva_duracion, nueva_valor, nueva_seleccion))

    while valor_total < kmin:
        for actividad in actividades_subtema:
            if actividad[3] not in actividades_seleccionadas:
                duracion = int(actividad[4])
                valor = int(actividad[5])

                if duracion_total + duracion <= kmax:
                    duracion_total += duracion
                    valor_total += valor
                    actividades_seleccionadas.append(actividad[3])

    return actividades_seleccionadas, duracion_total, valor_total


with open('i_3_2.csv', 'r') as archivo:
    lector_csv = csv.reader(archivo)
    datos = list(lector_csv)

subtemas = set(fila[2] for fila in datos)

puntajes_minimos = {1: 70, 2: 70, 3: 70, 4: 70, 5: 70, 6: 70, 7: 70, 8: 70}

print("\n\n---------------------IMPRESION DE SECUENCIAS ÓPTIMAS POR SUBTEMA POR BÚSQUEDA EN ANCHURA (BFS)-----------------------")

print("Instancia:", archivo.name)
print("\n----------------------------------------------------\n")

for subtema in sorted(subtemas):
    subtema_int = int(subtema)  # Convertir la clave a entero
    kmin = puntajes_minimos.get(subtema_int, 0)  # Obtener el valor mínimo
    actividades_seleccionadas, duracion_total, valor_total = seleccionar_actividades(subtema, kmin, 100, datos)

    print(f"Subtema: {subtema}")
    print(f"Actividades seleccionadas: {actividades_seleccionadas}")
    print(f"Duración total: {duracion_total}")
    print(f"Valor total de actividades: {valor_total}")
# Imprimir las actividades utilizadas para el cálculo del valor total
    print("Actividades utilizadas:")
    for actividad in actividades_seleccionadas:
        fila_actividad = [fila for fila in datos if fila[3] == actividad][0]
        print(f"ID: {actividad}, Duración: {fila_actividad[4]}, Valor: {fila_actividad[5]}")
    print("----------------------------------------------------------------\n")
    print()
end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time} segundos")


