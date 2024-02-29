# Quick Guide: Add your public SSH Keys from Your Computer to GitLab

Copying SSH keys from your computer to GitLab allows you to securely authenticate with GitLab repositories without having to enter your username and password each time. Here's a quick guide on how to do it:

1. **Locate Your SSH Keys:**
   - Open a terminal or command prompt on your computer.
   - Navigate to the directory where your SSH keys are stored. By default, SSH keys are usually stored in `~/.ssh/` directory on Unix-like systems (such as Linux or macOS) or `C:\Users\YourUsername\.ssh\` directory on Windows.

2. **Generate SSH Keys (if you don't have them already):**
   - If you don't have SSH keys yet, you can generate them using the `ssh-keygen` command:
     ```
     ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
     ```
   - Follow the prompts to generate the keys. Press Enter to accept the default file location (`~/.ssh/id_rsa`) and no passphrase, or customize it as needed.

3. **Display Your Public SSH Key:**
   - Use the `cat` command to display your public SSH key:
     ```
     cat ~/.ssh/id_rsa.pub
     ```
   - This will output your public SSH key to the terminal.

4. **Copy Your Public SSH Key:**
   - Select the entire content of your public SSH key displayed in the terminal, starting with `ssh-rsa` and ending with your email address.
   - Copy the selected text to your clipboard.

5. **Add SSH Key to GitLab:**
   - Log in to your GitLab account.
   - Click on your profile avatar in the upper right corner and select "Settings" from the dropdown menu.
   - In the left sidebar, click on "SSH Keys".
   - Paste the copied public SSH key into the "Key" field.
   - Optionally, provide a descriptive title for the key in the "Title" field (e.g., "My Laptop SSH Key").
   - Click the "Add key" button to save the SSH key.

6. **Verify SSH Key Addition:**
   - To verify that your SSH key has been successfully added, you can use the following command:
     ```
     ssh -T git@gitlab.com
     ```
   - If the key was added correctly, you will see a message confirming your connection to GitLab.

That's it! You've successfully copied your SSH key from your computer to GitLab, allowing you to securely authenticate with GitLab repositories using SSH.
