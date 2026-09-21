from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Oficina(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    direccion: str

    # Relación uno-a-muchos: una oficina tiene varias personas.
    # back_populates apunta al nombre del atributo en la clase Persona.
    personas: List["Persona"] = Relationship(back_populates="oficina")

class Persona(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    edad: int
    puesto: str
    
    # Clave foránea que conecta con el id de Oficina
    oficina_id: Optional[int] = Field(default=None, foreign_key="oficina.id")
    
    # Relación para navegar desde Persona hacia Oficina.
    # back_populates apunta al atributo "personas" en la clase Oficina.
    oficina: Optional[Oficina] = Relationship(back_populates="personas")