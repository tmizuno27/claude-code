import * as vscode from 'vscode';
import { execSync } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

// --- Types ---

interface CommitType {
  label: string;
  description: string;
  emoji: string;
}

const COMMIT_TYPES: CommitType[] = [
  { label: 'feat', description: 'A new feature', emoji: '✨' },
  { label: 'fix', description: 'A bug fix', emoji: '🐛' },
  { label: 'docs', description: 'Documentation only changes', emoji: '📝' },
  { label: 'style', description: 'Code style (formatting, semicolons, etc.)', emoji: '💎' },
  { label: 'refactor', description: 'Code refactoring', emoji: '♻️' },
  { label: 'perf', description: 'Performance improvement', emoji: '⚡' },
  { label: 'test', description: 'Adding or updating tests', emoji: '🧪' },
  { label: 'build', description: 'Build system or dependencies', emoji: '📦' },
  { label: 'ci', description: 'CI/CD configuration', emoji: '🔧' },
  { label: 'chore', description: 'Other changes (maintenance)', emoji: '🔨' },
];

interface DiffSummary {
  filesChanged: string[];
  insertions: number;
  deletions: number;
  diff: string;
}

interface ProjectConfig {
  template?: string;
  enableEmoji?: boolean;
  scopes?: string[];
  maxSubjectLength?: number;
  customTypes?: CommitType[];
}

// --- Git helpers ---

function getWorkspaceRoot(): string | undefined {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) { return undefined; }
  return folders[0].uri.fsPath;
}

function runGit(args: string, cwd: string): string {
  try {
    return execSync(`git ${args}`, { cwd, encoding: 'utf-8', timeout: 10000 }).trim();
  } catch {
    return '';
  }
}

function getStagedDiff(cwd: string): DiffSummary {
  const diff = runGit('diff --staged', cwd);
  const statOutput = runGit('diff --staged --stat', cwd);

  const filesChanged: string[] = [];
  let insertions = 0;
  let deletions = 0;

  const nameOutput = runGit('diff --staged --name-only', cwd);
  if (nameOutput) {
    filesChanged.push(...nameOutput.split('\n').filter(Boolean));
  }

  const summaryMatch = statOutput.match(/(\d+) insertions?\(\+\)/);
  const deletionMatch = statOutput.match(/(\d+) deletions?\(-\)/);
  if (summaryMatch) { insertions = parseInt(summaryMatch[1], 10); }
  if (deletionMatch) { deletions = parseInt(deletionMatch[1], 10); }

  return { filesChanged, insertions, deletions, diff };
}

// --- Smart detection ---

function detectTypeFromFiles(files: string[]): string {
  if (files.length === 0) { return 'chore'; }

  const allDocs = files.every((f) =>
    /\.(md|txt|rst|adoc)$/i.test(f) || f.toLowerCase().includes('readme') || f.toLowerCase().includes('changelog')
  );
  if (allDocs) { return 'docs'; }

  const allTests = files.every((f) =>
    /\.(test|spec)\.[jt]sx?$/i.test(f) || f.includes('__tests__') || f.includes('test/')
  );
  if (allTests) { return 'test'; }

  const allCI = files.every((f) =>
    f.includes('.github/workflows') || f.includes('.gitlab-ci') || f.includes('Jenkinsfile') || f.includes('.circleci')
  );
  if (allCI) { return 'ci'; }

  const allBuild = files.every((f) =>
    /^(package\.json|tsconfig\.json|webpack|rollup|vite|Makefile|Dockerfile|\.dockerignore|Cargo\.toml|go\.mod)/i.test(path.basename(f))
  );
  if (allBuild) { return 'build'; }

  const allStyle = files.every((f) =>
    /\.(css|scss|sass|less|styl)$/i.test(f) || f.includes('.prettierrc') || f.includes('.eslintrc')
  );
  if (allStyle) { return 'style'; }

  return 'feat';
}

function detectScopesFromFiles(files: string[]): string[] {
  const scopes = new Set<string>();
  for (const f of files) {
    const parts = f.replace(/\\/g, '/').split('/');
    if (parts.length >= 2) {
      // Use the first meaningful directory as scope
      const candidate = parts[0] === 'src' && parts.length >= 3 ? parts[1] : parts[0];
      if (candidate && candidate !== '.' && !candidate.startsWith('.')) {
        scopes.add(candidate);
      }
    }
  }
  return [...scopes].slice(0, 10);
}

function generateDescription(diffSummary: DiffSummary): string {
  const { filesChanged, insertions, deletions } = diffSummary;
  if (filesChanged.length === 0) { return ''; }

  if (filesChanged.length === 1) {
    const basename = path.basename(filesChanged[0]);
    if (insertions > 0 && deletions === 0) {
      return `add ${basename}`;
    } else if (deletions > 0 && insertions === 0) {
      return `remove ${basename}`;
    }
    return `update ${basename}`;
  }

  return `update ${filesChanged.length} files (+${insertions}/-${deletions})`;
}

