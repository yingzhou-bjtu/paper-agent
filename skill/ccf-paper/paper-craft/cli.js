#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const SKILLS = [
  'paper-launch', 'paper-search', 'paper-idea', 'paper-plan',
  'paper-data', 'paper-env', 'paper-train', 'paper-story',
  'paper-write', 'paper-review', 'paper-rebuttal', 'paper-audit'
];

const BUNDLES = {
  full: SKILLS,
  'search-only': ['paper-search'],
  'write-only': ['paper-story', 'paper-write', 'paper-review'],
  'launch-only': ['paper-launch']
};

const CONFERENCE_SKILLS = ['paper-search', 'paper-launch', 'paper-review'];

const SCRIPT_DIR = __dirname;

// Colors
const RED = '\x1b[0;31m';
const GREEN = '\x1b[0;32m';
const YELLOW = '\x1b[1;33m';
const NC = '\x1b[0m';

function info(msg) { console.log(`${GREEN}[paper-craft]${NC} ${msg}`); }
function warn(msg) { console.log(`${YELLOW}[paper-craft]${NC} ${msg}`); }
function error(msg) { console.error(`${RED}[paper-craft]${NC} ${msg}`); process.exit(1); }

// Parse arguments
function parseArgs(argv) {
  const args = { bundle: 'full', target: '.', tools: [] };
  const rest = argv.slice(2);
  let i = 0;
  while (i < rest.length) {
    switch (rest[i]) {
      case '--bundle':
        if (!rest[i + 1]) error('--bundle requires a value');
        args.bundle = rest[++i];
        break;
      case '--target':
        if (!rest[i + 1]) error('--target requires a value');
        args.target = rest[++i];
        break;
      case '--tool':
        if (!rest[i + 1]) error('--tool requires a value');
        args.tools.push(rest[++i]);
        break;
      case '--help': case '-h':
        console.log(`Usage: paper-craft [options]

Options:
  --bundle full|search-only|write-only|launch-only   Skill bundle (default: full)
  --target <dir>                                      Target directory (default: .)
  --tool claude-code|cursor|codex|gemini|copilot|windsurf  Target tool (auto-detected)
  --help                                              Show this help`);
        process.exit(0);
        break;
      default:
        error(`Unknown option: ${rest[i]}. Use --help for usage.`);
    }
    i++;
  }
  return args;
}

function needsConferences(selectedSkills) {
  return selectedSkills.some(s => CONFERENCE_SKILLS.includes(s));
}

