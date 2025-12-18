<div align="center">

# agentic-config (Personal Fork)

### Prompt-based installer for AI coding setups (profiles → project/user config)

Repo: https://github.com/fcimeson/agentic-config

Upstream base: https://github.com/darrenhinde/OpenAgents

**Primary goal:** Use `install.sh` + the existing profile system to install curated configs into:
- Project folders (`./.opencode`)
- User config (via the installer's existing global target, e.g. `~/.config/opencode`)

**Planned extensions:** MCP server selection per target • `.env` install per target • Claude Code support (TBD)

</div>


## Why Use This Fork?

- ✅ **Prompt-based installer** via `curl | bash` (built around `install.sh`)
- ✅ **Profiles-first workflow** (reuse/extend the existing profile system)
- ✅ **Targeted installs**: install into project folders (`./.opencode`) or user config (existing global target)
- ✅ **Personal setups**: add domain profiles for your work (e.g. `esp32`, `linux-admin`, etc.)
- 🧩 **Planned**: select MCP servers and write config per install target
- 🧩 **Planned**: copy/merge `.env` behavior into the chosen target
- 🧩 **Planned**: support Claude Code alongside OpenCode (details TBD)

This repo is intentionally diverging into a **personal customization and distribution** while still tracking upstream improvements.

## Keeping in sync with upstream

If you want to pull updates from the upstream project while keeping your changes:

```bash
# Add upstream once
git remote add upstream https://github.com/darrenhinde/OpenAgents.git

# Fetch upstream changes
git fetch upstream

# Merge upstream main into your main
git checkout main
git merge upstream/main
```

If you prefer a linear history, use rebase instead of merge:

```bash
git checkout main
git fetch upstream
git rebase upstream/main
```

When resolving conflicts, prioritize keeping this fork's installer/profile direction (especially `install.sh`, `registry.json`, and docs that reference this repo).

---

## Quick Start

### Step 1: Install OpenCode CLI
See the official docs: https://opencode.ai/docs

### Step 2: Install Agents & Commands

> **New! Python Installer:** The installer now uses Python (3.9+) instead of bash for improved cross-platform compatibility and easier maintenance. The `install.sh` script automatically detects and runs Python. Legacy bash installer is available at `install.sh.bak`.

**Option A: Interactive Installer**

> **Note:** Interactive mode needs a terminal. Download the script first, run it, then delete it if you like.

<details open>
<summary><b>macOS / Linux</b></summary>

```bash
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh -o install.sh
bash install.sh
rm install.sh
```
</details>

<details>
<parameter name="filePath">/home/fcimeson/agentic-config/README.md
<summary><b>Windows (Git Bash)</b></summary>

```bash
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh -o install.sh
bash install.sh
rm install.sh
```
</details>

<details>
<summary><b>Windows (PowerShell)</b></summary>

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh" -OutFile "$env:TEMP\install.sh"
& "C:\Program Files\Git\bin\bash.exe" "$env:TEMP\install.sh"
Remove-Item "$env:TEMP\install.sh" -Force
```

> **Note:** Git Bash comes with Git for Windows. [Download here](https://git-scm.com/download/win)
</details>

The installer offers:
- 🎯 **Quick Profiles**: Essential, Developer, Business, Full, or Advanced
- 🎨 **Custom Selection**: Pick exactly what you need
- 📦 **Smart Dependencies**: Auto-installs required components
- ✨ **Interactive Menus**: User-friendly component browser
- 🛡️ **Collision Detection**: Safely handles existing files with 4 strategies (skip/overwrite/backup/cancel)
- 🖥️ **Cross-Platform**: Works on macOS, Linux, and Windows (Git Bash/WSL)

> **Updating?** The installer detects existing files and lets you choose: skip existing (keep your changes), overwrite all (get latest), or backup & overwrite (safe update). [Learn more](docs/getting-started/collision-handling.md)

**Option B: Profile-Based Install (Recommended)**

> **Fastest method:** One command, no interaction needed

<details open>
<summary><b>macOS / Linux / Git Bash / WSL</b></summary>

```bash
# Essential - Minimal essentials (9 components)
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh | bash -s essential

# Developer - Recommended for daily work (19 components)
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh | bash -s developer

# Business - Business automation and content creation (15 components)
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh | bash -s business

# Full - Everything included (25 components)
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh | bash -s full

# Advanced - Full + System Builder (32 components)
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh | bash -s advanced
```
</details>

<details>
<summary><b>Windows PowerShell</b></summary>

```powershell
# Download script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh" -OutFile "install.sh"

# Essential profile
& "C:\Program Files\Git\bin\bash.exe" install.sh essential

# Developer profile
& "C:\Program Files\Git\bin\bash.exe" install.sh developer

# Business profile
& "C:\Program Files\Git\bin\bash.exe" install.sh business

# Full profile
& "C:\Program Files\Git\bin\bash.exe" install.sh full

# Advanced profile
& "C:\Program Files\Git\bin\bash.exe" install.sh advanced
```
</details>

> **New!** The `advanced` profile includes the **System Builder** - an interactive tool that generates complete custom AI systems tailored to your domain. [Learn more](docs/features/system-builder/)

**Option C: Manual Install**
```bash
# Clone this repository
git clone https://github.com/fcimeson/agentic-config.git
cd agentic-config

# Install to OpenCode directory (global)
mkdir -p ~/.config/opencode
cp -r .opencode/agent ~/.config/opencode/
cp -r .opencode/command ~/.config/opencode/
cp -r .opencode/context ~/.config/opencode/
```

### Step 3: Start Building
```bash
# Start the universal agent (recommended for new users)
opencode --agent openagent

# Ask questions or request tasks
> "Create a React todo list with TypeScript"
```

**What happens next:**
1. OpenAgent analyzes your request (question or task)
2. For tasks: proposes a plan and asks for approval
3. Executes step-by-step with validation
4. Delegates to specialists (@task-manager, @tester, @reviewer) when needed
5. Confirms completion and offers cleanup

---

## How It Works

```
User Request
    ↓
┌───────────────────────────────────────┐
│  Main Agents (User-Facing)           │
├───────────────────────────────────────┤
│  openagent     │ General tasks        │
│  opencoder     │ Complex coding       │
│  system-builder│ AI system generation │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│  Specialized Subagents                │
├───────────────────────────────────────┤
│  Core:         task-manager, docs     │
│  Code:         coder, tester, reviewer│
│  Utils:        image-specialist       │
│  Meta:         domain-analyzer, etc.  │
└───────────────────────────────────────┘
```

**The workflow:**
1. **You describe** what you want to build
2. **Agent plans** the implementation steps
3. **You approve** the plan
4. **Agent implements** incrementally with validation
5. **Quality checks** run automatically (tests, types, linting)
6. **Subagents handle** specialized tasks (testing, review, docs)

**Context-aware:** Agents automatically load patterns from `.opencode/context/` to follow your coding standards.

---

## What's Included

### 🤖 Main Agents
- **openagent** - Universal coordinator for general tasks, questions, and workflows (recommended default)
- **opencoder** - Specialized development agent for complex coding, architecture, and refactoring
- **system-builder** - Meta-level generator for creating custom AI architectures

### 🔧 Specialized Subagents (Auto-delegated)

**Core Coordination:**
- **task-manager** - Task breakdown and planning
- **documentation** - Documentation authoring

**Code Specialists:**
- **coder-agent** - Quick implementation tasks
- **reviewer** - Code review and security analysis
- **tester** - Test creation and validation
- **build-agent** - Build and type checking
- **codebase-pattern-analyst** - Pattern discovery

**Utilities:**
- **image-specialist** - Image generation with Gemini AI

**System Builder (Meta-Level):**
- **domain-analyzer** - Domain analysis and agent recommendations
- **agent-generator** - XML-optimized agent generation
- **context-organizer** - Context file organization
- **workflow-designer** - Workflow design
- **command-creator** - Custom command creation

### ⚡ Commands
- **/commit** - Smart git commits with conventional format
- **/optimize** - Code optimization
- **/test** - Testing workflows
- **/clean** - Cleanup operations
- **/context** - Context management
- **/prompt-enchancer** - Improve your prompts
- **/worktrees** - Git worktree management
- **/validate-repo** - Validate repository consistency

### 📚 Context Files
- `core/essential-patterns.md` - Universal coding patterns
- `project/project-context.md` - Your project-specific patterns

---

## Example Workflows

### Build a Feature
```bash
opencode --agent openagent
> "Create a user authentication system with email/password"

# OpenAgent will:
# 1. Analyze the request (complex task)
# 2. Propose implementation plan
# 3. Wait for your approval
# 4. Delegate to @task-manager (creates task breakdown)
# 5. Coordinate implementation step-by-step
# 6. Use @tester for tests and @reviewer for security
# 7. Validate, summarize, and confirm completion
```

### Make a Commit
```bash
# Make your changes
git add .

# Use the commit command
/commit

# Auto-generates: ✨ feat: add user authentication system
```

### Add Your Patterns
```bash
# Edit your project context
nano ~/.config/opencode/context/project/project-context.md

# Add your patterns:
# **API Endpoint Pattern:**
# ```typescript
# export async function POST(request: Request) {
#   // Your standard pattern
# }
# ```

# Agents will automatically use these patterns!
```

---

## 🏗️ System Builder (New!)

**Build complete custom AI systems tailored to your domain in minutes.**

The System Builder is an interactive tool that generates complete `.opencode` architectures customized to your needs.

### Quick Start
```bash
# Install advanced profile (includes system builder)
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh | bash -s advanced

# Run the interactive builder
/build-context-system
```

### What It Does
- 🎯 **Interactive Interview** - Asks about your domain, use cases, and requirements
- 🤖 **Generates Complete System** - Creates orchestrator, subagents, context files, workflows, and commands
- 🔗 **Integrates with Existing** - Detects and reuses your existing agents
- 🛡️ **Safe Merging** - Won't overwrite your work, offers merge strategies
- 📚 **Production-Ready** - Includes documentation, testing guides, and examples

### Example
```bash
$ /build-context-system

Domain: E-commerce Operations
Purpose: Automate order processing and customer support

# After answering questions, generates:
# - ecommerce-orchestrator (main agent)
# - order-processor, ticket-router, report-generator (subagents)
# - 12 context files (domain knowledge, processes, standards)
# - 5 workflows (process-order, route-ticket, etc.)
# - 5 custom commands (/process-order, /route-ticket, etc.)
# - Complete documentation
```

**Learn more:** [System Builder Documentation](docs/features/system-builder/)

---

## Optional Add-ons

### 📱 Telegram Notifications
Get notified when OpenCode sessions go idle.

```bash
# Copy plugin directory
cp -r .opencode/plugin ~/.config/opencode/

# Install dependencies
cd ~/.config/opencode/plugin
npm install

# Configure
cd ~/agentic-config
cp env.example .env
# Edit .env with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
```

**Get credentials:** Message @BotFather on Telegram → `/newbot` → Save token

See [`.opencode/plugin/README.md`](.opencode/plugin/README.md) for detailed documentation.

### 🎨 Gemini AI Image Tools
Generate and edit images using Gemini AI.

```bash
# Copy tool directory
cp -r .opencode/tool ~/.config/opencode/

# Install dependencies
cd ~/.config/opencode/tool
npm install

# Configure
cd ~/agentic-config
cp env.example .env
# Edit .env with GEMINI_API_KEY
```

**Get API key:** https://makersuite.google.com/app/apikey

---

## Common Questions

**Q: What's the main way to use this?**  
A: Use `opencode --agent openagent` as your default for general tasks and questions. For complex multi-file coding work, use `opencode --agent opencoder`. Both coordinate with specialists as needed.

**Q: Does this work on Windows?**  
A: Yes! Use Git Bash (recommended) or WSL. See [Platform Compatibility Guide](docs/getting-started/platform-compatibility.md) for details.

**Q: What bash version do I need?**  
A: Bash 3.2+ (works on macOS default bash). Run `bash scripts/tests/test-compatibility.sh` to check your system.

**Q: Do I need to install plugins/tools?**  
A: No, they're optional. Only install if you want Telegram notifications or Gemini AI features.

**Q: Where should I install - globally or per-project?**  
A: Global (`~/.config/opencode/`) works for most. Project-specific (`./.opencode/`) if you need different configs per project.

**Q: How do I add my own coding patterns?**  
A: Edit `~/.config/opencode/context/project/project-context.md` - agents automatically load this file.

**Q: What languages are supported?**  
A: The agents work with any language (TypeScript, Python, Go, Rust, etc.) and adapt based on your project files.

**Q: What's the Agent System Blueprint for?**  
A: It's a teaching document explaining architecture patterns and how to extend the system. See [docs/features/agent-system-blueprint.md](docs/features/agent-system-blueprint.md)

**Q: Can I use just one command or agent?**  
A: Yes! Use the installer's list feature to see all components:
```bash
./install.sh --list
```
Or cherry-pick individual files with curl:
```bash
curl -o ~/.config/opencode/agent/opencoder.md \
  https://raw.githubusercontent.com/fcimeson/agentic-config/main/.opencode/agent/opencoder.md
```

---

## Installation Profiles

The installer offers five pre-configured profiles:

### 🎯 Essential (Minimal - 9 components)
Minimal starter kit - universal agent with core subagents.
- **Agents**: openagent
- **Subagents**: task-manager, documentation
- **Commands**: context, clean
- **Tools**: env
- **Context**: essential-patterns, project-context
- **Config**: env-example
- **Best for**: Learning the system, lightweight tasks, minimal setup

### 💼 Developer (Recommended - 30 components)
Complete software development environment with code generation, testing, review, and build tools.
- Everything in Essential, plus:
- **Agents**: opencoder
- **Subagents**: coder-agent, reviewer, tester, build-agent, codebase-pattern-analyst
- **Commands**: commit, test, optimize, validate-repo
- **Context**: All standards and workflow files (code, patterns, tests, docs, analysis, delegation, sessions, task-breakdown, review, context-guide)
- **Config**: readme
- **Best for**: Most developers, daily use, full-featured development

### 📊 Business (15 components)
Business process automation, content creation, and visual workflows.
- **Agents**: openagent
- **Subagents**: task-manager, documentation, image-specialist
- **Commands**: context, clean, prompt-enhancer
- **Tools**: env, gemini (AI image generation)
- **Plugins**: notify, telegram-notify
- **Context**: essential-patterns, project-context
- **Config**: env-example, readme
- **Best for**: Business automation, content creation, non-developers

### 📦 Full (36 components)
Everything included - all agents, subagents, tools, and plugins.
- Everything in Developer and Business combined, plus:
- **Commands**: worktrees (git worktree management), validate-repo
- **Best for**: Power users, exploring all features

### 🚀 Advanced (43 components)
Full installation plus **System Builder** for creating custom AI architectures.
- Everything in Full, plus:
- **Agents**: system-builder
- **System Builder Subagents**: domain-analyzer, agent-generator, context-organizer, workflow-designer, command-creator
- **Commands**: build-context-system
- **Best for**: Building custom AI systems, contributors, learning the architecture

## Updating Components

Keep your components up to date:

```bash
# Update all installed components
./update.sh

# Or re-run the installer
curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh | bash
```

---

## Advanced

### Understanding the System
Read [Agent System Blueprint](docs/features/agent-system-blueprint.md) to learn:
- How context loading works (the `@` symbol)
- Agent architecture patterns
- How to create custom agents and commands
- How to extend the system for your needs

### Safety & Security
- **Approval-first workflow** - Agents propose plans before execution
- **Configurable permissions** - Granular control over agent capabilities
- **Secure credentials** - Environment variables for sensitive data
- **Input sanitization** - Protection against injection attacks

### Project Structure
```
.opencode/
├── agent/              # AI agents
│   ├── openagent.md
│   ├── opencoder.md
│   ├── system-builder.md
│   └── subagents/      # Specialized helpers
├── command/            # Slash commands
│   ├── commit.md
│   └── optimize.md
├── context/            # Coding patterns
│   ├── core/           # Essential patterns
│   └── project/        # Your patterns
├── plugin/             # Optional: Telegram
└── tool/               # Optional: Gemini AI
```

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing/CONTRIBUTING.md) for details.

1. Follow the established naming conventions and coding standards
2. Write comprehensive tests for new features
3. Update documentation for any changes
4. Ensure security best practices are followed

See also: [Code of Conduct](docs/contributing/CODE_OF_CONDUCT.md)

---

## License

This project is licensed under the MIT License.

---

## Recommended for New Users

**Start with `openagent`** - your universal coordinator for general tasks, questions, and workflows. It follows a systematic 6-stage workflow (Analyze → Approve → Execute → Validate → Summarize → Confirm) and automatically delegates to specialized subagents when needed.

```bash
opencode --agent openagent
> "How do I implement authentication in Next.js?"  # Questions
> "Create a user authentication system"            # Simple tasks
> "Create a README for this project"               # Documentation
```

OpenAgent will guide you through with a plan-first, approval-based approach. For questions, you get direct answers. For tasks, you see the plan before execution.

**For complex coding work**, use `opencoder`:

```bash
opencode --agent opencoder
> "Refactor this codebase to use dependency injection"  # Multi-file refactoring
> "Analyze the architecture and suggest improvements"   # Architecture analysis
```

**Learn more:** 
- [OpenAgent Guide](docs/agents/openagent.md) - General tasks and coordination
- [OpenCoder Guide](docs/agents/opencoder.md) - Specialized development work

