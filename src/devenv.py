#!/usr/bin/env python3
"""
DevEnv-Setup - One-Click Development Environment Setup Tool
Copyright (c) 2026 KEBANJILONG
Licensed under the MIT License.
"""

import sys
import os
import json
import platform
import subprocess
import shutil
import argparse
import datetime
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

VERSION = "1.0.0"
AUTHOR = "KEBANJILONG"
REPO_URL = "https://github.com/KEBANJILONG/DevEnv-Setup"

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    # Windows support
    @classmethod
    def enable_windows(cls):
        if platform.system() == "Windows":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except Exception:
                pass

Colors.enable_windows()


def print_banner():
    """Print the DevEnv-Setup banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
  ╔═══════════════════════════════════════════════════════╗
  ║                                                       ║
  ║   🚀 DevEnv-Setup v{VERSION}                          ║
  ║   One-Click Development Environment Setup Tool        ║
  ║                                                       ║
  ║   by {AUTHOR}                                        ║
  ║                                                       ║
  ╚═══════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)


def print_status(icon: str, message: str, color: str = Colors.WHITE):
    """Print a formatted status message."""
    print(f"  {color}{icon}{Colors.RESET} {message}")


def print_success(message: str):
    print_status("✅", message, Colors.GREEN)


def print_error(message: str):
    print_status("❌", message, Colors.RED)


def print_warning(message: str):
    print_status("⚠️", message, Colors.YELLOW)


def print_info(message: str):
    print_status("ℹ️", message, Colors.BLUE)


def print_progress(message: str):
    print_status("⏳", message, Colors.YELLOW)


# ============================================================
# Tool definitions
# ============================================================

TOOL_DEFINITIONS = {
    "nodejs": {
        "name": "Node.js",
        "check_cmd": ["node", "--version"],
        "install": {
            "windows": "winget install OpenJS.NodeJS.LTS",
            "macos": "brew install node@20",
            "linux": "curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs"
        },
        "version_cmd": ["node", "--version"],
        "category": "language"
    },
    "python": {
        "name": "Python",
        "check_cmd": ["python", "--version"],
        "install": {
            "windows": "winget install Python.Python.3.11",
            "macos": "brew install python@3.11",
            "linux": "sudo apt-get install -y python3.11 python3.11-venv python3-pip"
        },
        "version_cmd": ["python", "--version"],
        "category": "language"
    },
    "go": {
        "name": "Go",
        "check_cmd": ["go", "version"],
        "install": {
            "windows": "winget install GoLang.Go",
            "macos": "brew install go",
            "linux": "sudo snap install go --classic"
        },
        "version_cmd": ["go", "version"],
        "category": "language"
    },
    "rust": {
        "name": "Rust",
        "check_cmd": ["rustc", "--version"],
        "install": {
            "windows": "winget install Rustlang.Rustup",
            "macos": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
            "linux": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
        },
        "version_cmd": ["rustc", "--version"],
        "category": "language"
    },
    "git": {
        "name": "Git",
        "check_cmd": ["git", "--version"],
        "install": {
            "windows": "winget install Git.Git",
            "macos": "brew install git",
            "linux": "sudo apt-get install -y git"
        },
        "version_cmd": ["git", "--version"],
        "category": "vcs"
    },
    "docker": {
        "name": "Docker",
        "check_cmd": ["docker", "--version"],
        "install": {
            "windows": "winget install Docker.DockerDesktop",
            "macos": "brew install --cask docker",
            "linux": "curl -fsSL https://get.docker.com | sh"
        },
        "version_cmd": ["docker", "--version"],
        "category": "container"
    },
    "vscode": {
        "name": "VS Code",
        "check_cmd": ["code", "--version"],
        "install": {
            "windows": "winget install Microsoft.VisualStudioCode",
            "macos": "brew install --cask visual-studio-code",
            "linux": "sudo snap install code --classic"
        },
        "version_cmd": ["code", "--version"],
        "category": "editor"
    },
    "mysql": {
        "name": "MySQL",
        "check_cmd": ["mysql", "--version"],
        "install": {
            "windows": "winget install Oracle.MySQL",
            "macos": "brew install mysql",
            "linux": "sudo apt-get install -y mysql-server"
        },
        "version_cmd": ["mysql", "--version"],
        "category": "database"
    },
    "redis": {
        "name": "Redis",
        "check_cmd": ["redis-server", "--version"],
        "install": {
            "windows": "winget install Redis.Redis",
            "macos": "brew install redis",
            "linux": "sudo apt-get install -y redis-server"
        },
        "version_cmd": ["redis-server", "--version"],
        "category": "database"
    }
}

# Tool presets
PRESETS = {
    "web-frontend": {
        "description": "Frontend Web Development",
        "tools": ["nodejs", "git", "vscode"]
    },
    "web-full": {
        "description": "Full-Stack Web Development",
        "tools": ["nodejs", "python", "git", "docker", "vscode", "redis", "mysql"]
    },
    "backend-python": {
        "description": "Python Backend Development",
        "tools": ["python", "git", "docker", "vscode", "redis", "mysql"]
    },
    "backend-go": {
        "description": "Go Backend Development",
        "tools": ["go", "git", "docker", "vscode", "redis", "mysql"]
    },
    "backend-rust": {
        "description": "Rust Backend Development",
        "tools": ["rust", "git", "docker", "vscode", "redis"]
    },
    "devops": {
        "description": "DevOps / Infrastructure",
        "tools": ["python", "go", "git", "docker", "vscode"]
    },
    "mobile": {
        "description": "Mobile App Development",
        "tools": ["nodejs", "git", "vscode"]
    }
}

# VS Code extensions by category
VSCODE_EXTENSIONS = {
    "general": [
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint",
        "eamodio.gitlens",
        "ms-vscode-remote.remote-wsl",
        "christian-kohler.path-intellisense",
        "streetsidesoftware.code-spell-checker",
        "gruntfuggly.todo-tree",
        "PKief.material-icon-theme"
    ],
    "python": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff"
    ],
    "web": [
        "bradlc.vscode-tailwindcss",
        "prisma.prisma",
        "antfu.vite",
        "Vue.volar"
    ],
    "go": [
        "golang.Go"
    ],
    "rust": [
        "rust-lang.rust-analyzer",
        "vadimcn.vscode-lldb",
        "serayuzgur.crates"
    ],
    "docker": [
        "ms-azuretools.vscode-docker",
        "ms-vscode-remote.remote-containers"
    ]
}

# Project templates
PROJECT_TEMPLATES = {
    "react": {
        "description": "React + Vite + TypeScript",
        "command": "npm create vite@latest {name} -- --template react-ts",
        "post_commands": ["cd {name}", "npm install"]
    },
    "vue": {
        "description": "Vue 3 + Vite + TypeScript",
        "command": "npm create vue@latest {name}",
        "post_commands": ["cd {name}", "npm install"]
    },
    "next": {
        "description": "Next.js + TypeScript",
        "command": "npx create-next-app@latest {name} --typescript --tailwind --eslint --app",
        "post_commands": []
    },
    "express": {
        "description": "Express + TypeScript",
        "command": None,  # Custom template
        "post_commands": []
    },
    "fastapi": {
        "description": "FastAPI + Python",
        "command": None,  # Custom template
        "post_commands": []
    },
    "django": {
        "description": "Django + Python",
        "command": "django-admin startproject {name}",
        "post_commands": []
    }
}


class DevEnvSetup:
    """Main DevEnv-Setup class."""

    def __init__(self):
        self.os_type = platform.system().lower()
        self.home = Path.home()
        self.config_dir = self.home / ".devenv"
        self.config_file = self.config_dir / "config.json"
        self.backup_dir = self.config_dir / "backups"

    # --------------------------------------------------------
    # Environment check
    # --------------------------------------------------------
    def check_environment(self) -> Dict[str, dict]:
        """Check installed development tools."""
        print(f"\n{Colors.BOLD}🔍 Checking development environment...{Colors.RESET}\n")

        results = {}
        for tool_id, tool_info in TOOL_DEFINITIONS.items():
            installed, version = self._check_tool(tool_info)
            results[tool_id] = {
                "name": tool_info["name"],
                "installed": installed,
                "version": version,
                "category": tool_info["category"]
            }

        return results

    def _check_tool(self, tool_info: dict) -> Tuple[bool, str]:
        """Check if a single tool is installed."""
        try:
            result = subprocess.run(
                tool_info["check_cmd"],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if self.os_type == "windows" else 0
            )
            if result.returncode == 0:
                version = result.stdout.strip().split("\n")[0]
                return True, version
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass
        return False, ""

    def display_dashboard(self, results: Dict[str, dict]):
        """Display environment status dashboard."""
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════╗")
        print(f"║           🖥️  Development Environment Status             ║")
        print(f"╠═══════════════════════════════════════════════════════════╣{Colors.RESET}")

        categories = {}
        for tool_id, info in results.items():
            cat = info["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((tool_id, info))

        category_names = {
            "language": "Languages",
            "vcs": "Version Control",
            "container": "Containers",
            "editor": "Editors",
            "database": "Databases"
        }

        installed_count = 0
        total_count = len(results)

        for cat, tools in categories.items():
            cat_name = category_names.get(cat, cat.title())
            print(f"{Colors.BOLD}  [{cat_name}]{Colors.RESET}")
            for tool_id, info in tools:
                if info["installed"]:
                    print(f"  {Colors.GREEN}  ✅ {info['name']:<14} {info['version']}{Colors.RESET}")
                    installed_count += 1
                else:
                    print(f"  {Colors.RED}  ❌ {info['name']:<14} Not installed{Colors.RESET}")
            print()

        health = "🟢 Healthy" if installed_count >= total_count * 0.7 else "🟡 Needs Setup" if installed_count >= total_count * 0.3 else "🔴 Needs Installation"
        print(f"{Colors.CYAN}{Colors.BOLD}╠═══════════════════════════════════════════════════════════╣")
        print(f"║  Environment  {health}  ({installed_count}/{total_count} installed){Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚═══════════════════════════════════════════════════════════╝{Colors.RESET}\n")

    # --------------------------------------------------------
    # Tool installation
    # --------------------------------------------------------
    def install_tool(self, tool_id: str, version: Optional[str] = None):
        """Install a development tool."""
        if tool_id not in TOOL_DEFINITIONS:
            print_error(f"Unknown tool: {tool_id}")
            print_info(f"Available tools: {', '.join(TOOL_DEFINITIONS.keys())}")
            return

        tool = TOOL_DEFINITIONS[tool_id]
        installed, current_version = self._check_tool(tool)

        if installed:
            print_warning(f"{tool['name']} is already installed ({current_version})")
            return

        os_key = self.os_type
        if os_key == "darwin":
            os_key = "macos"

        install_cmd = tool["install"].get(os_key)
        if not install_cmd:
            print_error(f"Installation not supported for {self.os_type}")
            return

        print_progress(f"Installing {tool['name']}...")
        print_info(f"Command: {install_cmd}")

        try:
            if self.os_type == "windows":
                result = subprocess.run(
                    install_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=600
                )
            else:
                result = subprocess.run(
                    install_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=600
                )

            if result.returncode == 0:
                print_success(f"{tool['name']} installed successfully!")
            else:
                print_error(f"Failed to install {tool['name']}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            print_error(f"Installation timed out for {tool['name']}")

    def install_preset(self, preset_name: str):
        """Install a preset group of tools."""
        if preset_name not in PRESETS:
            print_error(f"Unknown preset: {preset_name}")
            print_info(f"Available presets: {', '.join(PRESETS.keys())}")
            return

        preset = PRESETS[preset_name]
        print(f"\n{Colors.BOLD}📦 Installing preset: {preset_name} - {preset['description']}{Colors.RESET}\n")

        for tool_id in preset["tools"]:
            self.install_tool(tool_id)
            print()

    # --------------------------------------------------------
    # VS Code extension management
    # --------------------------------------------------------
    def install_vscode_extensions(self, category: str = "general"):
        """Install VS Code extensions by category."""
        if category not in VSCODE_EXTENSIONS:
            print_error(f"Unknown category: {category}")
            print_info(f"Available: {', '.join(VSCODE_EXTENSIONS.keys())}")
            return

        extensions = VSCODE_EXTENSIONS[category]
        print(f"\n{Colors.BOLD}🧩 Installing VS Code extensions [{category}]{Colors.RESET}\n")

        for ext in extensions:
            print_progress(f"Installing {ext}...")
            try:
                result = subprocess.run(
                    ["code", "--install-extension", ext],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    creationflags=subprocess.CREATE_NO_WINDOW if self.os_type == "windows" else 0
                )
                if result.returncode == 0:
                    print_success(f"Installed {ext}")
                else:
                    print_warning(f"Failed to install {ext}")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                print_error(f"VS Code CLI not found. Is VS Code installed?")

    # --------------------------------------------------------
    # Configuration management
    # --------------------------------------------------------
    def config_git(self, name: str, email: str):
        """Configure Git user information."""
        print_progress("Configuring Git...")

        commands = [
            ["git", "config", "--global", "user.name", name],
            ["git", "config", "--global", "user.email", email],
            ["git", "config", "--global", "init.defaultBranch", "main"],
            ["git", "config", "--global", "core.autocrlf", "input" if self.os_type != "windows" else "auto"],
        ]

        for cmd in commands:
            try:
                subprocess.run(cmd, capture_output=True, timeout=10,
                             creationflags=subprocess.CREATE_NO_WINDOW if self.os_type == "windows" else 0)
            except (FileNotFoundError, subprocess.TimeoutExpired):
                print_warning(f"Failed: {' '.join(cmd)}")

        print_success(f"Git configured: {name} <{email}>")

    def backup_config(self, output_path: Optional[str] = None):
        """Backup development environment configuration."""
        if output_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = str(self.backup_dir / f"devenv-backup-{timestamp}.json")

        self.backup_dir.mkdir(parents=True, exist_ok=True)

        backup_data = {
            "version": VERSION,
            "timestamp": datetime.datetime.now().isoformat(),
            "platform": platform.platform(),
            "tools": {},
            "git_config": {},
            "env_vars": {}
        }

        # Check tools
        for tool_id, tool_info in TOOL_DEFINITIONS.items():
            installed, version = self._check_tool(tool_info)
            backup_data["tools"][tool_id] = {
                "installed": installed,
                "version": version
            }

        # Git config
        try:
            result = subprocess.run(
                ["git", "config", "--global", "--list"],
                capture_output=True, text=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if self.os_type == "windows" else 0
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        backup_data["git_config"][key] = value
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Important env vars
        important_vars = [
            "PATH", "HOME", "JAVA_HOME", "GOPATH", "GOROOT",
            "NODE_PATH", "PYTHONPATH", "CARGO_HOME", "RUSTUP_HOME",
            "NVM_DIR", "PYENV_ROOT", "CONDA_PREFIX"
        ]
        for var in important_vars:
            value = os.environ.get(var)
            if value:
                backup_data["env_vars"][var] = value

        # Write backup
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)

        print_success(f"Backup saved to: {output_file}")
        print_info(f"Tools: {sum(1 for t in backup_data['tools'].values() if t['installed'])} installed")

    def restore_config(self, input_path: str):
        """Restore configuration from backup."""
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print_error(f"Failed to read backup: {e}")
            return

        print(f"\n{Colors.BOLD}📂 Restoring from backup...{Colors.RESET}\n")
        print_info(f"Backup date: {backup_data.get('timestamp', 'Unknown')}")
        print_info(f"Platform: {backup_data.get('platform', 'Unknown')}")

        # Restore Git config
        if backup_data.get("git_config"):
            print_progress("Restoring Git configuration...")
            for key, value in backup_data["git_config"].items():
                try:
                    subprocess.run(
                        ["git", "config", "--global", key, value],
                        capture_output=True, timeout=10,
                        creationflags=subprocess.CREATE_NO_WINDOW if self.os_type == "windows" else 0
                    )
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    pass
            print_success("Git configuration restored")

        # Report tool status
        print(f"\n{Colors.BOLD}📋 Tool Status (from backup):{Colors.RESET}")
        for tool_id, info in backup_data.get("tools", {}).items():
            status = "✅" if info["installed"] else "❌"
            version = info.get("version", "")
            print(f"  {status} {tool_id}: {version}")

        print_info("Note: Tools need to be reinstalled. Run 'devenv install <tool>'")

    # --------------------------------------------------------
    # Project template generation
    # --------------------------------------------------------
    def create_project(self, template: str, name: str):
        """Create a new project from template."""
        if template not in PROJECT_TEMPLATES:
            print_error(f"Unknown template: {template}")
            print_info(f"Available: {', '.join(PROJECT_TEMPLATES.keys())}")
            return

        tmpl = PROJECT_TEMPLATES[template]
        print(f"\n{Colors.BOLD}🆕 Creating {tmpl['description']} project: {name}{Colors.RESET}\n")

        if tmpl["command"]:
            cmd = tmpl["command"].format(name=name)
            print_progress(f"Running: {cmd}")
            try:
                subprocess.run(cmd, shell=True, timeout=120)
            except subprocess.TimeoutExpired:
                print_error("Project creation timed out")
                return
        else:
            # Custom template
            self._create_custom_template(template, name)

        # Run post commands
        for post_cmd in tmpl["post_commands"]:
            cmd = post_cmd.format(name=name)
            print_progress(f"Running: {cmd}")
            try:
                subprocess.run(cmd, shell=True, timeout=120)
            except subprocess.TimeoutExpired:
                pass

        print_success(f"Project '{name}' created successfully!")

    def _create_custom_template(self, template: str, name: str):
        """Create a custom project template."""
        project_dir = Path(name)
        project_dir.mkdir(exist_ok=True)

        if template == "express":
            # Express + TypeScript template
            package_json = {
                "name": name,
                "version": "1.0.0",
                "description": "",
                "main": "dist/index.js",
                "scripts": {
                    "dev": "ts-node-dev --respawn src/index.ts",
                    "build": "tsc",
                    "start": "node dist/index.js",
                    "lint": "eslint src/"
                },
                "devDependencies": {
                    "@types/express": "^4.17.21",
                    "@types/node": "^20.11.0",
                    "typescript": "^5.3.0",
                    "ts-node-dev": "^2.0.0",
                    "eslint": "^8.56.0"
                },
                "dependencies": {
                    "express": "^4.18.2",
                    "cors": "^2.8.5",
                    "dotenv": "^16.3.0"
                }
            }

            with open(project_dir / "package.json", "w", encoding="utf-8") as f:
                json.dump(package_json, f, indent=2)

            src_dir = project_dir / "src"
            src_dir.mkdir(exist_ok=True)

            # Main entry
            with open(src_dir / "index.ts", "w", encoding="utf-8") as f:
                f.write("""import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/', (_req, res) => {
  res.json({ message: 'Hello, World!' });
});

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
""")

            # tsconfig
            tsconfig = {
                "compilerOptions": {
                    "target": "ES2020",
                    "module": "commonjs",
                    "lib": ["ES2020"],
                    "outDir": "./dist",
                    "rootDir": "./src",
                    "strict": True,
                    "esModuleInterop": True,
                    "skipLibCheck": True,
                    "forceConsistentCasingInFileNames": True,
                    "resolveJsonModule": True,
                    "declaration": True,
                    "declarationMap": True,
                    "sourceMap": True
                },
                "include": ["src/**/*"],
                "exclude": ["node_modules", "dist"]
            }
            with open(project_dir / "tsconfig.json", "w", encoding="utf-8") as f:
                json.dump(tsconfig, f, indent=2)

            # .env
            with open(project_dir / ".env", "w", encoding="utf-8") as f:
                f.write("PORT=3000\n")

            # .gitignore
            with open(project_dir / ".gitignore", "w", encoding="utf-8") as f:
                f.write("node_modules/\ndist/\n.env\n*.log\n")

        elif template == "fastapi":
            # FastAPI template
            with open(project_dir / "requirements.txt", "w", encoding="utf-8") as f:
                f.write("fastapi>=0.109.0\nuvicorn>=0.27.0\npydantic>=2.5.0\npython-dotenv>=1.0.0\n")

            app_dir = project_dir / "app"
            app_dir.mkdir(exist_ok=True)

            with open(app_dir / "__init__.py", "w", encoding="utf-8") as f:
                f.write("")

            with open(app_dir / "main.py", "w", encoding="utf-8") as f:
                f.write('''"""FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="''' + name + '''",
    description="API built with FastAPI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/health")
