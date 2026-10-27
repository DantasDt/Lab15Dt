from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy import select, func, desc
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///escolaDt.db')

Base = declarative_base()

matriculas = Table('matriculas', Base.metadata,
                    Column('aluno_id', Integer, ForeignKey('alunos.idAluno'), primary_key=True),
                    Column('disciplina_id', Integer, ForeignKey('disciplinas.idDisciplina'), primary_key=True))

class Curso(Base):
    __tablename__ = 'cursos'
    idCurso = Column(Integer, primary_key=True)
    nome = Column(String)

    alunos = relationship('Aluno', back_populates='curso')

    def __repr__(self):
        return f"Curso({self.idCurso}, {self.nome!r})"

class Aluno(Base):
    __tablename__ = 'alunos'
    idAluno = Column(Integer, primary_key=True)
    nome = Column(String)
    curso_id = Column(Integer, ForeignKey('cursos.idCurso'))

    curso = relationship('Curso', back_populates='alunos')

    disciplinas = relationship('Disciplina', secondary= matriculas, back_populates='alunos')

    def __repr__(self):
        return f"Aluno({self.idAluno}, {self.nome!r})"


class Disciplina(Base):
    __tablename__ = 'disciplinas'
    idDisciplina = Column(Integer, primary_key=True)
    nome = Column(String)

    alunos = relationship('Aluno', secondary= matriculas, back_populates='disciplinas')

    def __repr__(self):
        return f"Disciplina({self.idDisciplina}, {self.nome!r})"


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


informatica = Curso(nome='Informática')
eletronica = Curso(nome='Eletrônica')


banco = Disciplina(nome='Banco de Dados')
programacao = Disciplina(nome='Programação')
circuitos = Disciplina(nome='Circuitos')
matematica = Disciplina(nome='Matemática')

Dantastico = Aluno(nome='Dantas', curso = informatica, disciplinas = [banco, programacao, matematica])

Patapa = Aluno(nome='LuanGoat', curso = informatica, disciplinas = [programacao, matematica])

Luiz = Aluno(nome='Mico', curso = eletronica, disciplinas=[circuitos, matematica])

Calazans = Aluno(nome='Calazans', curso = eletronica, disciplinas = [circuitos])

Coimbra = Aluno(nome='Coimbra', curso = informatica, disciplinas = [banco, programacao, matematica])

session.add_all([Dantastico, Patapa, Luiz, Calazans, Coimbra])
session.commit()

print('\na) Alunos e seus cursos')

query = (select(Aluno.nome, Curso.nome)
        .join(Aluno.curso)
        .order_by(Aluno.nome))

for aluno, curso in session.execute(query):
    print(aluno, '-', curso)

print('\nb) Alunos matriculados em Banco de Dados')
query = (select(Aluno.nome)
        .join(Aluno.disciplinas)
        .where(Disciplina.nome == 'Banco de Dados')
        .order_by(Aluno.nome))

for linha in session.execute(query):
    print(linha.nome)

print('\nc) Quantidade de alunos por disciplina')
query = (select(Disciplina.nome, func.count(Aluno.idAluno))
        .join(Disciplina.alunos)
        .group_by(Disciplina.idDisciplina, Disciplina.nome)
        .order_by(desc(func.count(Aluno.idAluno)), Disciplina.nome))

for disciplina, quantidade in session.execute(query):
    print(disciplina, '-', quantidade, 'alunos')

session.close()