function copyDirSync(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function mkdirp(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

// Install for Claude Code
function installClaudeCode(targetDir, selectedSkills) {
  info('Installing for Claude Code...');
  const skillsDir = path.join(targetDir, '.claude', 'skills');
  mkdirp(skillsDir);

  for (const skill of selectedSkills) {
    const src = path.join(SCRIPT_DIR, 'skills', skill);
    const dest = path.join(skillsDir, skill);
    copyDirSync(src, dest);
    info(`  Installed skill: ${skill}`);
  }

  // Copy conference profiles to skills that reference them
  const confSrc = path.join(SCRIPT_DIR, 'references', 'conferences');
  let needsConf = false;
  for (const skill of CONFERENCE_SKILLS) {
    if (selectedSkills.includes(skill)) {
      needsConf = true;
      const confDest = path.join(skillsDir, skill, 'references', 'conferences');
      mkdirp(confDest);
      if (fs.existsSync(confSrc)) {
        copyDirSync(confSrc, confDest);
      }
    }
  }
  if (needsConf) info('  Installed conference profiles');

  // Handle CLAUDE.md
  const claudeMdPath = path.join(targetDir, '.claude', 'CLAUDE.md');
  const rulesContent = fs.readFileSync(path.join(SCRIPT_DIR, 'CLAUDE.md'), 'utf8');
  mkdirp(path.join(targetDir, '.claude'));

  if (fs.existsSync(claudeMdPath)) {
    fs.appendFileSync(claudeMdPath, '\n\n# --- PaperCraft Rules (appended by paper-craft) ---\n');
    fs.appendFileSync(claudeMdPath, rulesContent);
    info('  Appended rules to existing CLAUDE.md');
  } else {
    fs.writeFileSync(claudeMdPath, rulesContent);
    info('  Created .claude/CLAUDE.md');
  }
}

// Install for Cursor
function installCursor(targetDir, selectedSkills) {
  info('Installing for Cursor...');
  const rulesDir = path.join(targetDir, '.cursor', 'rules');
  mkdirp(rulesDir);

  for (const skill of selectedSkills) {
    const skillMd = path.join(SCRIPT_DIR, 'skills', skill, 'SKILL.md');
    let content = fs.readFileSync(skillMd, 'utf8');

    // Append reference file contents if they exist
    const refsDir = path.join(SCRIPT_DIR, 'skills', skill, 'references');
    if (fs.existsSync(refsDir)) {
      const refs = fs.readdirSync(refsDir).filter(f => f.endsWith('.md'));
      if (refs.length > 0) {
        content += '\n\n## Reference Files';
        for (const ref of refs) {
          content += `\n\n### ${path.basename(ref, '.md')}\n\n`;
          content += fs.readFileSync(path.join(refsDir, ref), 'utf8');
        }
      }
    }

    fs.writeFileSync(path.join(rulesDir, `${skill}.mdc`), content);
    info(`  Installed rule: ${skill}.mdc`);
  }

  // Copy conference profiles as a separate rule
  if (needsConferences(selectedSkills)) {
    const confSrc = path.join(SCRIPT_DIR, 'references', 'conferences');
    if (fs.existsSync(confSrc)) {
      let confContent = '# Conference Profiles (16 CCF-A)\n';
      for (const f of fs.readdirSync(confSrc).filter(f => f.endsWith('.md')).sort()) {
        confContent += '\n' + fs.readFileSync(path.join(confSrc, f), 'utf8') + '\n';
      }
      fs.writeFileSync(path.join(rulesDir, 'conference-profiles.mdc'), confContent);
      info('  Installed rule: conference-profiles.mdc');
    }
  }

  const rulesContent = fs.readFileSync(path.join(SCRIPT_DIR, 'CLAUDE.md'), 'utf8');
  fs.writeFileSync(path.join(rulesDir, 'paper-craft-rules.mdc'), rulesContent);
  info('  Installed rules: paper-craft-rules.mdc');
}

// Install for single-file tools (Codex, Gemini, Copilot, Windsurf)
function installSingleFile(targetDir, selectedSkills, fileName) {
  const validTools = {
    codex: { file: 'AGENTS.md', label: 'Codex CLI' },
    gemini: { file: 'GEMINI.md', label: 'Gemini CLI' },
    copilot: { file: path.join('.github', 'copilot-instructions.md'), label: 'GitHub Copilot' },
    windsurf: { file: '.windsurfrules', label: 'Windsurf' }
  };
  const { file, label } = validTools[fileName];
  info(`Installing for ${label}...`);

  let content = fs.readFileSync(path.join(SCRIPT_DIR, 'CLAUDE.md'), 'utf8');
  content += '\n\n## Skill Instructions';

  for (const skill of selectedSkills) {
    content += '\n\n' + fs.readFileSync(path.join(SCRIPT_DIR, 'skills', skill, 'SKILL.md'), 'utf8');
    const refsDir = path.join(SCRIPT_DIR, 'skills', skill, 'references');
    if (fs.existsSync(refsDir)) {
      for (const ref of fs.readdirSync(refsDir).filter(f => f.endsWith('.md'))) {
        content += `\n\n### Reference: ${path.basename(ref, '.md')}\n\n`;
        content += fs.readFileSync(path.join(refsDir, ref), 'utf8');
      }
    }
  }

  if (needsConferences(selectedSkills)) {
    content += '\n\n## Conference Profiles (16 CCF-A)';
    const confSrc = path.join(SCRIPT_DIR, 'references', 'conferences');
    if (fs.existsSync(confSrc)) {
      for (const f of fs.readdirSync(confSrc).filter(f => f.endsWith('.md')).sort()) {
        content += '\n\n' + fs.readFileSync(path.join(confSrc, f), 'utf8');
      }
    }
  }

  const filePath = path.join(targetDir, file);
  mkdirp(path.dirname(filePath));
  fs.appendFileSync(filePath, content);
  info(`  Appended to ${file}`);
}

// Main
function main() {
  const args = parseArgs(process.argv);

  // Validate bundle
  if (!BUNDLES[args.bundle]) {
    error(`Unknown bundle: ${args.bundle}. Use: full, search-only, write-only, launch-only`);
  }
  const selectedSkills = BUNDLES[args.bundle];

  // Resolve target directory
  const targetDir = path.resolve(args.target);
  if (!fs.existsSync(targetDir)) {
    error(`Target directory not found: ${args.target}`);
  }
  process.chdir(targetDir);

  // Auto-detect tools if not specified
  let tools = args.tools;
  if (tools.length === 0) {
    if (fs.existsSync('.claude')) tools.push('claude-code');
    if (fs.existsSync('.cursor')) tools.push('cursor');
    if (fs.existsSync('AGENTS.md')) tools.push('codex');
    if (fs.existsSync('GEMINI.md')) tools.push('gemini');
    if (fs.existsSync('.github')) tools.push('copilot');
    if (fs.existsSync('.windsurfrules')) tools.push('windsurf');

    if (tools.length === 0) {
      tools.push('claude-code');
      info('No tool detected, defaulting to Claude Code');
    } else {
      info(`Detected tools: ${tools.join(', ')}`);
    }
  }

  // Validate tool names
  const validToolNames = ['claude-code', 'cursor', 'codex', 'gemini', 'copilot', 'windsurf'];
  for (const tool of tools) {
    if (!validToolNames.includes(tool)) {
      error(`Unknown tool: ${tool}. Valid options: ${validToolNames.join(', ')}`);
    }
  }

  // Execute installations
  for (const tool of tools) {
    switch (tool) {
      case 'claude-code': installClaudeCode(targetDir, selectedSkills); break;
      case 'cursor': installCursor(targetDir, selectedSkills); break;
      case 'codex': installSingleFile(targetDir, selectedSkills, 'codex'); break;
      case 'gemini': installSingleFile(targetDir, selectedSkills, 'gemini'); break;
      case 'copilot': installSingleFile(targetDir, selectedSkills, 'copilot'); break;
      case 'windsurf': installSingleFile(targetDir, selectedSkills, 'windsurf'); break;
    }
  }

  info(`Installation complete!`);
  info(`Installed ${selectedSkills.length} skill(s) for ${tools.length} tool(s)`);
  info(`Skills: ${selectedSkills.join(', ')}`);
  info(`Tools: ${tools.join(', ')}`);
}

main();
