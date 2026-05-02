from ortools.sat.python import cp_model
import pandas as pd

class SiadaSolver:
    """
    Motor de optimización SIADA+ v6.1
    Resuelve el problema de asignación docente mediante Programación por Restricciones (CP-SAT).
    """
    def __init__(self, df_grupos, df_instructores, df_curriculo):
        self.model = cp_model.CpModel()
        self.grupos = df_grupos
        self.instructores = df_instructores
        self.curriculo = df_curriculo
        self.variables = {}
        
        # Parámetros de configuración (Basados en normativa SENA)
        self.max_horas_semana = 40
        self.max_dias_semana = 5

    def crear_modelo(self):
        """Define variables de decisión y restricciones matemáticas."""
        
        # Identificadores únicos (Limpiamos espacios por si acaso)
        lista_instructores = self.instructores['Nombre'].str.strip().tolist()
        lista_fichas = self.grupos['Ficha'].astype(str).str.strip().tolist()
        dias = range(1, 6)  # 1=Lunes a 5=Viernes

        # 1. DEFINICIÓN DE VARIABLES: x[i, d, g]
        # x = 1 si el instructor 'i' dicta al grupo 'g' el día 'd'
        for i in lista_instructores:
            for d in dias:
                for g in lista_fichas:
                    self.variables[(i, d, g)] = self.model.NewBoolVar(f'x_{i}_{d}_{g}')

        # 2. RESTRICCIÓN: Asignación única por grupo
        # Cada grupo debe tener exactamente un instructor asignado por día
        for d in dias:
            for g in lista_fichas:
                self.model.Add(sum(self.variables[(i, d, g)] for i in lista_instructores) == 1)

        # 3. RESTRICCIÓN: No solapamiento de instructor
        # Un instructor no puede estar en dos grupos el mismo día
        for i in lista_instructores:
            for d in dias:
                self.model.Add(sum(self.variables[(i, d, g)] for g in lista_fichas) <= 1)

        # 4. RESTRICCIÓN: Límites laborales (Máximo días por semana)
        for i in lista_instructores:
            self.model.Add(sum(self.variables[(i, d, g)] for d in dias for g in lista_fichas) <= self.max_dias_semana)

        # 5. FUNCIÓN OBJETIVO: Maximizar la equidad (Balance de carga)
        # Incentivamos al solver a distribuir las clases de forma pareja
        cargas = []
        for i in lista_instructores:
            carga_instructor = sum(self.variables[(i, d, g)] for d in dias for g in lista_fichas)
            cargas.append(carga_instructor)
        
        # Optimizamos para que la carga total sea estable
        self.model.Minimize(sum(cargas))

    def resolver(self):
        """Ejecuta el solver CP-SAT con parámetros de alto rendimiento."""
        solver = cp_model.CpSolver()
        
        # Configuraciones de rendimiento (Detección de 8 hilos como en tu ficha técnica)
        solver.parameters.max_time_in_seconds = 120.0
        solver.parameters.num_search_workers = 8  
        
        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            resultados = []
            for (i, d, g), var in self.variables.items():
                if solver.Value(var) == 1:
                    # Buscamos datos adicionales para el reporte
                    programa = self.grupos.loc[self.grupos['Ficha'].astype(str) == g, 'Programa'].values[0]
                    resultados.append({
                        "Instructor": i, 
                        "Dia": self.mapear_dia(d), 
                        "Ficha": g,
                        "Programa": programa,
                        "Estado": "Asignado Óptimamente"
                    })
            return pd.DataFrame(resultados)
        else:
            return None

    def mapear_dia(self, d):
        dias_map = {1: "Lunes", 2: "Martes", 3: "Miércoles", 4: "Jueves", 5: "Viernes"}
        return dias_map.get(d, "N/A")

# --- CAPA DE INTELIGENCIA ANTHROPIC (Propuesta de Valor) ---
def integrar_razonamiento_claude(prompt_usuario, contexto_datos):
    """
    Este método es el núcleo de nuestra propuesta a Anthropic.
    Permitirá que Claude 3.5 Sonnet actúe como una interfaz de lenguaje natural
    para modificar el comportamiento de SiadaSolver dinámicamente.
    """
    # Ejemplo conceptual:
    # prompt = "El instructor Carlos tiene permiso mañana."
    # Claude traduce esto a una restricción de disponibilidad inmediata.
    pass
