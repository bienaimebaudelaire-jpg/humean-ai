# HUMEAN - Advanced Cognitive AI System

> **HUMEAN** = IA × Humanité with verifiable guarantees (charters, policies, attestations)

HUMEAN is a modular, ethically-grounded cognitive AI system based on the Free Energy Principle. It provides verifiable decision-making with built-in ethical constraints and digital attestations.

## ✨ Features

- **🧠 Modular Architecture** - Five independent cognitive modules (Gateway, Memory, Scheduler, Ethics, Monitoring)
- **🔄 Intelligent Fallbacks** - Primary engine (Gemini) with local (Ollama) and cloud (HuggingFace) alternatives
- **🔐 Verifiable Decisions** - Digital signatures and audit trails for all decisions
- **⚡ Production-Ready** - Type-safe Python, comprehensive tests, CI/CD pipelines
- **🌍 Free Energy Principle** - Grounded in theoretical neuroscience foundations

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git
- API keys (optional): Gemini, HuggingFace

### Installation

```bash
# Clone the repository
git clone https://github.com/bienaimebaudelaire-jpg/humean-ai.git
cd humean-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Fill in your API keys in `.env`:
```env
GEMINI_API_KEY=your_api_key_here
HUMEAN_MODE=development
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest --cov=modules
```

### Code Quality

```bash
black modules tests      # Format code
ruff check modules tests # Lint
mypy modules             # Type checking
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🏗️ Architecture

| Module | Status | Purpose |
|--------|--------|---------|
| **Gateway** | Operational | API interface and request routing |
| **Memory** | Operational | Context and episodic memory management |
| **Scheduler** | Ready | Task scheduling and prioritization |
| **Ethics** | Ready | Ethical constraints and policy enforcement |
| **Monitoring** | Operational | System health and performance metrics |

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full architecture details.

## 📋 Project Structure

```
humean-ai/
├── modules/humean_core/       # Core cognitive system
├── tests/                      # Test suite
├── docs/                       # Documentation
├── .github/workflows/          # CI/CD pipelines
├── pyproject.toml             # Project configuration
└── README.md
```

## 📄 License

AGPL-3.0 - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔗 Links

- 📖 [Documentation](docs/)
- 🐛 [Issues](https://github.com/bienaimebaudelaire-jpg/humean-ai/issues)
- 💬 [Discussions](https://github.com/bienaimebaudelaire-jpg/humean-ai/discussions)

---

**Made with ❤️ for human-centered AI**
