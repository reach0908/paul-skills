// Evaluates grader regexes with JavaScript semantics, as `claude plugin eval` does.
// stdin: [{id, pattern, flags?, match?, text}]; stdout: [{id, matched, error?}].
// `match` is contains (default), not_contains or count:N.
const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const items = JSON.parse(Buffer.concat(chunks).toString('utf8'));
const results = items.map(({ id, pattern, flags = '', match = 'contains', text }) => {
  try {
    if (match === 'contains') return { id, matched: new RegExp(pattern, flags).test(text) };
    if (match === 'not_contains') return { id, matched: !new RegExp(pattern, flags).test(text) };
    const count = /^count:(\d+)$/.exec(match);
    if (count) {
      const global = flags.includes('g') ? flags : flags + 'g';
      return { id, matched: (text.match(new RegExp(pattern, global)) || []).length === Number(count[1]) };
    }
    return { id, matched: false, error: `unknown match mode ${match}` };
  } catch (error) {
    return { id, matched: false, error: String(error) };
  }
});
process.stdout.write(JSON.stringify(results));
