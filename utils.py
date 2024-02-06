import hashlib
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz     # PyMuPDF
import shutil, os


def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def comparar_senhas(hash_senha, senha_usuario):
    if hash_senha == hashlib.sha256(senha_usuario.encode()).hexdigest():
        return True
    else:
        return False

def Similaridade(text1, text2):
    # Converte os texto para vetores TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])

    # Calcula a similaridade do cosseno dos dois vetores
    similarity = cosine_similarity(vectors)
    return similarity[0][1]
    

def converte_pdf_em_imagens(doc, mat, path):
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        pix.save(f'{path}/page-{page.number}.png')  # store image as a PNG


def lista_cursos_periodos(doc):
    lista_turmas = list()
    for page in doc:
        text = page.get_text()
        linhas = text.splitlines()

        for frase in linhas:
            if 'Computação' in frase and 'período' in frase:
                lista_turmas.append(frase)
            elif 'Controle' in frase and 'período' in frase:
                lista_turmas.append(frase)
            elif 'Hídrica' in frase and 'período' in frase:
                lista_turmas.append(frase)
            elif 'Química' in frase and 'período' in frase:
                lista_turmas.append(frase)
            else:
                pass
    return lista_turmas


def get_periodo(turma):
    periodo = None
    for i in turma:
        try:
            periodo = int(i)
        except:
            pass
    return periodo


def deleta_arquivos(dir):
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


def renomeia_arquivos(turmas, path):
    for i in range(len(turmas)):
        old_file = f'{path}/page-{i}.png'
        filename = 'horario'

        if 'Computação' in turmas[i]:
            filename += '_eng_computacao'
        elif 'Controle' in turmas[i]:
            filename += '_eng_controle_automacao'
        elif 'Hídrica' in turmas[i]:
            filename += '_eng_hidrica'
        elif 'Química' in turmas[i]:
            filename += '_eng_quimica'
        else:
            pass

        periodo = get_periodo(turmas[i])
        filename += f'_{periodo}_periodo'

        new_file = f'{path}/{filename}.png'
        
        shutil.move(old_file, new_file)


def gerar_horarios(pdf, path):
    doc = fitz.open(pdf)

    deleta_arquivos(f'./{path}')

    turmas = lista_cursos_periodos(doc)

    zoom_x = 2.0
    zoom_y = 2.0
    mat = fitz.Matrix(zoom_x, zoom_y)
    converte_pdf_em_imagens(doc, mat, path)

    renomeia_arquivos(turmas, path)
