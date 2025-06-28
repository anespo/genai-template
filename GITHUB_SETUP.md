# GitHub Repository Setup Guide

This guide helps you set up the GenAI Template repository on GitHub.

## 🚀 Quick Setup

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `genai-template`
3. Set it as **Public** (recommended for templates)
4. **Don't** initialize with README, .gitignore, or license (we already have them)

### 2. Push Local Repository

```bash
# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/genai-template.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Configure Repository Settings

#### Enable GitHub Pages (Optional)
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs`
4. This will make documentation available at `https://YOUR_USERNAME.github.io/genai-template`

#### Set Repository Topics
Add these topics to help users find your template:
- `cookiecutter`
- `template`
- `genai`
- `llm`
- `openai`
- `bedrock`
- `gemini`
- `fastapi`
- `streamlit`
- `python`

#### Configure Branch Protection (Recommended)
1. Go to Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

## 📋 Repository Configuration

### Secrets for CI/CD
Add these secrets in Settings → Secrets and variables → Actions:

```
OPENAI_API_KEY=sk-your-test-key-for-ci
GEMINI_API_KEY=your-test-key-for-ci
```

### Environment Variables
For testing in CI, you might want to add:
```
PYTHONPATH=/github/workspace
LOG_LEVEL=DEBUG
```

## 🏷️ Release Management

### Creating Releases

1. **Tag the release:**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0: Initial stable release"
   git push origin v1.0.0
   ```

2. **Create GitHub Release:**
   - Go to Releases → Create a new release
   - Choose the tag `v1.0.0`
   - Title: `v1.0.0 - Initial Release`
   - Description: Copy from CHANGELOG.md

### Release Notes Template
```markdown
## 🚀 What's New

- Multi-provider support for OpenAI, AWS Bedrock, and Google Gemini
- FastAPI backend with async support
- Streamlit interactive dashboard
- Command-line interface (CLI)
- Docker containerization support

## 📦 Installation

```bash
cookiecutter https://github.com/YOUR_USERNAME/genai-template
```

## 🔧 Breaking Changes

None in this release.

## 🐛 Bug Fixes

- Fixed issue with...

## 📚 Documentation

- Added comprehensive README
- Added deployment guide
- Added examples and tutorials

## 🙏 Contributors

Thanks to all contributors who made this release possible!
```

## 📊 Analytics & Insights

### Enable Repository Insights
1. Go to Insights tab
2. Enable:
   - Traffic (to see clone/download stats)
   - Community (to track community health)
   - Dependency graph
   - Security advisories

### Badges for README
Add these badges to your README.md:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/genai-template.svg)](https://github.com/YOUR_USERNAME/genai-template/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/genai-template.svg)](https://github.com/YOUR_USERNAME/genai-template/network)
[![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/genai-template.svg)](https://github.com/YOUR_USERNAME/genai-template/issues)
[![GitHub license](https://img.shields.io/github/license/YOUR_USERNAME/genai-template.svg)](https://github.com/YOUR_USERNAME/genai-template/blob/main/LICENSE)
[![CI](https://github.com/YOUR_USERNAME/genai-template/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/genai-template/actions)
```

## 🤝 Community Setup

### Discussion Categories
Enable Discussions and create categories:
- 💡 **Ideas** - Feature requests and suggestions
- 🙋 **Q&A** - Questions and help
- 🗣️ **General** - General discussion
- 📢 **Announcements** - Updates and news
- 🎯 **Show and tell** - Projects built with the template

### Issue Templates
We've already included:
- Bug report template
- Feature request template
- Pull request template

### Contributing Guidelines
- CONTRIBUTING.md is already included
- Code of conduct (optional): Add CODE_OF_CONDUCT.md

## 📈 Marketing & Promotion

### Cookiecutter Template Registry
Submit to the official cookiecutter template list:
1. Fork [cookiecutter/cookiecutter](https://github.com/cookiecutter/cookiecutter)
2. Add your template to the README
3. Submit a pull request

### Social Media
Share on:
- Twitter/X with hashtags: #cookiecutter #genai #llm #python
- LinkedIn with a post about the template
- Reddit on r/Python, r/MachineLearning
- Dev.to with a tutorial article

### Blog Post Ideas
- "Building a Multi-Provider GenAI Application with Python"
- "From Idea to Production: GenAI Template Tutorial"
- "Comparing OpenAI, Bedrock, and Gemini in One Application"

## 🔧 Maintenance

### Regular Tasks
- [ ] Update dependencies monthly
- [ ] Review and merge community PRs
- [ ] Update documentation as needed
- [ ] Monitor security advisories
- [ ] Test with new Python versions

### Automation
Set up GitHub Actions for:
- Dependency updates (Dependabot)
- Security scanning
- Automated testing
- Release automation

## 📞 Support Channels

Set up support channels:
1. **GitHub Issues** - Bug reports and feature requests
2. **GitHub Discussions** - Community Q&A
3. **Documentation** - Comprehensive guides
4. **Examples** - Working code samples

## 🎯 Success Metrics

Track these metrics:
- ⭐ GitHub stars
- 🍴 Forks
- 📥 Downloads/clones
- 🐛 Issues resolved
- 💬 Community engagement
- 📝 Documentation views

## 🚀 Next Steps

After setting up the repository:

1. **Test the template** with `./test_template.sh`
2. **Create your first release** (v1.0.0)
3. **Share with the community**
4. **Gather feedback** and iterate
5. **Add more providers** based on demand

## 📝 Repository Checklist

- [ ] Repository created on GitHub
- [ ] Code pushed to main branch
- [ ] Repository description added
- [ ] Topics/tags configured
- [ ] Branch protection enabled
- [ ] Secrets configured for CI
- [ ] Discussions enabled
- [ ] Issues templates working
- [ ] CI/CD pipeline passing
- [ ] README badges added
- [ ] First release created
- [ ] Documentation complete
- [ ] Community guidelines set

Your GenAI Template is now ready for the community! 🎉