async def health():
    return {"status": "ok"}
''')

            with open(project_dir / "run.py", "w", encoding="utf-8") as f:
                f.write('''"""Run the FastAPI application."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
''')

            # .env
            with open(project_dir / ".env", "w", encoding="utf-8") as f:
                f.write("APP_NAME=" + name + "\n")

            # .gitignore
            with open(project_dir / ".gitignore", "w", encoding="utf-8") as f:
                f.write("__pycache__/\n*.pyc\n.env\n*.log\n.venv/\n")

    # --------------------------------------------------------
    # System info
    # --------------------------------------------------------
    def system_info(self):
        """Display system information."""
        print(f"\n{Colors.BOLD}💻 System Information{Colors.RESET}\n")
        print(f"  OS: {platform.platform()}")
        print(f"  Python: {platform.python_version()}")
        print(f"  Architecture: {platform.machine()}")
        print(f"  Processor: {platform.processor()}")
        print(f"  Hostname: {platform.node()}")

        # Disk space
        if self.os_type == "windows":
            try:
                result = subprocess.run(
                    ["wmic", "logicaldisk", "get", "size,freespace,caption"],
                    capture_output=True, text=True, timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                if result.returncode == 0:
                    print(f"\n{Colors.BOLD}  Disk Space:{Colors.RESET}")
                    for line in result.stdout.strip().split("\n")[1:]:
                        parts = line.strip().split()
                        if len(parts) >= 3:
                            drive = parts[0]
                            free_gb = int(parts[1]) / (1024**3)
                            total_gb = int(parts[2]) / (1024**3)
                            pct = (free_gb / total_gb) * 100
                            color = Colors.GREEN if pct > 30 else Colors.YELLOW if pct > 10 else Colors.RED
                            print(f"  {drive} {color}{free_gb:.1f}GB free / {total_gb:.1f}GB{Colors.RESET}")
            except Exception:
                pass
        else:
            try:
                result = subprocess.run(
                    ["df", "-h", "/"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split("\n")
                    if len(lines) >= 2:
                        print(f"\n{Colors.BOLD}  Disk Space:{Colors.RESET}")
                        print(f"  {lines[1]}")
            except Exception:
                pass

    # --------------------------------------------------------
    # Doctor - diagnose issues
    # --------------------------------------------------------
    def doctor(self):
        """Diagnose and fix common issues."""
        print(f"\n{Colors.BOLD}🔍 Environment Doctor{Colors.RESET}\n")
        issues = []
        fixes = []

        # Check Python version
        py_version = sys.version_info
        if py_version < (3, 8):
            issues.append(f"Python {py_version.major}.{py_version.minor} is too old (need 3.8+)")
            fixes.append("Install Python 3.8 or later")
        else:
            print_success(f"Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")

        # Check PATH
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        if self.os_type == "windows":
            local_bin = os.path.expandvars(r"%LOCALAPPDATA%\DevEnv-Setup")
        else:
            local_bin = os.path.expanduser("~/.local/bin")
        if local_bin not in path_dirs:
            issues.append(f"{local_bin} not in PATH")
            fixes.append(f"Add {local_bin} to your PATH")
        else:
            print_success("DevEnv bin directory in PATH")

        # Check for common issues
        if self.os_type == "windows":
            # Check Windows Developer Mode
            try:
                result = subprocess.run(
                    ["reg", "query", "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AppModelUnlock", "/v", "AllowDevelopmentWithoutDevLicense"],
                    capture_output=True, text=True, timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                if "0x1" not in result.stdout:
                    issues.append("Windows Developer Mode is off")
                    fixes.append("Enable Developer Mode in Settings > Update & Security > For developers")
                else:
                    print_success("Windows Developer Mode enabled")
            except Exception:
                pass

        # Check Git configuration
        try:
            result = subprocess.run(
                ["git", "config", "--global", "user.name"],
                capture_output=True, text=True, timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if self.os_type == "windows" else 0
            )
            if result.returncode != 0 or not result.stdout.strip():
                issues.append("Git user.name not configured")
                fixes.append("Run: devenv config git --name 'Your Name' --email 'your@email.com'")
            else:
                print_success(f"Git user: {result.stdout.strip()}")
        except Exception:
            issues.append("Git not found or not configured")

        # Summary
        print()
        if issues:
            print(f"{Colors.BOLD}⚠️  Issues Found: {len(issues)}{Colors.RESET}")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {Colors.YELLOW}{issue}{Colors.RESET}")
            print(f"\n{Colors.BOLD}🔧 Suggested Fixes:{Colors.RESET}")
            for i, fix in enumerate(fixes, 1):
                print(f"  {i}. {fix}")
        else:
            print_success("All checks passed! Your environment looks good.")

    # --------------------------------------------------------
    # Update tools
    # --------------------------------------------------------
    def update_tools(self, target: str):
        """Update installed tools."""
        print(f"\n{Colors.BOLD}🔄 Update Tools{Colors.RESET}\n")

        installed = self.check_environment()
        to_update = []

        if target == "all":
            to_update = [t for t, info in installed.items() if info["installed"]]
        elif target in installed and installed[target]["installed"]:
            to_update = [target]
        else:
            print_error(f"Tool not installed: {target}")
            return

        if not to_update:
            print_info("No tools to update")
            return

        print(f"Tools to update: {', '.join(to_update)}\n")

        for tool in to_update:
            print_progress(f"Updating {tool}...")
            if tool == "nodejs":
                if self.os_type == "windows":
                    subprocess.run(["npm", "install", "-g", "npm"], check=False)
                else:
                    subprocess.run(["npm", "install", "-g", "npm"], check=False)
                print_success(f"{tool} updated")
            elif tool == "python":
                print_info("Use your system package manager to update Python")
            elif tool == "git":
                print_info("Use your system package manager to update Git")
            else:
                print_warning(f"Auto-update not available for {tool}, please update manually")

    # --------------------------------------------------------
    # Clean cache
    # --------------------------------------------------------
    def clean_cache(self):
        """Clean downloaded cache files."""
        print(f"\n{Colors.BOLD}🧹 Clean Cache{Colors.RESET}\n")

        cache_dirs = [
            Path.home() / ".devenv" / "cache",
            Path.home() / ".devenv" / "downloads",
            Path.home() / ".cache" / "devenv",
        ]

        total_freed = 0
        for cache_dir in cache_dirs:
            if cache_dir.exists():
                size = sum(f.stat().st_size for f in cache_dir.rglob("*") if f.is_file())
                shutil.rmtree(cache_dir)
                total_freed += size
                print_success(f"Cleaned: {cache_dir} ({size / 1024 / 1024:.1f} MB)")

        if total_freed > 0:
            print(f"\n{Colors.GREEN}Total freed: {total_freed / 1024 / 1024:.1f} MB{Colors.RESET}")
        else:
            print_info("No cache to clean")

    # --------------------------------------------------------
    # Export config
    # --------------------------------------------------------
    def export_config(self, output: str):
        """Export current configuration."""
        print(f"\n{Colors.BOLD}📤 Export Configuration{Colors.RESET}\n")

        config = {
            "version": VERSION,
            "export_date": datetime.datetime.now().isoformat(),
            "platform": self.os_type,
            "tools": {},
            "git": {},
            "vscode_extensions": [],
        }

        # Export tool versions
        env = self.check_environment()
        for tool, info in env.items():
            if info["installed"]:
                config["tools"][tool] = {
                    "version": info.get("version", "unknown"),
                    "path": info.get("path", "unknown"),
                }

        # Export Git config
        try:
            result = subprocess.run(
                ["git", "config", "--global", "--list"],
                capture_output=True, text=True, timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if self.os_type == "windows" else 0
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        config["git"][key] = value
        except Exception:
            pass

        # Export VS Code extensions
        if self.check_tool("vscode")["installed"]:
            try:
                result = subprocess.run(
                    ["code", "--list-extensions"],
                    capture_output=True, text=True, timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW if self.os_type == "windows" else 0
                )
                if result.returncode == 0:
                    config["vscode_extensions"] = result.stdout.strip().split("\n")
            except Exception:
                pass

        # Write file
        output_path = Path(output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print_success(f"Configuration exported to: {output_path.absolute()}")
        print_info(f"Tools: {len(config['tools'])}")
        print_info(f"Git settings: {len(config['git'])}")
        print_info(f"VS Code extensions: {len(config['vscode_extensions'])}")

    # --------------------------------------------------------
    # Main command handler
    # --------------------------------------------------------
    def run(self, args: list):
        """Main entry point."""
        parser = argparse.ArgumentParser(
            prog="devenv",
            description="🚀 DevEnv-Setup - One-Click Development Environment Setup Tool"
        )
        parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # check
        subparsers.add_parser("check", help="Check current development environment")

        # install
        install_parser = subparsers.add_parser("install", help="Install a tool or preset")
        install_parser.add_argument("target", help="Tool name or preset (e.g., nodejs, web-full)")
        install_parser.add_argument("--version", help="Specific version to install")

        # config
        config_parser = subparsers.add_parser("config", help="Configure development tools")
        config_parser.add_argument("tool", help="Tool to configure (e.g., git)")
        config_parser.add_argument("--name", help="Name for git config")
        config_parser.add_argument("--email", help="Email for git config")

        # backup
        backup_parser = subparsers.add_parser("backup", help="Backup current configuration")
        backup_parser.add_argument("--output", help="Output file path")

        # restore
        restore_parser = subparsers.add_parser("restore", help="Restore from backup")
        restore_parser.add_argument("input", help="Backup file path")

        # new
        new_parser = subparsers.add_parser("new", help="Create project from template")
        new_parser.add_argument("template", help="Template name (react, vue, next, express, fastapi, django)")
        new_parser.add_argument("name", help="Project name")

        # extensions
        ext_parser = subparsers.add_parser("extensions", help="Install VS Code extensions")
        ext_parser.add_argument("category", nargs="?", default="general",
                              help="Category: general, python, web, go, rust, docker")

        # info
        subparsers.add_parser("info", help="Show system information")

        # list
        list_parser = subparsers.add_parser("list", help="List available tools/presets/templates")
        list_parser.add_argument("type", choices=["tools", "presets", "templates"],
                               help="What to list")

        # doctor - diagnose issues
        subparsers.add_parser("doctor", help="Diagnose and fix common issues")

        # update - update installed tools
        update_parser = subparsers.add_parser("update", help="Update installed tools")
        update_parser.add_argument("target", nargs="?", default="all",
                                 help="Tool to update (default: all)")

        # clean - clean cache
        subparsers.add_parser("clean", help="Clean downloaded cache files")

        # export - export config
        export_parser = subparsers.add_parser("export", help="Export configuration")
        export_parser.add_argument("--output", default="devenv-export.json",
                                 help="Output file path")

        parsed = parser.parse_args(args)

        if not parsed.command:
            print_banner()
            parser.print_help()
            return

        if parsed.command == "check":
            print_banner()
            results = self.check_environment()
            self.display_dashboard(results)

        elif parsed.command == "install":
            print_banner()
            target = parsed.target
            if target in PRESETS:
                self.install_preset(target)
            elif target in TOOL_DEFINITIONS:
                self.install_tool(target, parsed.version)
            else:
                print_error(f"Unknown target: {target}")
                print_info(f"Tools: {', '.join(TOOL_DEFINITIONS.keys())}")
                print_info(f"Presets: {', '.join(PRESETS.keys())}")

        elif parsed.command == "config":
            print_banner()
            if parsed.tool == "git":
                if parsed.name and parsed.email:
                    self.config_git(parsed.name, parsed.email)
                else:
                    print_error("Git config requires --name and --email")
            else:
                print_error(f"Unknown tool: {parsed.tool}")

        elif parsed.command == "backup":
            print_banner()
            self.backup_config(parsed.output)

        elif parsed.command == "restore":
            print_banner()
            self.restore_config(parsed.input)

        elif parsed.command == "new":
            print_banner()
            self.create_project(parsed.template, parsed.name)

        elif parsed.command == "extensions":
            print_banner()
            self.install_vscode_extensions(parsed.category)

        elif parsed.command == "info":
            print_banner()
            self.system_info()

        elif parsed.command == "list":
            print_banner()
            if parsed.type == "tools":
                print(f"\n{Colors.BOLD}🛠️  Available Tools:{Colors.RESET}\n")
                for tool_id, info in TOOL_DEFINITIONS.items():
                    print(f"  {Colors.CYAN}{tool_id:<14}{Colors.RESET} {info['name']} [{info['category']}]")
            elif parsed.type == "presets":
                print(f"\n{Colors.BOLD}📦 Available Presets:{Colors.RESET}\n")
                for preset_id, info in PRESETS.items():
                    print(f"  {Colors.CYAN}{preset_id:<18}{Colors.RESET} {info['description']}")
                    print(f"  {'':18} Tools: {', '.join(info['tools'])}")
            elif parsed.type == "templates":
                print(f"\n{Colors.BOLD}🆕 Available Templates:{Colors.RESET}\n")
                for tmpl_id, info in PROJECT_TEMPLATES.items():
                    print(f"  {Colors.CYAN}{tmpl_id:<14}{Colors.RESET} {info['description']}")

        elif parsed.command == "doctor":
            print_banner()
            self.doctor()

        elif parsed.command == "update":
            print_banner()
            self.update_tools(parsed.target)

        elif parsed.command == "clean":
            print_banner()
            self.clean_cache()

        elif parsed.command == "export":
            print_banner()
            self.export_config(parsed.output)


def main():
    """Main entry point."""
    app = DevEnvSetup()
    app.run(sys.argv[1:])


if __name__ == "__main__":
    main()
