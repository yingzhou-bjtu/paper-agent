const fs = require('fs');
const path = require('path');

const skills = {
  'paper-launch': [],
  'paper-search': ['search-sources', 'query-construction', 'quality-filter', 'relevance-scoring', 'citation-traversal'],
  'paper-idea': ['innovation-methods'],
  'paper-plan': ['training-recipes', 'env-compat'],
  'paper-data': ['data-pipeline', 'contamination-check'],
  'paper-env': ['env-compat'],
  'paper-train': ['training-recipes', 'results-analysis'],
  'paper-story': ['story-patterns'],
  'paper-write': ['abstract', 'introduction', 'related-work', 'method', 'experiments', 'conclusion', 'revision', 'figures-and-tables'],
  'paper-review': ['review-rubric'],
  'paper-rebuttal': ['rebuttal-strategies'],
  'paper-audit': ['audit-checklist']
};

const conferences = ['icml', 'iclr', 'neurips', 'aaai', 'ijcai', 'cvpr', 'iccv', 'eccv', 'acl', 'emnlp', 'kdd', 'sigir', 'www', 'wsdm', 'icse', 'sp'];

let ok = true;

// Check each skill's SKILL.md and reference files
Object.entries(skills).forEach(([skill, refs]) => {
  const skillPath = 'skills/' + skill + '/SKILL.md';
  if (!fs.existsSync(skillPath)) {
    console.error('MISSING: ' + skillPath);
    ok = false;
  } else {
    const content = fs.readFileSync(skillPath, 'utf8');
    if (!content.includes('name:') || !content.includes('description:')) {
      console.error('INVALID FRONTMATTER: ' + skillPath);
      ok = false;
    }
    if (!content.includes('## Output Format')) {
      console.error('MISSING "## Output Format" section in ' + skillPath);
      ok = false;
    }
    if (!content.includes('## Done When')) {
      console.error('MISSING "## Done When" section in ' + skillPath);
      ok = false;
    }
  }

  refs.forEach(ref => {
    const refPath = 'skills/' + skill + '/references/' + ref + '.md';
    if (!fs.existsSync(refPath)) {
      console.error('MISSING: ' + refPath);
      ok = false;
    }
  });
});

// Check conference profiles
conferences.forEach(conf => {
  const confPath = 'references/conferences/' + conf + '.md';
  if (!fs.existsSync(confPath)) {
    console.error('MISSING: ' + confPath);
    ok = false;
  } else {
    const content = fs.readFileSync(confPath, 'utf8');
    const required = ['Basic Info', 'Review Weights', 'Writing Style', 'Recent Trends', 'Reviewer Common Concerns', 'Anti-patterns', 'Success Patterns'];
    required.forEach(section => {
      if (!content.includes(section)) {
        console.error('MISSING SECTION "' + section + '" in ' + confPath);
        ok = false;
      }
    });
  }
});

// Check root files
['CLAUDE.md', 'install.sh', 'cli.js', 'README.md', 'package.json'].forEach(f => {
  if (!fs.existsSync(f)) {
    console.error('MISSING: ' + f);
    ok = false;
  }
});

// Cross-validate cli.js skill lists against this file
const cliContent = fs.readFileSync('cli.js', 'utf8');
const cliSkillsMatch = cliContent.match(/const SKILLS = \[([\s\S]*?)\]/);
const cliConfMatch = cliContent.match(/const CONFERENCE_SKILLS = \[([\s\S]*?)\]/);
const cliBundlesMatch = cliContent.match(/const BUNDLES = \{([\s\S]*?)\};/);

if (!cliSkillsMatch) {
  console.error('CROSS-CHECK: Cannot find SKILLS array in cli.js');
  ok = false;
} else {
  const cliSkills = cliSkillsMatch[1].match(/'([^']+)'/g).map(s => s.replace(/'/g, ''));
  const validateSkills = Object.keys(skills);
  const missingInCli = validateSkills.filter(s => !cliSkills.includes(s));
  const extraInCli = cliSkills.filter(s => !validateSkills.includes(s));
  if (missingInCli.length > 0) {
    console.error('CROSS-CHECK: Skills in validate.js but missing from cli.js: ' + missingInCli.join(', '));
    ok = false;
  }
  if (extraInCli.length > 0) {
    console.error('CROSS-CHECK: Skills in cli.js but missing from validate.js: ' + extraInCli.join(', '));
    ok = false;
  }
}

if (!cliConfMatch) {
  console.error('CROSS-CHECK: Cannot find CONFERENCE_SKILLS array in cli.js');
  ok = false;
} else {
  const cliConfSkills = cliConfMatch[1].match(/'([^']+)'/g).map(s => s.replace(/'/g, ''));
  const expectedConfSkills = ['paper-search', 'paper-launch', 'paper-review'];
  if (JSON.stringify(cliConfSkills.sort()) !== JSON.stringify(expectedConfSkills.sort())) {
    console.error('CROSS-CHECK: CONFERENCE_SKILLS in cli.js does not match expected: ' + expectedConfSkills.join(', '));
    ok = false;
  }
}

if (!cliBundlesMatch) {
  console.error('CROSS-CHECK: Cannot find BUNDLES object in cli.js');
  ok = false;
}

if (ok) {
  console.log('All files valid');
} else {
  process.exit(1);
}
