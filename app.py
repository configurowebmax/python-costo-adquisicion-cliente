"""
=====================================================================
 Costo de Adquisición de Cliente (CAC)
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_costo_adquisicion_cliente_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Costo de Adquisición de Cliente (CAC)."""

    def __init__(self, inversion, clientes):
        self.inversion = float(inversion)
        self.clientes = float(clientes)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        if self.clientes == 0:
            return {"error": "Debe haber al menos 1 cliente."}
        cac = self.inversion / self.clientes
        return {"cac": cac}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["cac"] > 50000:
            return "⚠️ CAC alto. Optimiza tus campañas de marketing."
        return "✅ CAC razonable."



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("inversion"), input_float("clientes"))
    r = c.calcular()
    if "error" in r:
        mostrar(f'❌ {r["error"]}', clase="is-error"); return
    html = f"""
      <div class="result-value">🎯 CAC: {fmt_moneda(r["cac"])}</div>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "inversion": input_float("inversion"),
            "clientes": input_float("clientes"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "inversion" in datos:
            document.querySelector("#inversion").value = datos["inversion"]
        if "clientes" in datos:
            document.querySelector("#clientes").value = datos["clientes"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
