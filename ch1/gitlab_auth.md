# Setting up your GitLab account

## Sign Up for a GitLab Account

1. Open your web browser and go to the [GitLab sign-up website](https://gitlab.com/users/sign_up).
2. In the registration page you can choose between different sign-up options. You can sign up using your Google, GitHub, or GitLab account, or you can create a new account by providing your email address and a password. If you choose to sign up with your email address, enter your email in the designated field and create a strong password. Make sure to follow any password requirements that GitLab may have.
3. After entering your email and password, click on the "Register" button to proceed.
GitLab may send you a confirmation email to verify your email address. Check your inbox and follow the instructions in the email to complete the verification process.
4. Once your email is verified, you will be redirected to your GitLab account dashboard. From here, you can start creating and managing your repositories, collaborate with others, and explore the various features offered by GitLab.

## Create and Use a Personal Access Token for GitLab

To securely authenticate and interact with GitLab repositories over HTTPS (such as creating, cloning, and pushing to repositories), you need to use a Personal Access Token (PAT) instead of your password. Here’s how to create and use a token:

1. **Generate a Personal Access Token:**
   - Log in to your GitLab account.
   - Click on your profile avatar in the upper right corner and select "Edit profile" or "Preferences".
   - In the left sidebar, click on "Access Tokens".
   - Click on "Add new token".
   - In Token name, give your token a descriptive name (e.g., "My Laptop Token").
   - Set an expiration date if desired.
   - Under "Select scopes", select at least `api` and `write_repository` (or just `write_repository` if you only need to push and pull code).
   - Click the "Create token" button.
   - **Copy the generated token and save it somewhere secure.** You will not be able to see it again.

2. **Use the Token for Git Operations:**
   - When you perform Git operations over HTTPS (such as `git clone`, `git push`, or `git pull`), Git will prompt you for a username and password.
   - Use your GitLab username as the username.
   - **Paste your personal access token as the password.**

3. **Store the Token for Convenience (Optional):**
   - To avoid entering your token every time, you can use a credential helper to cache your credentials:
     ```
     git config --global credential.helper cache
     ```
   - Or, for longer-term storage:
     ```
     git config --global credential.helper store
     ```
   - The next time you enter your token, it will be saved for future use.

   > **Note:**  
   > - If you use `credential.helper cache`, your token is stored temporarily in memory (RAM) and is not written to disk.  
   >   By default, it is cached for 15 minutes (900 seconds). You can change this with `git config --global credential.helper 'cache --timeout=SECONDS'`.  
   > - If you use `credential.helper store`, your token is saved in plain text (not encrypted) in the file `~/.git-credentials` on Linux/macOS or `%USERPROFILE%\.git-credentials` on Windows.  
   > - For better security, consider using a platform-specific credential manager (like `osxkeychain` on macOS or `wincred`/`manager` on Windows), which stores credentials encrypted and protected by your operating system.

4. **Verify Your Setup:**
   - Try cloning a repository:
     ```
     git clone https://gitlab.com/your-username/your-repo.git
     ```
   - When prompted, use your username and the token as described above.
   - You can also try pushing a commit to verify that authentication works.

That's it! You can now securely create, clone, and commit to repositories on GitLab using your personal access token.
   - If the key was added correctly, you will see a message confirming your connection to GitLab.

That's it! You've successfully copied your SSH key from your computer to GitLab, allowing you to securely authenticate with GitLab repositories using SSH.
