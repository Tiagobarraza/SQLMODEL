from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Oficina, Persona

def create_datos():
    with Session(engine) as session:
        # Alta de oficinas
        ofi_norte = Oficina(nombre="Sede Norte", direccion="Av. Rafael Nuñez 100")
        ofi_centro = Oficina(nombre="Sede Centro", direccion="Av. Colón 200")
        
        # Alta de personas, asociadas a una oficina a través del atributo de relación
        persona1 = Persona(nombre="Tiago", edad=21, puesto="Desarrollador", oficina=ofi_norte)
        persona2 = Persona(nombre="Martina", edad=26, puesto="Analista", oficina=ofi_norte)
        persona3 = Persona(nombre="Carlos", edad=40, puesto="Soporte", oficina=ofi_centro)
        
        # Al añadir las personas, SQLModel automáticamente añade las oficinas asociadas
        session.add(persona1)
        session.add(persona2)
        session.add(persona3)
        session.commit()

def read_datos():
    with Session(engine) as session:
        # Listado navegando la relación oficina.personas
        print("\n--- Personas en Sede Norte ---")
        statement = select(Oficina).where(Oficina.nombre == "Sede Norte")
        oficina = session.exec(statement).first()
        if oficina:
            for p in oficina.personas:
                print(f"- {p.nombre} ({p.puesto})")

        # Consulta con JOIN y filtro WHERE sobre un campo numérico (edad)
        print("\n--- Empleados menores de 30 años (Con JOIN) ---")
        statement_join = select(Persona, Oficina).join(Oficina).where(Persona.edad < 30)
        resultados = session.exec(statement_join).all()
        for persona, ofi in resultados:
            print(f"- {persona.nombre} trabaja en {ofi.nombre}")

def update_datos():
    with Session(engine) as session:
        # Reasignar una persona a otra oficina
        statement_persona = select(Persona).where(Persona.nombre == "Tiago")
        tiago = session.exec(statement_persona).first()
        
        statement_oficina = select(Oficina).where(Oficina.nombre == "Sede Centro")
        nueva_oficina = session.exec(statement_oficina).first()
        
        if tiago and nueva_oficina:
            tiago.oficina = nueva_oficina
            session.add(tiago)
            session.commit()
            print("\n--- Tiago fue reasignado a Sede Centro ---")

def delete_datos():
    with Session(engine) as session:
        # Eliminar una persona
        statement = select(Persona).where(Persona.nombre == "Carlos")
        carlos = session.exec(statement).first()
        
        if carlos:
            session.delete(carlos)
            session.commit()
            print("\n--- Carlos fue eliminado del sistema ---")

def main():
    create_db_and_tables()
    create_datos()
    read_datos()
    update_datos()
    delete_datos()

if __name__ == "__main__":
    main()