# Setting up your GitLab account

## Sign Up for a GitLab Account

1. Open your web browser and go to the [GitLab sign-up website](https://gitlab.com/users/sign_up).
2. On the registration page, you have several sign-up options. You can use an existing Google or GitHub account, or you can create a new GitLab account by providing your email address and creating a password. If you choose to sign up with your email, enter it in the designated field and create a strong password, following any listed requirements.
3. After entering your details, click the "Register" button. GitLab may send a confirmation email to verify your address. Check your inbox and follow the instructions to complete the process.
4. Once your email is verified, you will be redirected to your GitLab dashboard. From here, you can start creating repositories, collaborating with others, and exploring GitLab's features.

## Create and Use a Personal Access Token for GitLab

To securely interact with your GitLab repositories over HTTPS (for example, creating, cloning, and pushing), you should use a Personal Access Token (PAT) instead of your account password.

1. **Generate a Personal Access Token**
   - Log in to your GitLab account.
   - Click your profile avatar in the upper-right corner and select "Preferences".
   - In the left sidebar, click on "Access Tokens".
   - Click "Add new token".
   - Give your token a descriptive name (e.g., "My Laptop Token").
   - Set an expiration date for the token. For security, it's a good practice to set an expiration date.
   - Under "Select scopes," choose the permissions the token will have. For command-line Git operations, you will need `write_repository` and `read_api`.
   - Click the "Create personal access token" button.
   - **Important:** Copy the generated token immediately and save it in a secure location, like a password manager. You will not be able to see it again after you leave this page.

2. **Use the Token for Git Operations**
   - When you perform a Git operation over HTTPS (like `git clone`, `git push`, or `git pull`), you will be prompted for a username and password.
   - For the username, enter your GitLab username.
   - For the password, paste your Personal Access Token.

3. **Store the Token for Convenience (Optional)**
   - To avoid entering your token for every operation, you can configure Git to cache your credentials.

   - To cache your token temporarily (usually for 15 minutes):
     ```bash
     git config --global credential.helper cache
     ```
   - To store your token for a longer duration in a plain text file:
     ```bash
     git config --global credential.helper store
     ```

   Next time you perform a Git operation, Git will prompt you for your username and token, and it will then store them according to the helper you configured. This way, you won't have to enter your credentials every time you interact with GitLab.

   > **Note on Security:**
   > - `credential.helper cache` stores the token in memory for a limited time. You can change the default timeout with `git config --global credential.helper 'cache --timeout=SECONDS'`.
   > - `credential.helper store` saves the token in plain text in a file named `.git-credentials` in your home directory. This is more convenient but less secure.
   > - For better security, consider using a platform-specific credential manager, such as `osxkeychain` on macOS or `manager` on Windows. These tools store your credentials securely and are often the default if available.

4. **Verify Your Setup**
   - Test your setup by creating and pushing a new repository to GitLab:
     ```bash
     # Create a new directory and navigate into it
     mkdir my-test-repo
     cd my-test-repo

     # Initialize a new Git repository
     git init

     # Add a remote pointing to your new GitLab repository URL
     git remote add origin https://gitlab.com/your-username/my-test-repo.git

     # Create an empty commit
     git commit --allow-empty -m "Initial commit"

     # Push the commit to GitLab
     git push -u origin main
     ```
   - Replace `your-username` with your GitLab username.
   - If you haven't configured a credential helper, Git will prompt for your username and password (your PAT). If the push is successful, your authentication is working correctly.

That's it! You can now securely create, clone, and push to repositories on GitLab using your Personal Access Token.