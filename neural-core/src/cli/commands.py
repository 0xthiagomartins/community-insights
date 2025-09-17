import typer
from typing import Optional
from datetime import datetime, timedelta
from services.database import DatabaseManager
from services.ai_processor import AIProcessor

app = typer.Typer()
db = DatabaseManager()
ai_processor = AIProcessor()

@app.command()
def setup_project(
    name: str = typer.Option(..., "--name", "-n", help="Project name"),
    group: str = typer.Option(..., "--group", "-g", help="Telegram group/channel"),
    active: bool = typer.Option(True, "--active", "-a", help="Set project as active")
):
    """Setup a new project for monitoring"""
    try:
        project = db.create_project(name=name, telegram_group=group, is_active=active)
        typer.echo(f"Project '{project.name}' setup successfully!")
        typer.echo(f"Monitoring group: {project.telegram_group}")
        typer.echo(f"Status: {'Active' if project.is_active else 'Inactive'}")
    except Exception as e:
        typer.echo(f"Error setting up project: {e}")
        raise typer.Exit(1)

@app.command()
def list_projects():
    """List all configured projects"""
    try:
        projects = db.get_all_projects()
        if not projects:
            typer.echo("No projects configured yet")
            return
        
        typer.echo("Configured Projects:")
        for project in projects:
            status = "Active" if project.is_active else "Inactive"
            typer.echo(f"  • {project.name} ({project.telegram_group}) - {status}")
    except Exception as e:
        typer.echo(f"Error listing projects: {e}")
        raise typer.Exit(1)

@app.command()
def estimate_cost(
    project_name: str = typer.Option(..., "--project", "-p", help="Project name"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to summarize")
):
    """Estimate the cost of generating a summary"""
    try:
        project = db.get_project_by_name(project_name)
        if not project:
            typer.echo(f" Project '{project_name}' not found")
            raise typer.Exit(1)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        cost_estimate = ai_processor.estimate_cost(project, start_date, end_date)
        
        typer.echo(f" Cost Estimate for '{project_name}' ({days} days):")
        typer.echo(f"  • Total Cost: ${cost_estimate.total_cost:.2f}")
        typer.echo(f"  • Message Count: {cost_estimate.message_count}")
        typer.echo(f"  • Cost per Message: ${cost_estimate.cost_per_message:.4f}")
        
    except Exception as e:
        typer.echo(f" Error estimating cost: {e}")
        raise typer.Exit(1)

@app.command()
def generate_summary(
    project_name: str = typer.Option(..., "--project", "-p", help="Project name"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to summarize"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path")
):
    """Generate a summary for the specified project and date range"""
    try:
        project = db.get_project_by_name(project_name)
        if not project:
            typer.echo(f" Project '{project_name}' not found")
            raise typer.Exit(1)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        typer.echo(f" Generating summary for '{project_name}' ({days} days)...")
        summary = ai_processor.generate_summary(project, start_date, end_date)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(summary.content)
            typer.echo(f" Summary saved to: {output_file}")
        else:
            typer.echo("\n" + "="*50)
            typer.echo(" SUMMARY")
            typer.echo("="*50)
            typer.echo(summary.content)
            typer.echo("="*50)
        
        typer.echo(f" Actual Cost: ${summary.actual_cost:.2f}")
        
    except Exception as e:
        typer.echo(f" Error generating summary: {e}")
        raise typer.Exit(1)

@app.command()
def collect_now(
    project_name: str = typer.Option(..., "--project", "-p", help="Project name")
):
    """Request immediate message collection (Oracle Eye will process)"""
    try:
        project = db.get_project_by_name(project_name)
        if not project:
            typer.echo(f"Project '{project_name}' not found")
            raise typer.Exit(1)
        
        # Create command file for Oracle Eye
        import json
        from datetime import datetime
        from pathlib import Path
        
        commands_dir = Path("../shared/commands")
        commands_dir.mkdir(parents=True, exist_ok=True)
        
        command_file = commands_dir / f"collect_{project_name.lower()}.json"
        
        command_data = {
            "command": "collect",
            "project_name": project_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "pending"
        }
        
        with open(command_file, 'w') as f:
            json.dump(command_data, f, indent=2)
        
        typer.echo(f"Collection request sent for '{project_name}'")
        typer.echo(f"Oracle Eye will process this request shortly...")
        typer.echo(f"Use 'check-status --project {project_name}' to monitor progress")
        
    except Exception as e:
        typer.echo(f"Error requesting collection: {e}")
        raise typer.Exit(1)

@app.command()
def check_status(
    project_name: str = typer.Option(..., "--project", "-p", help="Project name")
):
    """Check the status of a collection request"""
    try:
        from pathlib import Path
        import json
        
        commands_dir = Path("../shared/commands")
        status_file = commands_dir / f"status_{project_name.lower()}.json"
        
        if not status_file.exists():
            typer.echo(f"No status found for '{project_name}'")
            return
        
        with open(status_file, 'r') as f:
            status_data = json.load(f)
        
        typer.echo(f"Status for '{project_name}':")
        typer.echo(f"  Status: {status_data.get('status', 'unknown')}")
        typer.echo(f"  Messages collected: {status_data.get('messages_collected', 0)}")
        typer.echo(f"  Last update: {status_data.get('timestamp', 'unknown')}")
        
    except Exception as e:
        typer.echo(f"Error checking status: {e}")
        raise typer.Exit(1)

@app.command()
def update_project(
    project_name: str = typer.Option(..., "--project", "-p", help="Project name"),
    new_name: Optional[str] = typer.Option(None, "--new-name", help="New project name"),
    new_group: Optional[str] = typer.Option(None, "--new-group", help="New Telegram group"),
    active: Optional[bool] = typer.Option(None, "--active", help="Set active status")
):
    """Update project configuration"""
    try:
        project = db.get_project_by_name(project_name)
        if not project:
            typer.echo(f" Project '{project_name}' not found")
            raise typer.Exit(1)
        
        update_data = {}
        if new_name:
            update_data["name"] = new_name
        if new_group:
            update_data["telegram_group"] = new_group
        if active is not None:
            update_data["is_active"] = active
        
        if not update_data:
            typer.echo(" No updates specified")
            raise typer.Exit(1)
        
        updated_project = db.update_project(project.id, **update_data)
        typer.echo(f" Project '{project_name}' updated successfully!")
        
        if new_name:
            typer.echo(f" New name: {updated_project.name}")
        if new_group:
            typer.echo(f" New group: {updated_project.telegram_group}")
        if active is not None:
            typer.echo(f" New status: {'Active' if updated_project.is_active else 'Inactive'}")
            
    except Exception as e:
        typer.echo(f" Error updating project: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
