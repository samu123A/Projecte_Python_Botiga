# -*- coding: utf-8 -*-
"""
PROJECTE ABP - PROGRAMACIÓ AMB PYTHON
Sistema Bàsic d'analitiques per a Botiga de Videojocs i Informàtica
"""

import csv
from datetime import datetime

# Funció 1: Menú Principal
def mostrar_menu():
    """
    Mostra el menú principal del sistema i gestiona les opcions seleccionades.
    """
    while True:
        print("\n" + "="*50)
        print("SISTEMA D'ANALITIQUES - BOTIGA DE VIDEOJOCS")
        print("="*50)
        print("1. Calcular facturació total")
        print("2. Mostrar estoc disponible")
        print("3. Top 3 productes més venuts")
        print("4. Sortir")
        print("="*50)
        
        opcio = input("Selecciona una opció (1-4): ")
        
        if opcio == "1":
            calcular_facturacio()
        elif opcio == "2":
            mostrar_estoc()
        elif opcio == "3":
            top_productes()
        elif opcio == "4":
            print("Gràcies per utilitzar el sistema. Fins aviat!")
            break
        else:
            print("Opció no vàlida. Si us plau, selecciona una opció del 1 al 4.")

# Funció 2: Calcular facturació total
def calcular_facturacio():
    """
    Calcula la facturació total (amb IVA i sense IVA) a partir dels datos del CSV.
    """
    try:
        with open('datos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            campos_requeridos = {'Producte', 'Quantitat_Venuda', 'Preu_Unitari', 'IVA'}
            if not campos_requeridos.issubset(reader.fieldnames):
                print("Error: L'arxiu CSV no té les columnes requerides.")
                print(f"Columnes necessàries: {', '.join(campos_requeridos)}")
                print(f"Columnes trobades: {', '.join(reader.fieldnames)}")
                return
            
            facturacio_sense_iva = 0.0
            facturacio_amb_iva = 0.0
            total_productes_venduts = 0
            productes_diferents = set()
            
            for row in reader:
                try:
                    if not all(row[key] for key in campos_requeridos):
                        print(f"Avís: Fila incompleta o amb valors buits - {row['Producte']}")
                        continue
                    
                    quantitat = int(row['Quantitat_Venuda'])
                    preu = float(row['Preu_Unitari'])
                    iva = float(row['IVA'])
                    
                    preu_sense_iva = quantitat * preu
                    preu_amb_iva = preu_sense_iva * (1 + iva/100)
                    
                    facturacio_sense_iva += preu_sense_iva
                    facturacio_amb_iva += preu_amb_iva
                    total_productes_venduts += quantitat
                    productes_diferents.add(row['Producte'])
                
                except ValueError as e:
                    print(f"Avís: Error en processar el producte {row.get('Producte','')} - Error: {str(e)}")
                    continue
            
            print("\n" + "="*50)
            print("INFORME DE FACTURACIÓ")
            print("="*50)
            print(f"Productes diferents venuts: {len(productes_diferents)}")
            print(f"Unitats totals venudes: {total_productes_venduts}")
            print(f"Facturació total sense IVA: {facturacio_sense_iva:.2f}€")
            print(f"Facturació total amb IVA: {facturacio_amb_iva:.2f}€")
            print("="*50)
    
    except FileNotFoundError:
        print("\nError: No s'ha trobat l'arxiu de dades 'datos.csv'")
        print("Assegureu-vos que:")
        print("1. L'arxiu existeix al mateix directori que el programa")
        print("2. El nom de l'arxiu és exactament 'datos.csv'")
        print("3. L'arxiu no està obert en un altre programa")
    except Exception as e:
        print(f"\nError inesperat: {str(e)}")

# Funció 3: Calcular estoc disponible
def mostrar_estoc():
    """
    Mostra l'estoc disponible de cada producte a la botiga.
    """
    try:
        with open('datos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            campos_requeridos = {'Producte', 'Categoria', 'Estoc_Disponible'}
            if not campos_requeridos.issubset(reader.fieldnames):
                print("Error: Falten columnes necessàries al fitxer CSV.")
                return
            
            estoc = {}
            
            for row in reader:
                try:
                    producte = row['Producte']
                    categoria = row['Categoria']
                    quantitat = int(row['Estoc_Disponible'])
                    
                    if producte in estoc:
                        # Si el producto ya existe, sumamos el stock
                        estoc[producte]['quantitat'] += quantitat
                    else:
                        estoc[producte] = {
                            'categoria': categoria,
                            'quantitat': quantitat
                        }
                
                except ValueError as e:
                    print(f"Avís: Error en processar fila - {row['Producte']} - Error: {str(e)}")
                    continue
            
            print("\n" + "="*50)
            print("ESTOC DISPONIBLE")
            print("="*50)
            print("{:<40} {:<20} {:<10}".format("Producte", "Categoria", "Quantitat"))
            print("-"*70)
            
            for producte, info in sorted(estoc.items()):
                print("{:<40} {:<20} {:<10}".format(
                    producte, 
                    info['categoria'], 
                    info['quantitat']
                ))
            
            print("="*70)
    
    except FileNotFoundError:
        print("Error: No s'ha trobat l'arxiu de dades 'datos.csv'")
    except Exception as e:
        print(f"Error inesperat: {str(e)}")

# Funció 4: Top 3 productes més venuts
def top_productes():
    """
    Identifica i mostra els 3 productes més venuts en quantitat.
    """
    try:
        with open('datos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            campos_requeridos = {'Producte', 'Categoria', 'Quantitat_Venuda', 'Preu_Unitari', 'IVA'}
            if not campos_requeridos.issubset(reader.fieldnames):
                print("Error: Falten columnes necessàries al fitxer CSV.")
                return
            
            productes = {}
            
            for row in reader:
                try:
                    nom_producte = row['Producte']
                    quantitat = int(row['Quantitat_Venuda'])
                    preu = float(row['Preu_Unitari'])
                    iva = float(row['IVA'])
                    
                    if nom_producte in productes:
                        productes[nom_producte]['quantitat'] += quantitat
                        productes[nom_producte]['facturacio_sense_iva'] += quantitat * preu
                        productes[nom_producte]['facturacio_amb_iva'] += quantitat * preu * (1 + iva/100)
                    else:
                        productes[nom_producte] = {
                            'categoria': row['Categoria'],
                            'quantitat': quantitat,
                            'facturacio_sense_iva': quantitat * preu,
                            'facturacio_amb_iva': quantitat * preu * (1 + iva/100)
                        }
                
                except ValueError as e:
                    print(f"Avís: Error en processar el producte {row.get('Producte','')} - Error: {str(e)}")
                    continue
            
            top3 = sorted(
                productes.items(), 
                key=lambda x: x[1]['quantitat'], 
                reverse=True
            )[:3]
            
            print("\n" + "="*50)
            print("TOP 3 PRODUCTES MÉS VENUTS")
            print("="*50)
            print("{:<5} {:<40} {:<20} {:<15} {:<20} {:<20}".format(
                "Pos.", "Producte", "Categoria", "Unitats venudes", "Facturació (s/IVA)", "Facturació (c/IVA)"))
            print("-"*120)
            
            for i, (producte, info) in enumerate(top3, 1):
                print("{:<5} {:<40} {:<20} {:<15} {:<20.2f}€ {:<20.2f}€".format(
                    i,
                    producte,
                    info['categoria'],
                    info['quantitat'],
                    info['facturacio_sense_iva'],
                    info['facturacio_amb_iva']
                ))
            
            print("="*120)
    
    except FileNotFoundError:
        print("Error: No s'ha trobat l'arxiu de dades 'datos.csv'")
    except Exception as e:
        print(f"Error inesperat: {str(e)}")

# Punt d'entrada del programa
if __name__ == "__main__":
    # Comprovar si l'arxiu de dades existeix
    try:
        with open('datos.csv', mode='r', encoding='utf-8') as file:
            # Lectura rápida para verificar que el archivo existe y es accesible
            pass
        mostrar_menu()
    except FileNotFoundError:
        print("\nError: No s'ha trobat l'arxiu de dades 'datos.csv'")
        print("Assegureu-vos que:")
        print("1. L'arxiu existeix al mateix directori que el programa")
        print("2. El nom de l'arxiu és exactament 'datos.csv' (sense extensions ocultes)")
        print("3. L'arxiu no està obert en un altre programa")
    except Exception as e:
        print(f"\nError inesperat: {str(e)}")