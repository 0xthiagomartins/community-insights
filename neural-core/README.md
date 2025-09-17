# Neural Core - Windows Setup Guide

## 🚀 Quick Start (Windows + Poetry)

### Prerequisites
- Python 3.11+
- Scoop package manager
- Pipx
- Poetry

### Installation Steps

1. **Install Scoop** (if not already installed):
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

2. **Install Pipx via Scoop**:
```powershell
scoop install pipx
pipx ensurepath
```

3. **Install Poetry via Pipx**:
```powershell
pipx install poetry
pipx ensurepath
```

4. **Verify installations**:
```powershell
scoop --version
python --version
pipx --version
poetry --version
```

5. **Setup Neural Core**:
```bash
cd neural-core
poetry install --no-root
poetry shell
```

6. **Configure environment**:
```bash
cp env.example .env
# Edit .env with your OpenAI API key
```

7. **Test the CLI**:
```bash
python src/main.py --help
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_ORGANIZATION_ID`: Your OpenAI organization ID (optional)
- `DATABASE_URL`: Path to shared SQLite database
- `CREWAI_VERBOSE`: Enable verbose CrewAI output (true/false)
- `CREWAI_MEMORY`: Enable CrewAI memory (true/false)

### OpenAI API Setup
1. Go to [OpenAI Platform](https://platform.openai.com/account/organization)
2. Verify your account and add funds
3. Create a new API key
4. Add the key to your `.env` file

## 🎯 Usage

### Available Commands
- `setup-project`: Create a new project
- `list-projects`: List all projects
- `estimate-cost`: Estimate processing cost
- `generate-summary`: Generate AI summary
- `update-project`: Update project settings

### Example Workflow
```bash
# Create a project
python src/main.py setup-project "My Project" "telegram_group_id"

# List projects
python src/main.py list-projects

# Estimate cost for last 7 days
python src/main.py estimate-cost "My Project" --days 7

# Generate summary
python src/main.py generate-summary "My Project" --days 7
```

## 🐛 Troubleshooting

### Common Issues
1. **Poetry not found**: Make sure `pipx ensurepath` was run and restart your terminal
2. **OpenAI API errors**: Verify your API key and account has sufficient credits
3. **Database errors**: Ensure Oracle Eye is running and database exists

### Windows-Specific Notes
- Use PowerShell for Scoop installation
- Poetry shell creates a virtual environment automatically
- CrewAI works better with Poetry on Windows than pip

## 📁 Project Structure
```
neural-core/
├── src/
│   ├── cli/           # CLI interface
│   ├── models/        # Database models
│   ├── services/      # Core services
│   └── utils/         # Utilities
├── pyproject.toml     # Poetry configuration
└── env.example        # Environment template
```