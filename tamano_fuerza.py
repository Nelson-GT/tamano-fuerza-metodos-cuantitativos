# Desarrollado por: Nelson Guerrero y Juan Diego Cordero.

import math

class CalculadoraCostos:
    def __init__(self, costo_retencion, costo_fijo_contratacion, costo_var_contratacion):
        self.costo_retencion = costo_retencion
        self.costo_fijo = costo_fijo_contratacion
        self.costo_var = costo_var_contratacion

    def calcular_costo_transicion(self, trabajadores_previos, trabajadores_actuales, demanda_actual):
        """Calcula el costo de retener exceso de personal y de contratar nuevos."""
        costo_exceso = self.costo_retencion * (trabajadores_actuales - demanda_actual)
        
        costo_contratacion = 0
        if trabajadores_actuales > trabajadores_previos:
            costo_contratacion = self.costo_fijo + self.costo_var * (trabajadores_actuales - trabajadores_previos)
            
        return costo_exceso + costo_contratacion


class ModeloFuerzaTrabajo:
    def __init__(self):
        self.semanas = 0
        self.demandas = []
        self.max_demanda = 0
        self.trabajadores_iniciales = 0
        self.calculadora = None
        self.tabla_dp = {}
        self.decisiones = {}

    def ingresar_datos(self):
        print("--- CONFIGURACIÓN DEL MODELO DE FUERZA DE TRABAJO ---")
        self.semanas = int(input("\nIngrese el número total de semanas: "))
        
        print("\nIngrese la demanda mínima de trabajadores para cada semana:")
        for i in range(self.semanas):
            demanda = int(input(f"  Semana {i+1}: "))
            self.demandas.append(demanda)
            
        self.max_demanda = max(self.demandas)
        
        print("\nIngrese los costos asociados:")
        c_retencion = float(input("  Costo por trabajador excedente por semana (e.g. 300): "))
        c_fijo = float(input("  Costo fijo por contratación (e.g. 400): "))
        c_var = float(input("  Costo variable por trabajador contratado por semana (e.g. 200): "))
        
        self.trabajadores_iniciales = int(input("\nTrabajadores iniciales antes de la semana 1 (usualmente 0): "))
        
        self.calculadora = CalculadoraCostos(c_retencion, c_fijo, c_var)
        print("\nDatos registrados exitosamente.\nCalculando...\n")
        print("-" * 55)

    def resolver(self):
        self.tabla_dp[self.semanas + 1] = {x: 0 for x in range(self.max_demanda + 1)}
        
        # Recorrer hacia atrás (backward): desde la última semana hasta la primera.
        for semana in range(self.semanas, 0, -1):
            demanda_actual = self.demandas[semana - 1]
            estado_siguiente = self.tabla_dp[semana + 1]
            
            resultados_semana = {}
            decisiones_semana = {}
            
            rango_previos = range(0, self.max_demanda + 1) if semana == 1 else range(self.demandas[semana-2], self.max_demanda + 1)
            if semana == 1:
                rango_previos = [self.trabajadores_iniciales] 
                
            print(f"\n--- ETAPA {semana} (Demanda mínima (b_{semana}) = {demanda_actual}) ---")
            print("\nFórmula --> Costo Total = Costo Transición + Costo Futuro Acumulado")
            
            for prev_x in rango_previos:
                min_costo = math.inf
                mejor_decision = -1
                
                print(f"\n  Evaluando estado anterior (x_{semana-1} = {prev_x}):")
                
                for actual_x in range(demanda_actual, self.max_demanda + 1):
                    costo_etapa = self.calculadora.calcular_costo_transicion(prev_x, actual_x, demanda_actual)
                    costo_futuro = estado_siguiente[actual_x]
                    costo_total = costo_etapa + costo_futuro
                    
                    print(f"    -> Opción x_{semana} = {actual_x} | ${costo_etapa:.2f} + ${costo_futuro:.2f} = ${costo_total:.2f}")
                    
                    if costo_total < min_costo:
                        min_costo = costo_total
                        mejor_decision = actual_x
                        
                resultados_semana[prev_x] = min_costo
                decisiones_semana[prev_x] = mejor_decision
                print(f"    R = ÓPTIMO para x_{semana-1} = {prev_x}: Decidir x_{semana} = {mejor_decision} (Costo Acumulado: ${min_costo:.2f})")
                
            self.tabla_dp[semana] = resultados_semana
            self.decisiones[semana] = decisiones_semana
            print("\n" + "-" * 65)

    def mostrar_solucion_optima(self):
        print("\n--- RUTA ÓPTIMA Y RESULTADO FINAL ---")
        estado_actual = self.trabajadores_iniciales
        costo_total_minimo = self.tabla_dp[1][estado_actual]
        
        print(f"Costo Mínimo Total: ${costo_total_minimo:.2f}\n")
        print("Plan de Contratación:")
        for semana in range(1, self.semanas + 1):
            decision = self.decisiones[semana][estado_actual]
            print(f"  Semana {semana}: Necesarios {self.demandas[semana-1]} -> Mantener/contratar hasta tener {decision} trabajadores.")
            estado_actual = decision


if __name__ == "__main__":
    modelo = ModeloFuerzaTrabajo()
    modelo.ingresar_datos()
    modelo.resolver()
    modelo.mostrar_solucion_optima()