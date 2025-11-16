# Credentials Directory

⚠️ **SECURITY WARNING**: This directory contains sensitive credentials and is excluded from Git via `.gitignore`.

## Google Drive Service Account Setup

If you want to use Google Drive integration:

1. **Create your service account** following the instructions in `docs/SETUP.md`
2. **Download the JSON key file** from Google Cloud Console
3. **Rename it to `service_account.json`** and place it in this directory
4. **Verify it's not tracked by Git**: Run `git status` - you should NOT see this file listed

## Template

A template file `service_account.json.example` is provided as a reference for the expected structure.

**Copy it and fill in your actual credentials**:
```bash
cp service_account.json.example service_account.json
# Then edit service_account.json with your real credentials
```

## Security Best Practices

✅ **DO**:
- Keep credentials in this directory (protected by .gitignore)
- Use environment variables when possible
- Rotate credentials regularly
- Use service accounts with minimal required permissions

❌ **DON'T**:
- Commit actual credentials to Git
- Share credentials in chat, email, or documentation
- Use production credentials in development
- Grant excessive permissions to service accounts

## Verify Protection

Check that credentials are protected:
```bash
# This should return empty (credentials/ is in .gitignore)
git ls-files app/credentials/

# This should show True
git check-ignore app/credentials/service_account.json
```

---

**Remember**: Your `.gitignore` includes `credentials/` to protect these files. Never use `git add -f` on actual credential files!
