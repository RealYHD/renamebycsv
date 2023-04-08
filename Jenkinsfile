pipeline {
    agent any
    stages {
        stage("install") {
            steps {
                sh 'conda env update --file environment.yml'
                sh 'echo "conda activate renamebycsv" >> ~/.bashrc'
            }
        }
        stage("build") {
            steps {
                sh "python -m build"
            }
        }
        stage("publish") {
            when {
            branch '**/master'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'rs-git-package-registry-ydeng', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "python -m twine upload --repository-url https://git.reslate.systems/api/packages/${USER}/pypi -u ${USER} -p ${PASS} --non-interactive --disable-progress-bar --verbose dist/*"
                }
            }
        }
    }
}