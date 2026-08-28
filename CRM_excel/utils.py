# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 12:10:44 2026

@author: DIEGO.NOLASCO
"""

from datetime import datetime

def formatear_moneda(valor):
    """Formatear valor como moneda"""
    if valor is None:
        return "$0"
    return f"${valor:,.0f}"

def calcular_edad_registro(fecha):
    """Calcular días desde registro"""
    if not fecha:
        return "N/A"
    dias = (datetime.now() - fecha).days
    if dias == 0:
        return "Hoy"
    elif dias == 1:
        return "Ayer"
    elif dias < 7:
        return f"Hace {dias} días"
    elif dias < 30:
        semanas = dias // 7
        return f"Hace {semanas} semana{'s' if semanas > 1 else ''}"
    elif dias < 365:
        meses = dias // 30
        return f"Hace {meses} mes{'es' if meses > 1 else ''}"
    else:
        años = dias // 365
        return f"Hace {años} año{'s' if años > 1 else ''}"

def validar_email(email):
    """Validación básica de email"""
    if not email:
        return False
    return '@' in email and '.' in email