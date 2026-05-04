#!/usr/bin/env bash
# DevEnv-Setup Installer for Linux/macOS
# One-Click Development Environment Setup Tool

set -e

VERSION="1.0.0"
INSTALL_DIR="${HOME}/.local/devenv"
BIN_DIR="${HOME}/.local/bin"
REPO_URL="https://github.com/KEBANJILONG/DevEnv-Setup"
RAW_URL="https://raw.githubusercontent.com/KEBANJILONG/DevEnv-Setup/main"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║   🚀 DevEnv-Setup v${VERSION}                          ║"
    echo "║   One-Click Development Environment Setup             ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "  ${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "  ${RED}❌${NC} $1"
}

print_info() {
    echo -e "  ${CYAN}ℹ️${NC} $1"
}

print_progress() {
    echo -e "  ${YELLOW}⏳${NC} $1"
}

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
        print_success "Python detected: $(python3 --version)"
        return 0
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        return 1
    fi
}

install_devenv() {
    print_progress "Installing DevEnv-Setup..."

    # Create directories
    mkdir -p "${INSTALL_DIR}"
    mkdir -p "${BIN_DIR}"

    # Download main script
    print_progress "Downloading main script..."
    if command -v curl &> /dev/null; then
        curl -fsSL "${RAW_URL}/src/devenv.py" -o "${INSTALL_DIR}/devenv.py"
    elif command -v wget &> /dev/null; then
        wget -q "${RAW_URL}/src/devenv.py" -O "${INSTALL_DIR}/devenv.py"
    fi

    # Create launcher script
    cat > "${INSTALL_DIR}/devenv" << 'LAUNCHER'
#!/usr/bin/env bash
python3 "${HOME}/.local/devenv/devenv.py" "$@"
LAUNCHER
    chmod +x "${INSTALL_DIR}/devenv"

    # Create symlink to bin
    ln -sf "${INSTALL_DIR}/devenv" "${BIN_DIR}/devenv"

    print_success "DevEnv-Setup installed successfully!"
}

add_to_path() {
    SHELL_RC=""
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    if [ -n "$SHELL_RC" ]; then
        if ! grep -q "export PATH=.*\.local/bin" "$SHELL_RC" 2>/dev/null; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
            print_info "Added ~/.local/bin to PATH in $SHELL_RC"
            print_info "Please run: source $SHELL_RC"
        fi
    fi
}

# Main
print_banner
echo ""

check_python || exit 1
echo ""

install_devenv
add_to_path

echo ""
print_success "Installation complete!"
echo ""
print_info "Usage:"
echo "  devenv check          - Check development environment"
echo "  devenv install nodejs - Install a tool"
echo "  devenv install web-full - Install preset"
echo "  devenv list tools     - List available tools"
echo ""
print_info "If 'devenv' command not found, restart your terminal or run:"
echo "  source ~/.bashrc  # or ~/.zshrc"