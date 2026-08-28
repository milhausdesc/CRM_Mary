import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import shutil
from io import BytesIO
import time
import threading

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(
    page_title="📊 CRM Personal con Excel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS - VERSIÓN MEJORADA CON COLORES
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .stat-label {
        color: #7f8c8d;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .badge-activo { background: #d4edda; color: #155724; }
    .badge-potencial { background: #fff3cd; color: #856404; }
    .badge-inactivo { background: #f8d7da; color: #721c24; }
    .badge-perdido { background: #e2e3e5; color: #383d41; }
    .badge-alta { background: #f8d7da; color: #721c24; }
    .badge-media { background: #fff3cd; color: #856404; }
    .badge-baja { background: #d4edda; color: #155724; }
    .badge-urgente { 
        background: #dc3545; 
        color: white;
        animation: pulse 1s infinite;
    }
    .stButton > button {
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        transition: all 0.2s;
    }
    .nota-preview {
        font-size: 0.85rem;
        color: #666;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;
        display: inline-block;
    }
    
    /* ============================================
       ESTILOS MEJORADOS PARA ALERTAS Y CITAS
       ============================================ */
    
    /* Alertas de citas próximas */
    .alerta-cita {
        background: #fff3cd !important;
        border-left: 6px solid #ffc107 !important;
        padding: 1.2rem 1.5rem !important;
        border-radius: 8px !important;
        margin: 0.8rem 0 !important;
        box-shadow: 0 2px 8px rgba(255, 193, 7, 0.3) !important;
        animation: parpadeo 1.5s infinite !important;
    }
    .alerta-cita strong {
        color: #856404 !important;
        font-size: 1.1rem !important;
    }
    .alerta-cita .cliente-nombre {
        color: #d39e00 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    .alerta-cita .cliente-empresa {
        color: #856404 !important;
        font-weight: normal !important;
    }
    .alerta-cita .fecha-cita {
        color: #856404 !important;
        font-weight: bold !important;
    }
    .alerta-cita .tiempo-restante {
        color: #dc3545 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    
    /* Citas urgentes - ROJO */
    .cita-urgente {
        background: #f8d7da !important;
        border-left: 6px solid #dc3545 !important;
        padding: 1rem 1.2rem !important;
        border-radius: 8px !important;
        margin: 0.5rem 0 !important;
        animation: pulse 1s infinite !important;
    }
    .cita-urgente strong {
        color: #721c24 !important;
        font-size: 1.1rem !important;
    }
    .cita-urgente .cliente-nombre {
        color: #721c24 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    .cita-urgente .tiempo-restante {
        color: #dc3545 !important;
        font-weight: bold !important;
    }
    
    /* Citas próximas - AMARILLO */
    .cita-proxima {
        background: #fff3cd !important;
        border-left: 6px solid #ffc107 !important;
        padding: 1rem 1.2rem !important;
        border-radius: 8px !important;
        margin: 0.5rem 0 !important;
    }
    .cita-proxima strong {
        color: #856404 !important;
        font-size: 1.1rem !important;
    }
    .cita-proxima .cliente-nombre {
        color: #d39e00 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    
    /* Citas programadas - VERDE */
    .cita-programada {
        background: #d4edda !important;
        border-left: 6px solid #28a745 !important;
        padding: 1rem 1.2rem !important;
        border-radius: 8px !important;
        margin: 0.5rem 0 !important;
    }
    .cita-programada strong {
        color: #155724 !important;
        font-size: 1.1rem !important;
    }
    .cita-programada .cliente-nombre {
        color: #155724 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    
    /* Citas atrasadas - ROJO OSCURO */
    .cita-atrasada {
        background: #f8d7da !important;
        border-left: 6px solid #c0392b !important;
        padding: 1rem 1.2rem !important;
        border-radius: 8px !important;
        margin: 0.5rem 0 !important;
    }
    .cita-atrasada strong {
        color: #721c24 !important;
        font-size: 1.1rem !important;
    }
    .cita-atrasada .cliente-nombre {
        color: #721c24 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    
    /* Alertas de colores para la lista de seguimientos */
    .seguimiento-urgente {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.3rem 0;
    }
    .seguimiento-proximo {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.3rem 0;
    }
    .seguimiento-hoy {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.3rem 0;
    }
    .seguimiento-manana {
        background: #cce5ff;
        border-left: 4px solid #007bff;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.3rem 0;
    }
    .seguimiento-normal {
        background: #e2e3e5;
        border-left: 4px solid #6c757d;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.3rem 0;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes parpadeo {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CLASE PARA MANEJAR EXCEL
# ============================================
class CRMExcel:
    def __init__(self):
        self.archivo = 'data/clientes.xlsx'
        self.asegurar_archivo()
    
    def asegurar_archivo(self):
        """Crear archivo Excel si no existe"""
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(self.archivo):
            # Columnas iniciales - SIN Valor_Estimado
            df = pd.DataFrame(columns=[
                'ID', 'Nombre', 'Empresa', 'Email', 'Teléfono', 'Celular',
                'Industria', 'Cargo', 'Estado', 'Prioridad', 'Fuente',
                'Etiquetas', 'Notas',
                'Ultimo_Contacto', 'Proximo_Seguimiento',
                'Fecha_Registro', 'Fecha_Actualizacion'
            ])
            df.to_excel(self.archivo, index=False)
            print(f"✅ Archivo {self.archivo} creado automáticamente")
    
    def leer_todos(self):
        """Leer todos los clientes - Forzar tipos de datos"""
        try:
            # Leer Excel especificando tipos de datos
            df = pd.read_excel(
                self.archivo,
                dtype={
                    'Teléfono': str,
                    'Celular': str,
                    'Email': str,
                    'ID': 'Int64'
                }
            )
            # Asegurar que las columnas de fecha sean datetime
            for col in ['Ultimo_Contacto', 'Proximo_Seguimiento', 'Fecha_Registro', 'Fecha_Actualizacion']:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            return df
        except Exception as e:
            st.error(f"Error al leer datos: {e}")
            return pd.DataFrame()
    
    def guardar_todos(self, df):
        """Guardar DataFrame en Excel"""
        try:
            # Crear backup automático
            self.crear_backup()
            
            # Asegurar que los teléfonos sean string antes de guardar
            for col in ['Teléfono', 'Celular']:
                if col in df.columns:
                    df[col] = df[col].astype(str).replace('nan', None)
            
            # Guardar
            df.to_excel(self.archivo, index=False)
            return True
        except Exception as e:
            st.error(f"Error al guardar: {e}")
            return False
    
    def crear_backup(self):
        """Crear backup del archivo"""
        if os.path.exists(self.archivo):
            backup_dir = 'backups'
            os.makedirs(backup_dir, exist_ok=True)
            
            fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f'{backup_dir}/clientes_backup_{fecha}.xlsx'
            shutil.copy2(self.archivo, backup_file)
            
            # Mantener solo últimos 10 backups
            backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.xlsx')])
            if len(backups) > 10:
                for f in backups[:-10]:
                    os.remove(os.path.join(backup_dir, f))
    
    def agregar_cliente(self, datos):
        """Agregar nuevo cliente - SIN Valor_Estimado"""
        df = self.leer_todos()
        
        # Generar ID
        if df.empty:
            nuevo_id = 1
        else:
            nuevo_id = df['ID'].max() + 1
        
        # Preparar datos - Convertir teléfonos a string
        for key in ['Teléfono', 'Celular']:
            if key in datos and datos[key] is not None:
                datos[key] = str(datos[key])
        
        datos['ID'] = nuevo_id
        ahora = datetime.now()
        datos['Fecha_Registro'] = ahora
        datos['Fecha_Actualizacion'] = ahora
        # Al crear, el último contacto es la fecha de creación
        datos['Ultimo_Contacto'] = ahora
        
        # Crear nuevo registro
        nuevo_registro = pd.DataFrame([datos])
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        
        if self.guardar_todos(df):
            return nuevo_id
        return None
    
    def actualizar_cliente(self, id_cliente, datos, es_interaccion=False):
        """
        Actualizar cliente existente
        es_interaccion: True si es un registro de interacción (llamada, email, etc.)
                       False si es actualización de datos
        """
        df = self.leer_todos()
        idx = df[df['ID'] == id_cliente].index
        
        if len(idx) > 0:
            ahora = datetime.now()
            
            # Actualizar los campos
            for key, value in datos.items():
                if key in df.columns:
                    # Convertir campos de texto a string
                    if key in ['Teléfono', 'Celular'] and value is not None:
                        value = str(value)
                    df.loc[idx[0], key] = value
            
            # Siempre actualizar Fecha_Actualizacion
            df.loc[idx[0], 'Fecha_Actualizacion'] = ahora
            
            # Si es una interacción, actualizar Ultimo_Contacto
            if es_interaccion:
                df.loc[idx[0], 'Ultimo_Contacto'] = ahora
            
            if self.guardar_todos(df):
                return True
        return False
    
    def eliminar_cliente(self, id_cliente):
        """Eliminar cliente"""
        df = self.leer_todos()
        df = df[df['ID'] != id_cliente]
        return self.guardar_todos(df)
    
    def buscar_clientes(self, termino):
        """Buscar clientes por término"""
        df = self.leer_todos()
        if df.empty:
            return df
        
        termino = str(termino).lower()
        mask = pd.Series([False] * len(df))
        
        # Buscar en columnas de texto
        columnas_texto = ['Nombre', 'Empresa', 'Email', 'Teléfono', 'Celular', 'Industria', 'Etiquetas', 'Notas']
        for col in columnas_texto:
            if col in df.columns:
                mask |= df[col].astype(str).str.lower().str.contains(termino, na=False)
        
        return df[mask]
    
    def obtener_estadisticas(self):
        """Obtener estadísticas para dashboard - SIN Valor_Estimado"""
        df = self.leer_todos()
        if df.empty:
            return {
                'total': 0,
                'por_estado': {},
                'por_industria': {},
                'nuevos_mes': 0,
                'proximos_seguimientos': []
            }
        
        stats = {
            'total': len(df),
            'por_estado': df['Estado'].value_counts().to_dict(),
            'por_industria': df['Industria'].value_counts().to_dict(),
            'nuevos_mes': 0,
            'proximos_seguimientos': []
        }
        
        # Nuevos este mes
        if 'Fecha_Registro' in df.columns:
            hoy = datetime.now()
            inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0)
            stats['nuevos_mes'] = len(df[pd.to_datetime(df['Fecha_Registro']) >= inicio_mes])
        
        # Próximos seguimientos (todas las fechas futuras)
        if 'Proximo_Seguimiento' in df.columns:
            hoy = datetime.now()
            # Considerar todos los seguimientos futuros (no solo 7 días)
            seguimientos = df[pd.to_datetime(df['Proximo_Seguimiento']) >= hoy]
            stats['proximos_seguimientos'] = seguimientos.to_dict('records')
        
        return stats

# ============================================
# INICIALIZAR CRM
# ============================================
@st.cache_resource
def init_crm():
    return CRMExcel()

crm = init_crm()

# ============================================
# FUNCIONES DE UTILIDAD
# ============================================
def formatear_fecha(fecha):
    if pd.isna(fecha) or fecha is None:
        return "-"
    if isinstance(fecha, str):
        try:
            fecha = pd.to_datetime(fecha)
        except:
            return fecha
    if hasattr(fecha, 'strftime'):
        return fecha.strftime('%d/%m/%Y %H:%M')
    return str(fecha)

def formatear_nota(nota):
    """Formatear nota para mostrar solo la última línea"""
    if pd.isna(nota) or nota is None:
        return "-"
    if isinstance(nota, str):
        lineas = nota.strip().split('\n')
        if lineas:
            ultima = lineas[-1].strip()
            if len(ultima) > 50:
                return ultima[:47] + "..."
            return ultima
    return str(nota)[:50]

def verificar_alertas():
    """Verifica si hay citas próximas en los próximos 5 minutos"""
    df = crm.leer_todos()
    alertas = []
    
    if not df.empty and 'Proximo_Seguimiento' in df.columns:
        ahora = datetime.now()
        limite = ahora + timedelta(minutes=5)
        
        for _, cliente in df.iterrows():
            if pd.notna(cliente['Proximo_Seguimiento']):
                fecha_cita = pd.to_datetime(cliente['Proximo_Seguimiento'])
                # Verificar si la cita está en el rango de 5 minutos
                if fecha_cita >= ahora and fecha_cita <= limite:
                    minutos = int((fecha_cita - ahora).total_seconds() / 60)
                    alertas.append({
                        'cliente': cliente['Nombre'],
                        'empresa': cliente['Empresa'] if pd.notna(cliente['Empresa']) else 'Sin empresa',
                        'fecha': fecha_cita,
                        'minutos': minutos
                    })
    
    return alertas

def reproducir_alerta():
    """Reproduce un sonido de alerta (solo en Windows) o muestra notificación en otros sistemas"""
    try:
        import platform
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(800, 500)
            time.sleep(0.2)
            winsound.Beep(1000, 500)
        else:
            # En Linux/Mac, mostrar notificación visual
            st.toast("🔔 ¡Alerta de cita próxima!", icon="🔔")
    except:
        pass  # Silenciosamente falla si no hay soporte

# ============================================
# MENÚ PRINCIPAL
# ============================================
# Inicializar session_state si no existe
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 VISTA GENERAL"
if 'alertas_mostradas' not in st.session_state:
    st.session_state.alertas_mostradas = set()

# Definir las páginas
paginas = ["🏠 Dashboard", "➕ Nuevo Cliente", "📋 Mis Clientes", 
           "📞 Interacciones", "🔍 Buscar", "📊 Reportes", "⚙️ Configuración"]

# Header
st.markdown('<div class="main-header"><h1>📊 Mi CRM Personal</h1><p>Gestión profesional de relaciones con Excel</p></div>', unsafe_allow_html=True)

# ============================================
# VERIFICACIÓN DE ALERTAS (VERSIÓN CON COLORES MEJORADOS)
# ============================================
alertas = verificar_alertas()

# Mostrar alertas si hay citas próximas
if alertas:
    st.markdown("### 🔔 ALERTAS DE CITAS PRÓXIMAS")
    
    for alerta in alertas:
        alerta_id = f"{alerta['cliente']}_{alerta['fecha']}"
        
        # Determinar nivel de urgencia para colores
        minutos = alerta['minutos']
        if minutos <= 2:
            # Muy urgente - Rojo
            bg_color = "#ff6b6b"
            border_color = "#c0392b"
            text_color = "#0A0000"
            title_color = "#0A0000"
            title = "🚨 ¡CITA URGENTE!"
        elif minutos <= 5:
            # Urgente - Naranja
            bg_color = "#ff9f43"
            border_color = "#e67e22"
            text_color = "#2d3436"
            title_color = "#2d3436"
            title = "⏰ ¡CITA PRÓXIMA!"
        else:
            # Normal - Amarillo
            bg_color = "#ffeaa7"
            border_color = "#fdcb6e"
            text_color = "#2d3436"
            title_color = "#2d3436"
            title = "📅 Cita Programada"
        
        st.markdown(f"""
        <div style="
            background: {bg_color};
            border-left: 6px solid {border_color};
            padding: 1.2rem 1.5rem;
            border-radius: 8px;
            margin: 0.8rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            animation: parpadeo 1.5s infinite;
        ">
            <div style="font-size: 1.1rem; font-weight: bold; color: {title_color}; margin-bottom: 0.5rem;">
                {title}
            </div>
            <div style="font-size: 1.2rem; font-weight: bold; color: {text_color}; margin-bottom: 0.3rem;">
                👤 {alerta['cliente']}
            </div>
            <div style="color: {text_color}; font-weight: normal; margin-bottom: 0.3rem;">
                📍 {alerta['empresa']}
            </div>
            <div style="color: {text_color}; font-weight: bold; margin-bottom: 0.3rem;">
                📅 {formatear_fecha(alerta['fecha'])}
            </div>
            <div style="color: {'#c0392b' if minutos <= 5 else '#2d3436'}; font-weight: bold; font-size: 1.1rem;">
                ⏳ Tiempo restante: {alerta['minutos']} minutos
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Reproducir sonido si es una alerta nueva
        if alerta_id not in st.session_state.alertas_mostradas:
            reproducir_alerta()
            st.session_state.alertas_mostradas.add(alerta_id)
        
        if st.button(f"✅ Marcar como vista - {alerta['cliente']}", key=f"alerta_{alerta_id}"):
            st.session_state.alertas_mostradas.discard(alerta_id)
            st.rerun()
    
    st.divider()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/contacts.png", width=80)
    st.markdown("## 📋 Navegación")
    
    menu = st.radio(
        "Selecciona una opción:",
        paginas,
        index=paginas.index(st.session_state.pagina)
    )
    
    # Actualizar la página seleccionada
    st.session_state.pagina = menu
    
    st.markdown("---")
    stats = crm.obtener_estadisticas()
    st.metric("Total Clientes", stats['total'])
    
    # Mostrar próximas citas en el sidebar
    if stats['proximos_seguimientos']:
        st.markdown("### 📅 Próximas Citas")
        for cliente in stats['proximos_seguimientos'][:3]:
            fecha = pd.to_datetime(cliente['Proximo_Seguimiento'])
            dias = (fecha - datetime.now()).days
            if dias < 0:
                texto = "⚠️ ATRASADA"
            elif dias == 0:
                horas = int((fecha - datetime.now()).total_seconds() / 3600)
                texto = f"⏰ Hoy en {horas}h"
            elif dias == 1:
                texto = "📅 Mañana"
            else:
                texto = f"📅 En {dias} días"
            
            st.caption(f"• {cliente['Nombre']}: {texto}")
    
    st.caption(f"💾 Datos en: data/clientes.xlsx")
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Asignar la página actual
menu = st.session_state.pagina

# ============================================
# PÁGINA: DASHBOARD
# ============================================
if menu == "🏠 Dashboard":
    st.header("📈 Panel de Control")
    
    stats = crm.obtener_estadisticas()
    df = crm.leer_todos()
    
    if not df.empty:
        # Métricas - SIN Valor Estimado (solo 3 columnas)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{stats['total']}</div>
                <div class="stat-label">👥 Total Clientes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            activos = stats['por_estado'].get('Activo', 0)
            st.markdown(f"""
            <div class="stat-card" style="border-left-color: #2ecc71;">
                <div class="stat-value">{activos}</div>
                <div class="stat-label">✅ Activos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card" style="border-left-color: #f39c12;">
                <div class="stat-value">{stats['nuevos_mes']}</div>
                <div class="stat-label">🆕 Nuevos este mes</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ============================================
        # CITAS DE HOY - VERSIÓN CON COLORES MEJORADOS
        # ============================================
        st.subheader("📅 Citas de Hoy")
        if 'Proximo_Seguimiento' in df.columns:
            hoy = datetime.now()
            citas_hoy = df[
                (pd.to_datetime(df['Proximo_Seguimiento']).dt.date == hoy.date()) &
                (pd.to_datetime(df['Proximo_Seguimiento']) >= hoy)
            ]
            
            if not citas_hoy.empty:
                for _, cliente in citas_hoy.iterrows():
                    fecha = pd.to_datetime(cliente['Proximo_Seguimiento'])
                    horas_restantes = int((fecha - hoy).total_seconds() / 3600)
                    minutos_restantes = int(((fecha - hoy).total_seconds() % 3600) / 60)
                    
                    # Determinar urgencia y color
                    if horas_restantes < 1:
                        # Rojo - URGENTE (menos de 1 hora)
                        st.markdown(f"""
                        <div class="cita-urgente">
                            <strong>🔴 ¡URGENTE!</strong><br>
                            <span class="cliente-nombre">{cliente['Nombre']}</span><br>
                            <span style="color: #721c24;">{cliente['Empresa'] if pd.notna(cliente['Empresa']) else 'Sin empresa'}</span><br>
                            ⏰ {formatear_fecha(fecha)} - <span class="tiempo-restante">En {horas_restantes}h {minutos_restantes}min</span>
                        </div>
                        """, unsafe_allow_html=True)
                    elif horas_restantes < 4:
                        # Amarillo/Naranja - Próxima (entre 1 y 4 horas)
                        st.markdown(f"""
                        <div class="cita-proxima">
                            <strong>🟡 ¡PRÓXIMA!</strong><br>
                            <span class="cliente-nombre">{cliente['Nombre']}</span><br>
                            <span style="color: #856404;">{cliente['Empresa'] if pd.notna(cliente['Empresa']) else 'Sin empresa'}</span><br>
                            ⏰ {formatear_fecha(fecha)} - En {horas_restantes}h {minutos_restantes}min
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Verde - Programada (más de 4 horas)
                        st.markdown(f"""
                        <div class="cita-programada">
                            <strong>🟢 Programada</strong><br>
                            <span class="cliente-nombre">{cliente['Nombre']}</span><br>
                            <span style="color: #155724;">{cliente['Empresa'] if pd.notna(cliente['Empresa']) else 'Sin empresa'}</span><br>
                            ⏰ {formatear_fecha(fecha)} - En {horas_restantes}h {minutos_restantes}min
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("✅ No hay citas programadas para hoy")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Distribución por Estado")
            if stats['por_estado']:
                fig = px.pie(
                    values=list(stats['por_estado'].values()),
                    names=list(stats['por_estado'].keys()),
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=0.4
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sin datos")
        
        with col2:
            st.subheader("🏭 Top Industrias")
            if stats['por_industria']:
                industrias = sorted(stats['por_industria'].items(), key=lambda x: x[1], reverse=True)[:5]
                fig = px.bar(
                    x=[i[1] for i in industrias],
                    y=[i[0] for i in industrias],
                    orientation='h',
                    color=[i[1] for i in industrias],
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sin datos")
        
        # Tabla de últimos clientes
        st.subheader("📋 Últimos Clientes Registrados")
        ultimos = df.sort_values('Fecha_Registro', ascending=False).head(10)
        ultimos_display = ultimos[['ID', 'Nombre', 'Empresa', 'Estado', 'Ultimo_Contacto']].copy()
        ultimos_display['Ultimo_Contacto'] = ultimos_display['Ultimo_Contacto'].apply(formatear_fecha)
        st.dataframe(ultimos_display, use_container_width=True)
        
        # Próximos seguimientos - CON COLORES
        if stats['proximos_seguimientos']:
            st.subheader("⏰ Todos los Seguimientos Programados")
            for cliente in sorted(stats['proximos_seguimientos'], 
                                key=lambda x: pd.to_datetime(x['Proximo_Seguimiento']))[:10]:
                fecha = pd.to_datetime(cliente['Proximo_Seguimiento'])
                ahora = datetime.now()
                dias = (fecha - ahora).days
                horas = int((fecha - ahora).total_seconds() / 3600)
                
                if dias < 0:
                    estado = "⚠️ ATRASADA"
                    clase = "seguimiento-atrasado"
                    color_clase = "cita-atrasada"
                elif dias == 0:
                    if horas < 1:
                        estado = "🔴 ¡URGENTE!"
                        clase = "seguimiento-urgente"
                    elif horas < 4:
                        estado = "🟡 Próxima"
                        clase = "seguimiento-proximo"
                    else:
                        estado = "🟢 Hoy"
                        clase = "seguimiento-hoy"
                elif dias == 1:
                    estado = "📅 Mañana"
                    clase = "seguimiento-manana"
                else:
                    estado = f"📅 En {dias} días"
                    clase = "seguimiento-normal"
                
                st.markdown(f"""
                <div class="{clase}">
                    <strong>{cliente['Nombre']}</strong> - {formatear_fecha(fecha)} - {estado}
                </div>
                """, unsafe_allow_html=True)
        
        # Botón para ir a Nuevo Cliente
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➕ Ir a Nuevo Cliente", use_container_width=True):
                st.session_state.pagina = "➕ Nuevo Cliente"
                st.rerun()
        
    else:
        st.info("🎯 ¡Bienvenido! Comienza registrando tu primer cliente.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➕ Crear mi primer cliente", use_container_width=True):
                st.session_state.pagina = "➕ Nuevo Cliente"
                st.rerun()

# ============================================
# PÁGINA: NUEVO CLIENTE
# ============================================
elif menu == "➕ Nuevo Cliente":
    st.header("➕ Registrar Nuevo Cliente")
    
    with st.form("form_nuevo_cliente", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre Completo *", placeholder="Ej: Juan Pérez")
            empresa = st.text_input("Empresa", placeholder="Ej: Tech Solutions")
            email = st.text_input("Email", placeholder="juan@empresa.com")
            telefono = st.text_input("Teléfono", placeholder="55 1234 5678")
            celular = st.text_input("Celular", placeholder="55 9876 5432")
        
        with col2:
            industria = st.selectbox(
                "Industria",
                ["", "Tecnología", "Salud", "Finanzas", "Educación", "Manufactura", 
                 "Retail", "Consultoría", "Marketing", "Legal", "Construcción", 
                 "Entretenimiento", "Otro"]
            )
            cargo = st.text_input("Cargo", placeholder="Ej: Director de Ventas")
            estado = st.selectbox("Estado", ["Potencial", "Activo", "Inactivo", "Perdido"])
            prioridad = st.select_slider("Prioridad", options=[1, 2, 3], value=2, 
                                        help="1=Baja, 2=Media, 3=Alta")
            fuente = st.selectbox("Fuente", ["", "Web", "Referido", "Redes Sociales", 
                                            "Evento", "LinkedIn", "Otro"])
        
        etiquetas = st.text_input("Etiquetas (separadas por coma)", 
                                 placeholder="VIP, Cliente importante, Sector salud")
        
        st.subheader("📅 Programar Primer Seguimiento")
        col_fecha, col_hora = st.columns(2)
        with col_fecha:
            fecha_seguimiento = st.date_input("Fecha", value=datetime.now().date() + timedelta(days=7))
        with col_hora:
            hora_seguimiento = st.time_input("Hora", value=datetime.now().time().replace(hour=10, minute=0))
        
        notas = st.text_area("Notas", placeholder="Información relevante sobre el cliente...")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("💾 Guardar Cliente", use_container_width=True)
        
        if submitted:
            if not nombre:
                st.error("⚠️ El nombre es obligatorio")
            else:
                # Combinar fecha y hora para el seguimiento
                fecha_hora_seguimiento = datetime.combine(fecha_seguimiento, hora_seguimiento)
                
                datos = {
                    'Nombre': nombre,
                    'Empresa': empresa if empresa else None,
                    'Email': email if email else None,
                    'Teléfono': telefono if telefono else None,
                    'Celular': celular if celular else None,
                    'Industria': industria if industria else None,
                    'Cargo': cargo if cargo else None,
                    'Estado': estado,
                    'Prioridad': prioridad,
                    'Fuente': fuente if fuente else None,
                    'Etiquetas': etiquetas if etiquetas else None,
                    'Notas': notas if notas else None,
                    'Proximo_Seguimiento': fecha_hora_seguimiento
                }
                
                cliente_id = crm.agregar_cliente(datos)
                if cliente_id:
                    st.success(f"✅ Cliente registrado exitosamente (ID: {cliente_id})")
                    st.info(f"📅 Seguimiento programado para: {formatear_fecha(fecha_hora_seguimiento)}")
                    st.balloons()
                    st.rerun()

# ============================================
# PÁGINA: MIS CLIENTES
# ============================================
elif menu == "📋 Mis Clientes":
    st.header("📋 Lista de Clientes")
    
    df = crm.leer_todos()
    
    if not df.empty:
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            estados = ["Todos"] + df['Estado'].dropna().unique().tolist()
            estado_filter = st.selectbox("Filtrar por Estado", estados)
        
        with col2:
            industrias = ["Todos"] + df['Industria'].dropna().unique().tolist()
            industria_filter = st.selectbox("Filtrar por Industria", industrias)
        
        with col3:
            ordenar = st.selectbox("Ordenar por", 
                                  ["Nombre", "Empresa", "Fecha_Registro", "Ultimo_Contacto", "Proximo_Seguimiento"])
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if estado_filter != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Estado'] == estado_filter]
        
        if industria_filter != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Industria'] == industria_filter]
        
        df_filtrado = df_filtrado.sort_values(ordenar, ascending=False)
        
        # Mostrar tabla - CON Notas y Actualización
        if not df_filtrado.empty:
            # Preparar datos para mostrar
            display_df = df_filtrado[['ID', 'Nombre', 'Empresa', 'Estado', 'Prioridad', 
                                     'Ultimo_Contacto', 'Proximo_Seguimiento', 
                                     'Fecha_Actualizacion', 'Notas']].copy()
            
            # Formatear fechas
            display_df['Ultimo_Contacto'] = display_df['Ultimo_Contacto'].apply(formatear_fecha)
            display_df['Proximo_Seguimiento'] = display_df['Proximo_Seguimiento'].apply(formatear_fecha)
            display_df['Fecha_Actualizacion'] = display_df['Fecha_Actualizacion'].apply(formatear_fecha)
            
            # Formatear notas - mostrar solo la última
            display_df['Notas'] = display_df['Notas'].apply(formatear_nota)
            
            # Renombrar columnas
            display_df.columns = ['ID', 'Nombre', 'Empresa', 'Estado', 'Prioridad', 
                                 'Último Contacto', 'Próximo Seguimiento', 'Actualización', 'Última Nota']
            
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # Acciones individuales
            st.subheader("✏️ Editar o Eliminar Cliente")
            
            cliente_seleccionado = st.selectbox(
                "Seleccionar cliente",
                options=df_filtrado['ID'].tolist(),
                format_func=lambda x: f"{x} - {df_filtrado[df_filtrado['ID']==x]['Nombre'].iloc[0]}"
            )
            
            if cliente_seleccionado:
                cliente = df[df['ID'] == cliente_seleccionado].iloc[0]
                
                with st.expander(f"📝 Editando: {cliente['Nombre']}", expanded=True):
                    st.info(f"📅 Último contacto: {formatear_fecha(cliente['Ultimo_Contacto'])}")
                    st.info(f"📅 Última actualización: {formatear_fecha(cliente['Fecha_Actualizacion'])}")
                    
                    # Mostrar historial de notas
                    if pd.notna(cliente['Notas']) and cliente['Notas']:
                        st.subheader("📝 Historial de Notas")
                        notas = cliente['Notas'].strip().split('\n')
                        for nota in notas:
                            if nota.strip():
                                st.text(f"• {nota.strip()}")
                        st.divider()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        nuevo_nombre = st.text_input("Nombre", value=cliente['Nombre'])
                        nueva_empresa = st.text_input("Empresa", value=cliente['Empresa'] if pd.notna(cliente['Empresa']) else '')
                        nuevo_email = st.text_input("Email", value=cliente['Email'] if pd.notna(cliente['Email']) else '')
                        nuevo_telefono = st.text_input("Teléfono", value=cliente['Teléfono'] if pd.notna(cliente['Teléfono']) else '')
                    
                    with col2:
                        nuevo_estado = st.selectbox(
                            "Estado",
                            ["Potencial", "Activo", "Inactivo", "Perdido"],
                            index=["Potencial", "Activo", "Inactivo", "Perdido"].index(cliente['Estado'])
                        )
                        
                        st.subheader("📅 Programar Seguimiento")
                        col_fecha, col_hora = st.columns(2)
                        with col_fecha:
                            fecha_actual = cliente['Proximo_Seguimiento'] if pd.notna(cliente['Proximo_Seguimiento']) else datetime.now() + timedelta(days=7)
                            if isinstance(fecha_actual, pd.Timestamp):
                                fecha_actual = fecha_actual.to_pydatetime()
                            nueva_fecha = st.date_input("Fecha", value=fecha_actual.date())
                        with col_hora:
                            nueva_hora = st.time_input("Hora", value=fecha_actual.time())
                        
                        nuevas_notas = st.text_area("Agregar Nota", 
                                                   placeholder="Escribe una nueva nota de seguimiento...")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("💾 Actualizar Datos", type="primary"):
                            # Combinar fecha y hora
                            fecha_hora_seguimiento = datetime.combine(nueva_fecha, nueva_hora)
                            
                            # Preparar datos para actualizar
                            datos = {
                                'Nombre': nuevo_nombre,
                                'Empresa': nueva_empresa if nueva_empresa else None,
                                'Email': nuevo_email if nuevo_email else None,
                                'Teléfono': str(nuevo_telefono) if nuevo_telefono else None,
                                'Estado': nuevo_estado,
                                'Proximo_Seguimiento': fecha_hora_seguimiento
                            }
                            
                            # Si hay una nueva nota, agregarla al historial
                            if nuevas_notas and nuevas_notas.strip():
                                nota_actual = cliente['Notas'] if pd.notna(cliente['Notas']) else ""
                                timestamp = datetime.now().strftime('[%d/%m/%Y %H:%M]')
                                nueva_nota_completa = f"{timestamp} {nuevas_notas.strip()}"
                                
                                if nota_actual:
                                    datos['Notas'] = f"{nota_actual}\n{nueva_nota_completa}"
                                else:
                                    datos['Notas'] = nueva_nota_completa
                            
                            # Actualización de datos (NO actualiza Ultimo_Contacto)
                            if crm.actualizar_cliente(cliente_seleccionado, datos, es_interaccion=False):
                                st.success("✅ Cliente actualizado")
                                st.info(f"📅 Seguimiento programado para: {formatear_fecha(fecha_hora_seguimiento)}")
                                st.rerun()
                    
                    with col3:
                        if st.button("🗑️ Eliminar", type="secondary"):
                            if st.checkbox("⚠️ Confirmar eliminación permanente"):
                                if crm.eliminar_cliente(cliente_seleccionado):
                                    st.warning("❌ Cliente eliminado")
                                    st.rerun()
        else:
            st.info("No hay clientes con esos filtros")
    else:
        st.info("📭 No hay clientes registrados. ¡Comienza agregando uno!")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➕ Ir a Nuevo Cliente", use_container_width=True):
                st.session_state.pagina = "➕ Nuevo Cliente"
                st.rerun()

# ============================================
# PÁGINA: INTERACCIONES
# ============================================
elif menu == "📞 Interacciones":
    st.header("📞 Registrar Interacción")
    
    df = crm.leer_todos()
    
    if not df.empty:
        # Seleccionar cliente
        cliente_seleccionado = st.selectbox(
            "Seleccionar cliente",
            options=df['ID'].tolist(),
            format_func=lambda x: f"{x} - {df[df['ID']==x]['Nombre'].iloc[0]} - {df[df['ID']==x]['Empresa'].iloc[0] or 'Sin empresa'}"
        )
        
        if cliente_seleccionado:
            cliente = df[df['ID'] == cliente_seleccionado].iloc[0]
            
            st.info(f"📅 Último contacto: {formatear_fecha(cliente['Ultimo_Contacto'])}")
            
            with st.form("form_interaccion"):
                col1, col2 = st.columns(2)
                
                with col1:
                    tipo = st.selectbox("Tipo de Interacción", 
                                       ["📞 Llamada", "✉️ Email", "🤝 Reunión", "💬 Mensaje", "📝 Nota"])
                    resumen = st.text_input("Resumen", placeholder="Breve descripción de la interacción")
                
                with col2:
                    resultado = st.selectbox("Resultado", 
                                            ["✅ Positivo", "➖ Neutral", "❌ Negativo", "⏳ Pendiente"])
                    
                    st.subheader("📅 Programar Próximo Seguimiento")
                    col_fecha, col_hora = st.columns(2)
                    with col_fecha:
                        fecha_seguimiento = st.date_input("Fecha", value=datetime.now().date() + timedelta(days=7))
                    with col_hora:
                        hora_seguimiento = st.time_input("Hora", value=datetime.now().time().replace(hour=10, minute=0))
                
                detalle = st.text_area("Detalle", placeholder="Describe la interacción en detalle...")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submitted = st.form_submit_button("💾 Registrar Interacción", use_container_width=True)
                
                if submitted:
                    if not resumen:
                        st.error("⚠️ El resumen es obligatorio")
                    else:
                        # Combinar fecha y hora para el seguimiento
                        fecha_hora_seguimiento = datetime.combine(fecha_seguimiento, hora_seguimiento)
                        
                        # Registrar interacción - Esto actualizará Ultimo_Contacto
                        notas_actuales = cliente['Notas'] if pd.notna(cliente['Notas']) else ""
                        timestamp = datetime.now().strftime('[%d/%m/%Y %H:%M]')
                        nueva_nota = f"{timestamp} {tipo}: {resumen}"
                        if detalle:
                            nueva_nota += f"\n    Detalle: {detalle}"
                        if resultado:
                            nueva_nota += f"\n    Resultado: {resultado}"
                        
                        if notas_actuales:
                            nueva_nota_completa = f"{notas_actuales}\n{nueva_nota}"
                        else:
                            nueva_nota_completa = nueva_nota
                        
                        datos = {
                            'Notas': nueva_nota_completa,
                            'Proximo_Seguimiento': fecha_hora_seguimiento
                        }
                        
                        # es_interaccion=True para actualizar Ultimo_Contacto
                        if crm.actualizar_cliente(cliente_seleccionado, datos, es_interaccion=True):
                            st.success("✅ Interacción registrada exitosamente")
                            st.info(f"📅 Próximo seguimiento programado para: {formatear_fecha(fecha_hora_seguimiento)}")
                            st.balloons()
                            st.rerun()
    else:
        st.info("📭 No hay clientes registrados. ¡Comienza agregando uno!")

# ============================================
# PÁGINA: BUSCAR
# ============================================
elif menu == "🔍 Buscar":
    st.header("🔍 Buscar Clientes")
    
    busqueda = st.text_input("Buscar por nombre, empresa, email, teléfono, etiquetas o notas",
                            placeholder="Ej: Juan, Tech, @gmail.com, reunión")
    
    if busqueda:
        resultados = crm.buscar_clientes(busqueda)
        
        if not resultados.empty:
            st.success(f"✅ Encontrados {len(resultados)} resultados")
            
            # Mostrar resultados
            display = resultados[['ID', 'Nombre', 'Empresa', 'Email', 'Estado', 
                                 'Ultimo_Contacto', 'Proximo_Seguimiento',
                                 'Fecha_Actualizacion', 'Notas']].copy()
            display['Ultimo_Contacto'] = display['Ultimo_Contacto'].apply(formatear_fecha)
            display['Proximo_Seguimiento'] = display['Proximo_Seguimiento'].apply(formatear_fecha)
            display['Fecha_Actualizacion'] = display['Fecha_Actualizacion'].apply(formatear_fecha)
            display['Notas'] = display['Notas'].apply(formatear_nota)
            display.columns = ['ID', 'Nombre', 'Empresa', 'Email', 'Estado', 
                              'Último Contacto', 'Próximo Seguimiento',
                              'Actualización', 'Última Nota']
            
            st.dataframe(display, use_container_width=True)
            
            # Mostrar detalle de cada resultado
            st.subheader("📄 Detalle completo")
            for _, row in resultados.iterrows():
                with st.expander(f"📌 {row['Nombre']} - {row['Empresa']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Email:** {row['Email']}")
                        st.write(f"**Teléfono:** {row['Teléfono']}")
                        st.write(f"**Celular:** {row['Celular']}")
                        st.write(f"**Industria:** {row['Industria']}")
                        st.write(f"**Cargo:** {row['Cargo']}")
                    with col2:
                        st.write(f"**Estado:** {row['Estado']}")
                        st.write(f"**Prioridad:** {row['Prioridad']}")
                        st.write(f"**Fuente:** {row['Fuente']}")
                        st.write(f"**Último Contacto:** {formatear_fecha(row['Ultimo_Contacto'])}")
                        st.write(f"**Próximo Seguimiento:** {formatear_fecha(row['Proximo_Seguimiento'])}")
                        st.write(f"**Actualización:** {formatear_fecha(row['Fecha_Actualizacion'])}")
                        if pd.notna(row['Etiquetas']):
                            st.write(f"**Etiquetas:** {row['Etiquetas']}")
                    
                    # Mostrar todas las notas
                    if pd.notna(row['Notas']) and row['Notas']:
                        st.subheader("📝 Historial de Notas")
                        notas = row['Notas'].strip().split('\n')
                        for nota in notas:
                            if nota.strip():
                                st.text(f"• {nota.strip()}")
        else:
            st.info("❌ No se encontraron resultados")

# ============================================
# PÁGINA: REPORTES
# ============================================
elif menu == "📊 Reportes":
    st.header("📊 Reportes y Análisis")
    
    df = crm.leer_todos()
    
    if not df.empty:
        # Exportar
        st.subheader("📥 Exportar Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Exportar a Excel", use_container_width=True):
                # Crear archivo en memoria
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Clientes', index=False)
                
                st.download_button(
                    label="⬇️ Descargar Excel",
                    data=output.getvalue(),
                    file_name=f"clientes_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col2:
            if st.button("📋 Ver Resumen Estadístico", use_container_width=True):
                st.dataframe(df.describe())
        
        # Análisis temporal
        st.subheader("📈 Análisis Temporal")
        
        if 'Fecha_Registro' in df.columns:
            df['Fecha_Registro'] = pd.to_datetime(df['Fecha_Registro'])
            df['Mes'] = df['Fecha_Registro'].dt.to_period('M')
            
            registros_mes = df.groupby('Mes').size().reset_index(name='Cantidad')
            registros_mes['Mes'] = registros_mes['Mes'].astype(str)
            
            fig = px.line(registros_mes, x='Mes', y='Cantidad',
                         title='Registros de Clientes por Mes',
                         markers=True)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Clientes por último contacto
        st.subheader("⏰ Clientes sin contacto reciente")
        if 'Ultimo_Contacto' in df.columns:
            df['Ultimo_Contacto'] = pd.to_datetime(df['Ultimo_Contacto'])
            hace_30_dias = datetime.now() - timedelta(days=30)
            sin_contacto = df[df['Ultimo_Contacto'] < hace_30_dias]
            
            if not sin_contacto.empty:
                st.warning(f"⚠️ {len(sin_contacto)} clientes sin contacto en los últimos 30 días")
                display = sin_contacto[['Nombre', 'Empresa', 'Estado', 'Ultimo_Contacto']].copy()
                display['Ultimo_Contacto'] = display['Ultimo_Contacto'].apply(formatear_fecha)
                st.dataframe(display, use_container_width=True)
            else:
                st.success("✅ Todos los clientes han tenido contacto reciente")
        
        # Actividad reciente
        st.subheader("📝 Actividad Reciente")
        if 'Fecha_Actualizacion' in df.columns:
            df['Fecha_Actualizacion'] = pd.to_datetime(df['Fecha_Actualizacion'])
            recientes = df.sort_values('Fecha_Actualizacion', ascending=False).head(10)
            display = recientes[['Nombre', 'Empresa', 'Estado', 'Fecha_Actualizacion']].copy()
            display['Fecha_Actualizacion'] = display['Fecha_Actualizacion'].apply(formatear_fecha)
            display.columns = ['Nombre', 'Empresa', 'Estado', 'Última Actividad']
            st.dataframe(display, use_container_width=True)
        
        # Próximas citas
        st.subheader("📅 Próximas Citas Programadas")
        if 'Proximo_Seguimiento' in df.columns:
            df['Proximo_Seguimiento'] = pd.to_datetime(df['Proximo_Seguimiento'])
            hoy = datetime.now()
            proximas = df[df['Proximo_Seguimiento'] >= hoy].sort_values('Proximo_Seguimiento')
            
            if not proximas.empty:
                display = proximas[['Nombre', 'Empresa', 'Estado', 'Proximo_Seguimiento']].copy()
                display['Proximo_Seguimiento'] = display['Proximo_Seguimiento'].apply(formatear_fecha)
                display.columns = ['Nombre', 'Empresa', 'Estado', 'Próxima Cita']
                st.dataframe(display, use_container_width=True)
            else:
                st.success("✅ No hay citas programadas")
        
    else:
        st.info("No hay datos para generar reportes")

# ============================================
# PÁGINA: CONFIGURACIÓN
# ============================================
elif menu == "⚙️ Configuración":
    st.header("⚙️ Configuración")
    
    st.subheader("💾 Gestión de Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📦 Crear Respaldo Ahora", use_container_width=True):
            crm.crear_backup()
            st.success("✅ Respaldo creado en la carpeta 'backups'")
    
    with col2:
        if st.button("📂 Abrir Carpeta de Datos", use_container_width=True):
            st.info("📁 Abre la carpeta 'data' para ver el archivo Excel")
    
    st.subheader("📊 Información del Sistema")
    
    df = crm.leer_todos()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clientes", len(df))
    col2.metric("Columnas", len(df.columns))
    col3.metric("Archivo", "clientes.xlsx")
    
    if not df.empty:
        st.write("**📅 Última actualización:**", datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        st.write("**📊 Registros totales:**", len(df))
        st.write("**📁 Tamaño del archivo:**", 
                f"{os.path.getsize('data/clientes.xlsx') / 1024:.2f} KB" if os.path.exists('data/clientes.xlsx') else "N/A")
        
        # Últimos contactos
        st.subheader("📞 Resumen de Contactos")
        if 'Ultimo_Contacto' in df.columns:
            df['Ultimo_Contacto'] = pd.to_datetime(df['Ultimo_Contacto'])
            hoy = datetime.now()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Contacto hoy", len(df[df['Ultimo_Contacto'].dt.date == hoy.date()]))
            col2.metric("Contacto esta semana", len(df[df['Ultimo_Contacto'] > (hoy - timedelta(days=7))]))
            col3.metric("Sin contacto (30+ días)", len(df[df['Ultimo_Contacto'] < (hoy - timedelta(days=30))]))
        
        # Próximas citas
        st.subheader("📅 Resumen de Citas")
        if 'Proximo_Seguimiento' in df.columns:
            df['Proximo_Seguimiento'] = pd.to_datetime(df['Proximo_Seguimiento'])
            hoy = datetime.now()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Citas hoy", len(df[df['Proximo_Seguimiento'].dt.date == hoy.date()]))
            col2.metric("Citas esta semana", len(df[df['Proximo_Seguimiento'] < (hoy + timedelta(days=7))]))
            col3.metric("Citas atrasadas", len(df[df['Proximo_Seguimiento'] < hoy]))
        
        # Verificar backups
        backup_dir = 'backups'
        if os.path.exists(backup_dir):
            backups = [f for f in os.listdir(backup_dir) if f.endswith('.xlsx')]
            st.write(f"**💾 Backups disponibles:** {len(backups)}")
            if backups:
                with st.expander("📂 Ver últimos 5 backups"):
                    for b in sorted(backups)[-5:]:
                        st.write(f"📄 {b}")
    
    st.subheader("⚠️ Zona de Peligro")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Eliminar TODOS los datos", type="secondary", use_container_width=True):
            st.warning("⚠️ Esta acción eliminará TODOS los clientes")
            if st.checkbox("✅ Confirmar eliminación permanente"):
                df_vacio = pd.DataFrame(columns=df.columns if not df.empty else [
                    'ID', 'Nombre', 'Empresa', 'Email', 'Teléfono', 'Celular',
                    'Industria', 'Cargo', 'Estado', 'Prioridad', 'Fuente',
                    'Etiquetas', 'Notas',
                    'Ultimo_Contacto', 'Proximo_Seguimiento',
                    'Fecha_Registro', 'Fecha_Actualizacion'
                ])
                if crm.guardar_todos(df_vacio):
                    st.error("❌ Todos los datos han sido eliminados")
                    st.rerun()

# ============================================
# FOOTER
# ============================================
st.sidebar.markdown("---")
st.sidebar.caption("📊 CRM Personal v2.0")
st.sidebar.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.sidebar.caption("💾 Datos en Excel local")
