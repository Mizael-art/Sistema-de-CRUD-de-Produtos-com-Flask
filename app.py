from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

# Caminho do arquivo JSON com os produtos
ARQUIVO = "produtos.json"


# -------------------------------------------------------
# Função auxiliar: carrega os produtos do JSON
# -------------------------------------------------------
def carregar_produtos():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except:
        return []


# -------------------------------------------------------
# Função auxiliar: salva a lista de produtos no JSON
# -------------------------------------------------------
def salvar_produtos(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)


# -------------------------------------------------------
# ROTA: Menu principal
# -------------------------------------------------------
@app.route("/")
def home():
    return render_template("menu.html")


# -------------------------------------------------------
# ROTA: Listar todos os produtos
# -------------------------------------------------------
@app.route("/produtos")
def produtos():
    dados = carregar_produtos()
    return render_template("produtos.html", produtos=dados)


# -------------------------------------------------------
# ROTA: Cadastrar produto (GET mostra form, POST salva)
# -------------------------------------------------------
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():

    if request.method == "POST":
        # TODO: pegar os campos do formulário
        nome = request.form["nome"]
        preco = float(request.form["preco"])
        categoria = request.form["categoria"]

        # TODO: criar o dicionário do produto
        produto = {
            "nome": nome,
            "preco": preco,
            "categoria": categoria
        }

        # TODO: carregar lista atual, adicionar e salvar
        dados = carregar_produtos()
        dados.append(produto)
        salvar_produtos(dados)

        # Passa sucesso=True para o template exibir a mensagem verde
        return render_template("cadastrar.html", sucesso=True)

    return render_template("cadastrar.html")


# -------------------------------------------------------
# ROTA: Listar produtos para escolher qual editar
# -------------------------------------------------------
@app.route("/editar")
def editar():
    dados = carregar_produtos()
    return render_template("editar.html", produtos=dados)


# -------------------------------------------------------
# ROTA: Editar um produto específico pelo índice
# -------------------------------------------------------
@app.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar_produto(indice):
    dados = carregar_produtos()
    produto = dados[indice]  # pega o produto pelo índice

    if request.method == "POST":
        # TODO: ler os novos dados do formulário
        dados[indice]["nome"]      = request.form["nome"]
        dados[indice]["preco"]     = float(request.form["preco"])
        dados[indice]["categoria"] = request.form["categoria"]

        # TODO: salvar e redirecionar
        salvar_produtos(dados)
        return redirect("/editar")

    return render_template("editar_produto.html", produto=produto, indice=indice)


# -------------------------------------------------------
# ROTA: Excluir um produto pelo índice
# -------------------------------------------------------
@app.route("/excluir/<int:indice>")
def excluir(indice):
    dados = carregar_produtos()

    # TODO: remover o produto e salvar
    dados.pop(indice)
    salvar_produtos(dados)

    return redirect("/editar")


# -------------------------------------------------------

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