// --- Project config (.commitcrafterrc) ---

function loadProjectConfig(cwd: string): ProjectConfig {
  const rcPath = path.join(cwd, '.commitcrafterrc');
  try {
    const raw = fs.readFileSync(rcPath, 'utf-8');
    return JSON.parse(raw) as ProjectConfig;
  } catch {
    return {};
  }
}

// --- Config helpers ---

function getConfig<T>(key: string, fallback: T, projectConfig: ProjectConfig): T {
  const projectValue = (projectConfig as Record<string, unknown>)[key.replace('commitCrafter.', '')];
  if (projectValue !== undefined) { return projectValue as T; }
  const vsConfig = vscode.workspace.getConfiguration('commitCrafter');
  return vsConfig.get<T>(key.replace('commitCrafter.', ''), fallback);
}

// --- Validation ---

function validateMessage(message: string, maxSubjectLength: number): string[] {
  const warnings: string[] = [];
  const lines = message.split('\n');
  const subject = lines[0] || '';

  if (subject.length > maxSubjectLength) {
    warnings.push(`Subject is ${subject.length} chars (max ${maxSubjectLength})`);
  }

  // Check body lines (72 char wrap)
  for (let i = 2; i < lines.length; i++) {
    if (lines[i].length > 72) {
      warnings.push(`Line ${i + 1} exceeds 72 chars (${lines[i].length})`);
    }
  }

  // Conventional commit format check
  if (!/^(feat|fix|docs|style|refactor|perf|test|build|ci|chore)(\(.+\))?!?:\s.+/.test(subject)) {
    warnings.push('Subject does not follow Conventional Commits format');
  }

  return warnings;
}

// --- Fill SCM input ---

function fillScmInputBox(message: string): void {
  const gitExt = vscode.extensions.getExtension('vscode.git');
  if (!gitExt) { return; }
  const gitApi = gitExt.exports.getAPI(1);
  if (!gitApi || gitApi.repositories.length === 0) { return; }
  gitApi.repositories[0].inputBox.value = message;
}

// --- Commands ---

