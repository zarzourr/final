pipeline {
    agent any

    environment {
        GIT_REPO = "https://github.com/your-username/auto-refactor.git"
        TARGET_BRANCH = "refactored"
        GIT_CREDENTIALS_ID = "github-token"
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: "${env.GIT_REPO}",
                    credentialsId: "${env.GIT_CREDENTIALS_ID}"
            }
        }

        stage('Run Refactor Script') {
            steps {
                sh '''
                echo "🧠 Running refactor script..."
                python3 refactor.py
                '''
            }
        }

        stage('Format with Black') {
            steps {
                sh '''
                echo "🧹 Formatting code with Black..."
                black . > format_output.txt || true
                '''
            }
        }

        stage('Commit & Push Changes') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${env.GIT_CREDENTIALS_ID}", usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    sh '''
                    git config user.name "jenkins-bot"
                    git config user.email "jenkins@ci.local"
                    git checkout -B ${TARGET_BRANCH}
                    git add .
                    git commit -m "🤖 Auto-refactored code [skip ci]" || echo "Nothing to commit"
                    git push https://${GIT_USER}:${GIT_PASS}@github.com/your-username/auto-refactor.git ${TARGET_BRANCH}
                    '''
                }
            }
        }

        stage('Archive Report') {
            steps {
                archiveArtifacts artifacts: 'refactor_log.txt,format_output.txt', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "✅ Auto-refactor pipeline finished."
        }
    }
}
