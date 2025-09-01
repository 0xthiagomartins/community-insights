import typer
from commands import setup_project, list_projects, estimate_cost, generate_summary, update_project

app = typer.Typer(
    name="neural-core",
    help="🤖 Neural Core - AI-powered crypto community insights",
    add_completion=False
)

# Add commands
app.command(name="setup-project")(setup_project)
app.command(name="list-projects")(list_projects)
app.command(name="estimate-cost")(estimate_cost)
app.command(name="generate-summary")(generate_summary)
app.command(name="update-project")(update_project)

if __name__ == "__main__":
    app()
