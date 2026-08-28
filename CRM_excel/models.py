# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 12:09:27 2026

@author: DIEGO.NOLASCO
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    empresa = Column(String(100))
    email = Column(String(100))
    telefono = Column(String(20))
    celular = Column(String(20))
    direccion = Column(String(200))
    
    # Información de negocio
    industria = Column(String(50))
    cargo = Column(String(50))
    fuente = Column(String(50))  # Web, Referido, Redes, etc.
    
    # Estado y seguimiento
    estado = Column(String(20), default='Potencial')  # Potencial, Activo, Inactivo, Perdido
    prioridad = Column(Integer, default=1)  # 1=Baja, 2=Media, 3=Alta
    valor_estimado = Column(Float, default=0)
    
    # Contacto
    ultimo_contacto = Column(DateTime)
    proximo_seguimiento = Column(DateTime)
    frecuencia_contacto = Column(String(20))  # Diario, Semanal, Quincenal, Mensual
    
    # Notas y metadatos
    notas = Column(Text)
    etiquetas = Column(String(200))  # Tags separados por coma
    origen = Column(String(50))  # Cómo llegó a ti
    
    # Fechas
    fecha_registro = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.now)
    
    # Campos personalizados (para flexibilidad)
    campo_personalizado_1 = Column(String(200))
    campo_personalizado_2 = Column(String(200))
    campo_personalizado_3 = Column(String(200))

class Interaccion(Base):
    __tablename__ = 'interacciones'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, nullable=False)
    tipo = Column(String(30))  # Llamada, Email, Reunión, Mensaje, Nota
    fecha = Column(DateTime, default=datetime.now)
    resumen = Column(Text)
    detalle = Column(Text)
    duracion = Column(Integer)  # minutos
    resultado = Column(String(100))
    proxima_accion = Column(String(200))
    fecha_proximo_contacto = Column(DateTime)

class Tarea(Base):
    __tablename__ = 'tareas'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    prioridad = Column(String(20))  # Alta, Media, Baja
    estado = Column(String(20), default='Pendiente')  # Pendiente, En Progreso, Completada
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_limite = Column(DateTime)
    fecha_completada = Column(DateTime)
    recordatorio = Column(DateTime)

# Crear base de datos
def init_database():
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'crm.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return engine

# Configuración de sesión
engine = init_database()
Session = sessionmaker(bind=engine)