# M+AI+CE Hackathon Registration Guide

This guide will help you get set up and registered for the M+AI+CE hackathon.

## 📋 Registration Checklist

Follow these steps to complete your registration:

### ✅ Step 1: Create Required Accounts

- [ ] **Google Account** (if you don't have one)
  - Visit: [accounts.google.com](https://accounts.google.com/)
  - This will be used for all other account registrations

- [ ] **GitHub Account** (using Google)
  - Visit: [github.com/signup](https://github.com/signup)
  - Sign up using your Google account
  - Note your GitHub username for registration

- [ ] **Claude Account** (using Google)
  - Visit: [console.anthropic.com](https://console.anthropic.com/)
  - Sign up using your Google account
  - Generate an API key (see Step 2)

- [ ] **Google Developer Account**
  - Visit: [console.cloud.google.com](https://console.cloud.google.com/)
  - Create a new project for the hackathon
  - Enable required APIs (see Step 3)

### ✅ Step 2: Obtain API Keys

#### Claude API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Navigate to **API Keys** section
3. Click **Create Key**
4. Name it "MAICE Hackathon"
5. Copy the key and save it securely
6. You'll add this to your `.env` file later

#### Google OAuth Credentials

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth client ID**
5. Configure the OAuth consent screen if prompted
6. Select **Web application** as the application type
7. Add authorized redirect URIs:
   - `http://localhost:3000/auth/callback`
   - `http://localhost:8000/auth/callback`
   - Add your production URL when deployed
8. Copy the **Client ID** and **Client Secret**
9. Save these securely for your `.env` file

### ✅ Step 3: Submit Registration

To get access to the repository, provide the following information:

**Registration Form** (submit via Slack or email):

```
Name: [Your Full Name]
Email: [Your Google Account Email]
GitHub Username: [Your GitHub Username]
Organization (optional): [Your Company/University]
Experience Level: [Beginner/Intermediate/Advanced]
Team Name (optional): [If participating as a team]
```

**Where to Submit:**
- **Slack**: Post in the #registration channel at [maice-workspace.slack.com](https://maice-workspace.slack.com)
- **Email**: Contact organizers (details in Slack)

### ✅ Step 4: Join the Community

- [ ] **Join Slack Workspace**
  - Visit: [maice-workspace.slack.com](https://maice-workspace.slack.com)
  - Use your Google account to sign in
  - Introduce yourself in #introductions
  - Check #announcements for updates

- [ ] **Accept GitHub Repository Invitation**
  - Check your email for the repository invitation
  - Accept the invitation to become a collaborator
  - Star the repository to show your support!

### ✅ Step 5: Set Up Development Environment

Once you have repository access:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/stephencummins/mace-digital-compliance-checker.git
   cd mace-digital-compliance-checker
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key_here
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   ```

5. **Test Your Setup**
   ```bash
   python check_compliance.py --help
   ```

## 🎯 Quick Start After Registration

Once you're registered and set up:

1. **Read the Documentation**
   - [HACKATHON.md](HACKATHON.md) - Hackathon overview and rules
   - [README.md](README.md) - Technical documentation
   - [docs/ISO_19650_GUIDE.md](docs/ISO_19650_GUIDE.md) - ISO standards reference

2. **Explore the Codebase**
   - Review the existing code structure
   - Check out the example documents
   - Run the sample validation scripts

3. **Join a Team or Go Solo**
   - Post in #team-formation on Slack
   - Or register as a solo participant

4. **Start Building**
   - Pick a challenge level (Bronze, Silver, or Gold)
   - Create a feature branch
   - Start coding!

## 🆘 Troubleshooting

### Common Issues

**Issue**: Can't access the repository
- **Solution**: Make sure you've accepted the GitHub invitation email
- **Solution**: Verify your GitHub username was submitted correctly

**Issue**: Claude API key not working
- **Solution**: Check that you copied the entire key without spaces
- **Solution**: Verify the key is active in the Anthropic console

**Issue**: Google OAuth errors
- **Solution**: Ensure redirect URIs are correctly configured
- **Solution**: Check that the OAuth consent screen is published

**Issue**: Python dependencies won't install
- **Solution**: Make sure you're using Python 3.11 or higher
- **Solution**: Try upgrading pip: `pip install --upgrade pip`

### Getting Help

- **Slack**: Ask in #technical-help
- **GitHub**: Open an issue with the `question` label
- **Documentation**: Check the [docs/](docs/) folder

## 📅 Important Dates

- **Registration Opens**: Check Slack for announcement
- **Hackathon Kickoff**: Check Slack for announcement
- **Submission Deadline**: Check Slack for announcement
- **Winner Announcement**: Check Slack for announcement

## 🎉 You're Ready!

Once you've completed all the steps above, you're ready to participate in the M+AI+CE hackathon!

**Next Steps:**
1. Join the kickoff session (details in Slack)
2. Review the challenge requirements
3. Start building your solution
4. Have fun and learn!

---

**Questions?** Ask in the Slack #registration channel or check [HACKATHON.md](HACKATHON.md) for more information.

**Good luck and happy hacking!** 🚀
