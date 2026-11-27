# Arquitectura del Sistema — SIADA+ Evolución v6.1

**Sistema Inteligente de Asignación de Docencia y Ambientes**  
**Autor:** Alejandro Martínez Lopera (Tecnólogo ADSO)  
**Entorno Operativo:** [Hugging Face Spaces (Running)](https://huggingface.co)  

---

## 1. Diagrama Lógico de Flujo y Optimización

Representa el procesamiento interno de datos, la formulación matemática de variables binarias $x_{i,d,g} \in \{0,1\}$, las restricciones duras (`Hard Constraints`) y la proyección cognitiva con Claude.

```mermaid
flowchart TD
    subgraph Entrada["1. Capa de Entrada (Streamlit UI)"]
        A1[("GRUPOS_GLOBAL1__5.xlsx")]
        A2[("INSTRUCTORES_GLOBAL_2.xlsx")]
        A3[("AMBIENTES.xlsx")]
        A4[("CURRICULO_GLOBAL_2.xlsx")]
        P1["Parámetros: Fecha, Días (75), Topes Laborales"]
    end

    subgraph Procesamiento["2. Preprocesamiento y Contexto"]
        B1["Limpieza y Mapeo Flexible (Pandas)"]
        B2["API Nager.Date: Festivos Colombia"]
        B3["Parseo de Exclusiones por Día"]
    end

    subgraph Solver["3. Motor Matemático (OR-Tools CP-SAT)"]
        C1["Variables Binarias: x(i, d, g) ∈ {0,1}"]
        C2["Restricciones Duras: Cobertura, No Cruce, Topes, Exclusiones"]
        C3["Función Objetivo: Minimizar Desbalance (max - min)"]
        C4{"¿Solución Encontrada?"}
    end

    subgraph Salida["4. Salidas y Analítica"]
        D1["Cronograma 19 Columnas + Gráficos"]
        D2["Exportación CSV y Excel (3 Hojas)"]
        D3["Panel de Diagnóstico y Sugerencias"]
    end

    IA["5. Capa Cognitiva Claude API (v7.0): Lenguaje Natural -> Restricciones"]

    A1 & A2 & A3 & A4 --> B1
    P1 --> B2
    B1 --> B3
    B1 & B2 & B3 --> C1 --> C2 --> C3 --> C4
    IA -.->|"Ajuste Dinámico"| C2
    C4 -->|"OPTIMAL / FEASIBLE"| D1 --> D2
    C4 -->|"INFEASIBLE"| D3
```

---

## 2. Diagrama de Secuencia Operativa

Detalla la interacción cronológica entre el Coordinador Académico, la interfaz web, los servicios externos y el solucionador combinatorio de 8 hilos.

```mermaid
sequenceDiagram
    autonumber
    actor Coord as Coordinador Académico
    participant UI as Interfaz Web (Streamlit)
    participant Parser as Procesador Datos (Pandas)
    participant API as API Festivos (Nager.Date)
    participant Solver as Motor CP-SAT (OR-Tools)
    participant Claude as Capa IA Claude (v7.0)

    Coord->>UI: Carga 4 archivos Excel (.xlsx) y configura parámetros (75 días, 40h/sem)
    Coord->>UI: Clic en "Generar Horario Óptimo"
    
    UI->>Parser: Envía archivos cargados
    Parser->>Parser: Normaliza columnas, limpia NaN y parsea exclusiones
    Parser-->>UI: Retorna estructuras validadas (52 grupos, 113 instructores, 60 ambientes)

    UI->>API: GET /publicholidays/{año}/CO
    API-->>UI: Retorna fechas festivas oficiales de Colombia
    UI->>UI: Calcula conjunto de días no laborables (fines de semana + festivos)

    opt Ajuste en Lenguaje Natural (Roadmap v7.0)
        Coord->>UI: Ingresa novedad ("Instructor 082 incapacitado el lunes")
        UI->>Claude: Envía contexto y solicitud en lenguaje natural
        Claude-->>UI: Traduce novedad a restricción matemática x[i, d, g] = 0
    end

    UI->>Solver: Inicializa modelo con variables binarias x[i, d, g] ∈ {0,1}
    Solver->>Solver: Aplica restricciones duras (cobertura, no cruce, topes, exclusiones, equidad)
    Solver->>Solver: Ejecuta búsqueda paralela (8 hilos, máx. 120s)

    alt Solución OPTIMAL o FEASIBLE encontrada
        Solver-->>UI: Retorna matriz resuelta (2,600 asignaciones, 0 conflictos)
        UI->>UI: Construye tabla maestra (19 columnas) y gráficos estadísticos
        UI-->>Coord: Muestra dashboard interactivo y habilita descarga (.CSV y .XLSX 3 hojas)
    else Estado INFEASIBLE
        Solver-->>UI: Reporta imposibilidad matemática con parámetros actuales
        UI-->>Coord: Despliega panel de diagnóstico y sugerencias de ajuste
    end
```

---

## 3. Diagrama de Despliegue (Arquitectura Cloud)

Describe la infraestructura contenerizada en **Docker** desplegada en **Hugging Face Spaces** y su comunicación con APIs externas.

```mermaid
flowchart TB
    subgraph Cliente["Dispositivo del Usuario (Coordinador Académico)"]
        Browser["Navegador Web (Chrome / Edge / Firefox)"]
        ExcelLocal[("Archivos Excel Locales (.xlsx)")]
    end

    subgraph CloudHF["Nube: Hugging Face Spaces (amlsistemas/siada-evolucion2)"]
        subgraph DockerContainer["Contenedor Docker (Puerto expuesto: 7860)"]
            subgraph RuntimePython["Entorno Python 3.10+ (Linux)"]
                StreamlitServer["Servidor Web Streamlit (--server.port=7860)"]
                PandasEngine["Procesamiento en Memoria (Pandas / Openpyxl / BytesIO)"]
                ORToolsEngine["Motor Matemático Google OR-Tools (CP-SAT, 8 Hilos)"]
                AnthropicSDK["Cliente SDK Anthropic (Capa Cognitiva v7.0)"]
            end
        end
    end

    subgraph ExternalAPIs["Servicios Externos (Internet / HTTPS)"]
        GitHubRepo[("Repositorio GitHub (Control de Versiones & CI/CD)")]
        NagerAPI["API REST Nager.Date (Festivos Oficiales Colombia)"]
        ClaudeAPI["Anthropic API (Claude 3.5 / 4 - Razonamiento NLP)"]
    end

    ExcelLocal -->|"Carga HTTP (Multipart)"| Browser
    Browser <-->|"HTTPS / WebSockets (Puerto 443 -> 7860)"| StreamlitServer
    StreamlitServer <--> PandasEngine
    PandasEngine <--> ORToolsEngine
    StreamlitServer -.->|"Evolución v7.0"| AnthropicSDK
    
    GitHubRepo -.->|"Sincronización / Despliegue"| DockerContainer
    PandasEngine <-->|"REST GET / JSON"| NagerAPI
    AnthropicSDK <-.->|"HTTPS / JSON (API Key)"| ClaudeAPI
```