async function generateCommand(): Promise<void> {
  const cwd = getWorkspaceRoot();
  if (!cwd) {
    vscode.window.showWarningMessage('Commit Crafter: No workspace folder open.');
    return;
  }

  const projectConfig = loadProjectConfig(cwd);
  const enableEmoji = getConfig('commitCrafter.enableEmoji', false, projectConfig);
  const template = getConfig('commitCrafter.template', '{type}({scope}): {description}', projectConfig);
  const configScopes = getConfig<string[]>('commitCrafter.scopes', [], projectConfig);
  const maxSubjectLength = getConfig('commitCrafter.maxSubjectLength', 50, projectConfig);

  // Get staged diff
  const diffSummary = getStagedDiff(cwd);
  if (diffSummary.filesChanged.length === 0) {
    vscode.window.showWarningMessage('Commit Crafter: No staged changes found. Stage files with `git add` first.');
    return;
  }

  // 1. Pick commit type
  const suggestedType = detectTypeFromFiles(diffSummary.filesChanged);
  const typeItems = COMMIT_TYPES.map((t) => ({
    label: enableEmoji ? `${t.emoji} ${t.label}` : t.label,
    description: t.description,
    picked: t.label === suggestedType,
    value: t.label,
    emoji: t.emoji,
  }));

  // Move suggested type to top
  typeItems.sort((a, b) => (a.picked ? -1 : b.picked ? 1 : 0));

  const pickedType = await vscode.window.showQuickPick(typeItems, {
    placeHolder: `Select commit type (suggested: ${suggestedType}) — ${diffSummary.filesChanged.length} file(s) staged`,
  });
  if (!pickedType) { return; }

  // 2. Pick scope
  const detectedScopes = detectScopesFromFiles(diffSummary.filesChanged);
  const allScopes = [...new Set([...configScopes, ...detectedScopes])];

  let scope = '';
  if (allScopes.length > 0) {
    const scopeItems = [
      { label: '(none)', description: 'No scope' },
      ...allScopes.map((s) => ({ label: s, description: '' })),
    ];
    const pickedScope = await vscode.window.showQuickPick(scopeItems, {
      placeHolder: 'Select scope (optional)',
    });
    if (pickedScope && pickedScope.label !== '(none)') {
      scope = pickedScope.label;
    }
  }

  // 3. Description
  const suggestedDesc = generateDescription(diffSummary);
  const description = await vscode.window.showInputBox({
    prompt: 'Enter commit description',
    value: suggestedDesc,
    placeHolder: 'Short description of the change',
    validateInput: (val) => {
      if (!val.trim()) { return 'Description is required'; }
      return undefined;
    },
  });
  if (!description) { return; }

  // 4. Breaking change?
  const breakingPick = await vscode.window.showQuickPick(
    [{ label: 'No', description: 'Regular commit' }, { label: 'Yes', description: 'BREAKING CHANGE' }],
    { placeHolder: 'Is this a breaking change?' }
  );
  if (!breakingPick) { return; }
  const isBreaking = breakingPick.label === 'Yes';

  // 5. Body (optional)
  const body = await vscode.window.showInputBox({
    prompt: 'Enter commit body (optional, press Enter to skip)',
    placeHolder: 'Longer description of the change',
  });

  // 6. Footer (optional)
  let footer = '';
  if (isBreaking) {
    footer = await vscode.window.showInputBox({
      prompt: 'Describe the breaking change',
      placeHolder: 'e.g., API endpoint renamed from /users to /accounts',
    }) || '';
  }

  // Build message from template
  const typeLabel = pickedType.value;
  const emojiPrefix = enableEmoji ? `${COMMIT_TYPES.find((t) => t.label === typeLabel)?.emoji || ''} ` : '';
  const breakingMark = isBreaking ? '!' : '';

  let subject = template
    .replace('{type}', typeLabel)
    .replace('({scope})', scope ? `(${scope})` : '')
    .replace('{scope}', scope)
    .replace('{description}', description);

  // Insert breaking mark before colon
  if (isBreaking) {
    subject = subject.replace(/:\s/, `${breakingMark}: `);
  }

  subject = emojiPrefix + subject;

  // Compose full message
  let message = subject;
  if (body) {
    message += `\n\n${body}`;
  }
  if (footer) {
    message += `\n\nBREAKING CHANGE: ${footer}`;
  }

  // Validate
  const warnings = validateMessage(message, maxSubjectLength);
  if (warnings.length > 0) {
    const proceed = await vscode.window.showWarningMessage(
      `Commit message warnings:\n${warnings.join('\n')}`,
      'Use anyway',
      'Edit',
      'Cancel'
    );
    if (proceed === 'Cancel' || !proceed) { return; }
    if (proceed === 'Edit') {
      const edited = await vscode.window.showInputBox({
        prompt: 'Edit commit message',
        value: message,
      });
      if (!edited) { return; }
      message = edited;
    }
  }

  // Fill SCM input box
  fillScmInputBox(message);
  vscode.window.showInformationMessage(`Commit Crafter: Message set — ${message.split('\n')[0]}`);
}

async function selectTemplateCommand(): Promise<void> {
  const cwd = getWorkspaceRoot();
  if (!cwd) {
    vscode.window.showWarningMessage('Commit Crafter: No workspace folder open.');
    return;
  }

  const projectConfig = loadProjectConfig(cwd);
  const enableEmoji = getConfig('commitCrafter.enableEmoji', false, projectConfig);
  const configScopes = getConfig<string[]>('commitCrafter.scopes', [], projectConfig);

  // Quick templates — pre-built conventional commit starters
  const templates = COMMIT_TYPES.map((t) => ({
    label: enableEmoji ? `${t.emoji} ${t.label}` : t.label,
    description: t.description,
    value: t.label,
  }));

  const picked = await vscode.window.showQuickPick(templates, {
    placeHolder: 'Select a commit type template',
  });
  if (!picked) { return; }

  // Optional scope
  let scope = '';
  if (configScopes.length > 0) {
    const scopeItems = [
      { label: '(none)', description: 'No scope' },
      ...configScopes.map((s) => ({ label: s, description: '' })),
    ];
    const pickedScope = await vscode.window.showQuickPick(scopeItems, {
      placeHolder: 'Select scope (optional)',
    });
    if (pickedScope && pickedScope.label !== '(none)') {
      scope = pickedScope.label;
    }
  }

  const emojiPrefix = enableEmoji ? `${COMMIT_TYPES.find((t) => t.label === picked.value)?.emoji || ''} ` : '';
  const scopePart = scope ? `(${scope})` : '';
  const prefix = `${emojiPrefix}${picked.value}${scopePart}: `;

  // Let user type description
  const description = await vscode.window.showInputBox({
    prompt: 'Enter commit description',
    placeHolder: 'Short description of the change',
    value: prefix,
    valueSelection: [prefix.length, prefix.length],
  });
  if (!description) { return; }

  fillScmInputBox(description);
  vscode.window.showInformationMessage(`Commit Crafter: Message set — ${description}`);
}

// --- Activation ---

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('commitCrafter.generate', generateCommand),
    vscode.commands.registerCommand('commitCrafter.selectTemplate', selectTemplateCommand),
  );
}

export function deactivate() {}
