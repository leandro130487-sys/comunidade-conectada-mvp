
from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint("main", __name__)

ocorrencias = []

CATEGORIAS_PERMITIDAS = [
    "Iluminação pública",
    "Buracos nas ruas",
    "Descarte irregular de resíduos",
    "Limpeza urbana",
    "Manutenção de espaços públicos"
]


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        categoria = request.form.get("categoria", "").strip()
        descricao = request.form.get("descricao", "").strip()
        localizacao = request.form.get("localizacao", "").strip()

        if not categoria or not descricao or not localizacao:
            flash("Preencha todos os campos obrigatórios.", "erro")
            return redirect(url_for("main.registrar"))

        if categoria not in CATEGORIAS_PERMITIDAS:
            flash("Categoria inválida. Selecione uma opção permitida.", "erro")
            return redirect(url_for("main.registrar"))

        ocorrencia = {
            "id": len(ocorrencias) + 1,
            "categoria": categoria,
            "descricao": descricao,
            "localizacao": localizacao,
            "status": "Pendente"
        }

        ocorrencias.append(ocorrencia)

        flash("Ocorrência registrada com sucesso!", "sucesso")
        return redirect(url_for("main.consultar"))

    return render_template("registrar.html")


@main.route("/consultar")
def consultar():
    return render_template(
        "consultar.html",
        ocorrencias=ocorrencias
    )
