# Create csv users.csv with a column "GitHubUser" containing the GitHub usernames of the students
rm -rf tmp
mkdir tmp
python3 scripts/clone_github_repo.py --csv scripts/users.csv --csv-column "GitHubUser" --output-subdir tmp --results-csv tmp/results.csv
git clone https://github.com/mcallara/autograder tmp/autograder
python3 scripts/update_results_with_grades.py tmp/results.csv --autograder-dir tmp/autograder --projects-dir tmp