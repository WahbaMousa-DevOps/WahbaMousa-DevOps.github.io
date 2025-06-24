# Wahba Mousa – DevSecOps Portfolio Website (CI/CD + GitHub Pages)

![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-green?style=flat-square) ![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)
[![Security Rating](https://img.shields.io/badge/security-A+-green.svg)](https://github.com/your-username/your-repo/security)
[![SBOM](https://img.shields.io/badge/SBOM-compliant-blue.svg)](https://github.com/your-username/your-repo/security/supply-chain)

👤 **Created by**: Wahba Mousa – Senior DevOps Engineer

- CI/CD with GitHub Actions
- Security-first architecture (CodeQL, Trivy, Gitleaks, SBOM)
- Rolling deployment strategy
- Branch protection enforcement via GitHub CLI

[![CI Pipeline](https://github.com/WahbaMousa-DevOps/WahbaMousa-DevOps.github.io/actions/workflows/CI.yml/badge.svg)](https://github.com/WahbaMousa-DevOps/WahbaMousa-DevOps.github.io/actions/workflows/CI.yml)
[![Deploy to Production](https://github.com/WahbaMousa-DevOps/WahbaMousa-DevOps.github.io/workflows/Deploy%20to%20Production/badge.svg)](https://github.com/WahbaMousa-DevOps/WahbaMousa-DevOps.github.io/actions/workflows/deploy-production.yml)

## 🏗️ Architecture Overview: CI/CD + Security Flow

```
                ┌─────────────────────────────────────────────┐
                │                GitHub Repo                  │
                │      WahbaMousa-DevOps.github.io            │
                └─────────────────────────────────────────────┘
                               │
            ┌──────────────────┼────────────────────┐
            ▼                  ▼                    ▼
     Pull Request        Direct Pushes         Staticman API
 (e.g., feature → main)   (e.g., main)        (user comments form)
            │                  │                    │
            ▼                  ▼                    ▼
    .github/workflows/  .github/workflows/     staticman.yml
    └─ CI triggers:     └─ Deploy triggers         │
       test.yml             to staging/prod        ▼
       lint.yml             ───────────────►  _data/comments/ (via commit)
       trivy.yml
       codeql.yml
       scan.yml
       sbom.yml
       sbom-sign.yml
       lighthouse.yml

       coverage.yml
            │
            ▼
 ┌──────────────────────────────────────────────┐
 │     CI & Security Checks (Parallel Jobs)     │
 │ - Trivy FS + Trivy Image                     │
 │ - Gitleaks + git-secrets                     │
 │ - CodeQL + Jest Coverage                     │
 │ - SEO + Accessibility + SBOM                 │
 └──────────────────────────────────────────────┘
            │
            ▼
 ┌────────────────────────────────────────────────────────────┐
 │        Auto-label/merge (PR Bot), Bad PR Filter            │
 │    └─ auto-label.yml, auto-merge.yml, bad-pr.yml           │
 └────────────────────────────────────────────────────────────┘
            │
            ▼
 ┌────────────────────────────────────┐
 │     Branch Protection Enforcement  │
 │ └─ enforce-branch-protection.yml   │
 │    └─ Reads: branch-protection.yml │
 │    └─ Applies via Python/CLI       │
 └────────────────────────────────────┘
            │
            ▼
 ┌────────────────────────────────────────────────────────────┐
 │      GitHub Pages Rolling Deployment (CD)                  │
 │ └─ deploy-page-staging.yml  →  "Success"                   │
 │ └─ deploy-page-production.yml  →  Environment              │
 └────────────────────────────────────────────────────────────┘
            │
            ▼
 ┌──────────────────────────────────────────────┐
 │             Public Website                   │
 │  ┌────────────────────────────────────┐      │
 │  │           wahba.aiopsvision.com    │      │
 │  │                                    │      │
 │  └────────────────────────────────────┘      │
 └──────────────────────────────────────────────┘

```
📝 Note: `sbom-image.yml` and Cosign-based Docker image signing are included as modular references for future container-based pipelines. They are **not active** in this static GitHub Pages project.


### 🌐  Rolling Deployments
- **Production**: [https://wahba.aiopsvision.com](https://wahba.aiopsvision.com)

## 🚀 Technology Stack

| Area        | Tools/Tech                                   |
|-------------|----------------------------------------------|
| Frontend    | Jekyll, GitHub Pages           |
| CI/CD       | GitHub Actions, Environments, Artifacts      |
| Security    | CodeQL, Trivy (FS), Gitleaks, Secret Scanning|
| Branching   | GitFlow (`main`, `release`, `develop`, etc.) |
| SBOM        | Anchore (CycloneDX), Syft (reference only)   |
| Governance  | Branch protection rules, PR automation       |

## 🔒 Security Architecture
### Aligned with OWASP Standards

| Area                                 | How You're Covered                                    |
|--------------------------------------|-------------------------------------------------------|
| **Secrets in Code (A03:2021)**       | `gitleaks`, `git-secrets`, `secret.yml`               |
| **Vulnerable Components (A06:2021)** | `Trivy FS`, `Trivy Image`, `SBOM`                     |
| **Security Misconfig (A05:2021)**    | GitHub branch protection, token management            |
| **Software Integrity (A08:2021)**    | `Cosign` signing, `SBOM` attestation                  |
| **CI/CD Exposure (A10:2021)**        | Modular workflows + policy enforcement                |
| **OWASP CycloneDX**                  | SBOM format generated via `sbom.yml`, `sbom-sign.yml` |

### Verified Quality Metrics

| Metric            | Status           | Notes                                                |
|-------------------|------------------|------------------------------------------------------|
| **Code Coverage** | Enabled       | Reported via Jest + Codecov                         |
| **Security Score**| A+ Equivalent | Secret scanning, SBOM, image signing                |
| **Performance**   | <2s load time | Jekyll site + CDN = fast load                       |
| **Accessibility** | Enabled       | Checked via axe-core CI workflow                    |
| **SEO Score**     | >90/100       | Verified via Lighthouse CI audit                    |


## 🌳 Git Branching Strategy

### **GitFlow Implementation**

```
main        ← 🟦 Production Environment
├── release ← 🟩 Staging Environment
    ├── develop       ← Integration / QA Branch
        ├── feature/* ← New Features
        ├── hotfix/*  ← Emergency Fixes
        └── bugfix/*  ← Bug Patches

```
swap.yml is used to promote release → main after successful staging validation.

### **Branch Protection Rules**

#### **Main Branch ( Production)**
```yaml
Require PR review (1+)
Require code owner review
Require status checks to pass
Require branches up to date
Require conversation resolution
Require linear history
Lock branch (prevent bypass)
Restrict force pushes
Restrict deletions

```

#### **Release Branch ( Staging → Production Candidate)**
```yaml
Require PR review (1+)
Require code owner review
Require status checks to pass
Require branches up to date
Require conversation resolution
Require linear history
Lock branch (prevent bypass)
Restrict force pushes
Restrict deletions

```

## 🔄 CI/CD Pipeline Architecture

### **Continuous Integration**

```yaml
Triggers: Push to [develop, feature/*, hotfix/*, release, main]

Stages:
  1. Build with Jekyll (or App Build)
  2. Unit Tests (Jest / npm test)
  3. Lint (Markdown, JS, etc.)
  4. Code Coverage + Lighthouse + SEO
  5. CodeQL Security Scan
  6. Trivy FS Scan (Source)
  7. Trivy Image Scan (Docker)
  8. SBOM Generation (Syft / Trivy)
  9. Image Signing (Cosign)
 10. Quality Gate Summary
```

## 🔧 Local Development

### **Setup Instructions**
```bash
# Clone repository
git clone https://github.com/WahbaMousa-DevOps/WahbaMousa-DevOps.github.io.git
cd WahbaMousa-DevOps.github.io

# Install dependencies
bundle install

# Run locally
bundle exec jekyll serve

# Access development server
http://localhost:4000
```

### **Development Workflow**
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test locally
bundle exec jekyll serve

# Run local quality checks
./scripts/local-lint.sh
./scripts/local-security-scan.sh

# Commit and push
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name

# Create pull request to develop branch
```

## 🤝 Contributing

### **Contribution Guidelines**
1. Fork the repository
2. Create feature branch from `develop`
3. Follow coding standards and security practices
4. Ensure all quality gates pass
5. Submit pull request with detailed description
6. Code review and approval process
7. Automated deployment to Staging
8. promotion to Production


<!-- ## 📞 Support & Contact

### **DevOps Team**
- **Lead DevOps Engineer**: WahbaMousa-DevOps
- **Email**: devops@aiopsvision.com
- **Slack**: #devops-support
- **On-call**: PagerDuty integration

### **Emergency Contacts**
- **Production Issues**: +1-xxx-xxx-xxxx
- **Security Incidents**: security@aiopsvision.com
- **Escalation Manager**: manager@aiopsvision.com -->

> 📦 Designed and implemented by Wahba Mousa — Senior DevSecOps Engineer (2025)
This repository serves as a real-world demonstration of CI/CD + DevSecOps excellence on GitHub.

## 📚 Credits & License
* Theme: [Jekyll](https://jekyllrb.com/) + [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) by [Michael Rose](https://mademistakes.com/)
* Customizations by [Wahba Mousa](https://github.com/engineerwahba)

Licensed under [MIT](LICENSE)

## 💬 Feedback
If you have questions or want to learn how to build a similar site, feel free to:
* Connect with me on [LinkedIn](https://www.linkedin.com/in/engineerwahba/)
