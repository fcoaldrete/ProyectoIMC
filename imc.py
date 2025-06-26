class IMC:
    """
    Clase para calcular el Índice de Masa Corporal (IMC)
    y determinar la clasificación de acuerdo con los valores estándar.
    """
    def __init__(self, nombre: str, edad: int, estatura_m: float, peso_kg: float):
        self.__nombre = nombre
        self.__edad = edad
        self.__estatura = estatura_m
        self.__peso = peso_kg
        self.__imc = self.__calcular_imc()
        self.__clasificacion = self.__clasificar()

    def __calcular_imc(self) -> float:
        return round(self.__peso / (self.__estatura ** 2), 2)

    def __clasificar(self) -> str:
        if self.__imc < 18.5:
            return "Bajo peso"
        elif self.__imc < 25:
            return "Normal"
        elif self.__imc < 30:
            return "Sobrepeso"
        elif self.__imc < 35:
            return "Obesidad grado I"
        elif self.__imc < 40:
            return "Obesidad grado II"
        else:
            return "Obesidad grado III"

    def obtener_datos(self) -> dict:
        return {
            "nombre": self.__nombre,
            "edad": self.__edad,
            "estatura": self.__estatura,
            "peso": self.__peso,
            "imc": self.__imc,
            "clasificacion": self.__clasificacion
        }

# Ejemplo de uso (comentado para pruebas manuales)
#if __name__ == "__main__":
#    persona = IMC("Juan Pérez", 30, 1.75, 72)
#   print(persona.obtener_datos())
