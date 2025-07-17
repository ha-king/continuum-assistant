# Son of Anton - Multi-Environment AI Assistant Platform

A sophisticated Streamlit application featuring 28+ specialized AI assistants with real-time web browsing capabilities, deployed across production and development environments with automated CI/CD.

## 🚀 Live Applications

### Production Environment
- **URL**: https://d2wyi9setnpika.cloudfront.net
- **Branch**: `main`
- **Environment**: `prod`
- **CI/CD**: ✅ Automated deployment on push to main

### Development Environment
- **URL**: https://d2e0ww502aa30c.cloudfront.net
- **Branch**: `dev`
- **Environment**: `dev`
- **CI/CD**: ✅ Automated deployment on push to dev

## 🤖 Available Assistants

### Core Assistants
- **Math Assistant** - Mathematical calculations and problem solving
- **English Assistant** - Writing, grammar, and literature
- **Computer Science Assistant** - Programming and algorithms
- **Financial Assistant** - Business finance and accounting
- **AWS Assistant** - Cloud architecture and best practices
- **Research Assistant** - Real-time web research and data gathering
- **Web Browser Assistant** - Live website browsing and analysis

### Specialized Experts
- **Psychology Assistant** - Mental health and behavioral analysis
- **Cryptography Assistant** - Encryption and security protocols
- **Blockchain Assistant** - Distributed ledger technology
- **Cryptocurrency Assistant** - Digital currency analysis
- **Economics Assistant** - Economic theory and market analysis
- **Cybersecurity Offense/Defense** - Security testing and protection
- **Formula 1 Assistant** - Live F1 race data, standings, and comprehensive analysis with multi-source integration (OpenF1, Ergast, ESPN)
- **AI Assistant** - Artificial intelligence and machine learning
- **Nuclear Energy Assistant** - Nuclear technology and safety
- **Data Analysis Assistant** - Statistical analysis and insights

## 🔧 CI/CD Deployment Instructions

### Automatic Deployment
1. **Production**: Push changes to `main` branch
2. **Development**: Push changes to `dev` branch

### Manual Deployment
```bash
# Production
cdk deploy StreamlitAssistantStack --require-approval never

# Development
cdk deploy StreamlitAssistantStackDev --app "python3 app_dev.py" --require-approval never
```

## 🏗️ Architecture

- **Frontend**: Streamlit with Cognito authentication
- **Backend**: AWS ECS Fargate containers
- **Distribution**: CloudFront CDN
- **CI/CD**: AWS CodePipeline with GitHub integration
- **Infrastructure**: AWS CDK (Python)

## 🔐 Authentication

Both environments use AWS Cognito for secure user authentication with environment-specific user pools.

## 📝 Development Workflow

1. Create feature branch from `dev`
2. Make changes and test locally
3. Push to feature branch
4. Create PR to `dev` branch
5. Merge triggers automatic dev deployment
6. Test in dev environment
7. Create PR from `dev` to `main`
8. Merge triggers automatic prod deployment

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r docker_app/requirements.txt

# Run locally
cd docker_app
streamlit run app.py
```

## 📊 Features

- ✅ 28+ Specialized AI Assistants
- ✅ Real-time Web Browsing Capabilities
- ✅ Live Data Integration (F1, Crypto, Aviation)
- ✅ OpenF1 API Integration for live F1 data
- ✅ Multi-tab Chat Interface
- ✅ Reference Tracking
- ✅ Environment-specific Authentication
- ✅ Automated CI/CD Pipeline
- ✅ Multi-environment Deployment
- ✅ Current Date/Time Awareness