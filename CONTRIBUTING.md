# Contributing

Thanks for your interest in improving DocScribe!

How to contribute
- Open an issue to discuss large changes before making a PR.
- For bug fixes and small features, feel free to open a PR directly.

Development setup
1. Install Python 3.10+ and Tesseract (see README)
2. Create a virtualenv and install deps:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run tests:
   ```
   pytest -q
   ```

PR guidelines
- Keep changes focused and small.
- Add or update tests where applicable.
- Update README/docs if behavior changes.

Code of Conduct
By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).