from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Armazenamento temporário de projetos
projects_data = {}

@app.route("/")
def index():
    return render_template("index.html", projects_data=projects_data)

@app.route("/gerenciamento/<int:project_id>")
def gerenciamento(project_id):
    # Recupera o projeto pelo ID; se não existir, redireciona para a página inicial
    project = projects_data.get(project_id)
    if not project:
        return redirect(url_for("index"))
    return render_template("gerenciamento.html", project=project)

@app.route("/criar_projeto", methods=["POST"])
def criar_projeto():
    project_name = request.form.get("project_name")
    if project_name:
        project_id = len(projects_data) + 1  # Gera um ID simples
        # Cria um novo projeto com o nome e uma lista vazia de colunas
        projects_data[project_id] = {
            "id": project_id,
            "name": project_name,
            "columns": []
        }
    return redirect(url_for("index"))

@app.route("/criar_coluna/<int:project_id>", methods=["POST"])
def criar_coluna(project_id):
    # Adiciona uma coluna vazia ao projeto
    project = projects_data.get(project_id)
    if project:
        column_id = len(project["columns"]) + 1
        project["columns"].append({
            "id": column_id,
            "name": f"Coluna {column_id}",
            "tasks": []
        })
    return '', 204  # Responde sem conteúdo para evitar recarregar a página

@app.route("/criar_tarefa/<int:project_id>/<int:column_id>", methods=["POST"])
def criar_tarefa(project_id, column_id):
    # Adiciona uma tarefa a uma coluna específica do projeto
    project = projects_data.get(project_id)
    if project:
        column = next((col for col in project["columns"] if col["id"] == column_id), None)
        if column:
            task_name = request.form.get("task_name")
            if task_name:
                column["tasks"].append(task_name)
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
