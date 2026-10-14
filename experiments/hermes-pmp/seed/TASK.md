# Bounded fixture task

Normalize every item label in fixture.json with whitespace splitting and joining
with one ASCII space. Preserve schema, IDs, item order and all other fields.
For this fixture the resulting labels are "Portable memory" and "Evidence chain".
Acceptance: `python -I -m unittest discover -s . -p test_fixture.py -v` must pass three tests.
The model returns JSON; the host writes the fixture and executes tests. The model
must not claim it executed those tests. No other implementation change is allowed.
Next actor: Codex. Next action: independently rerun the three acceptance tests,
verify the evidence hashes and record a continuation receipt; do not expand scope.
