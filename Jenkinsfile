pipeline {
    agent any
    stages {
        stage("clean") {
            steps {
                sh 'rm -rf ./dist/*'
            }
        }
        stage("install") {
            steps {
                sh 'mamba env update --file environment.yml'
                sh 'echo "mamba activate renamebycsv" >> ~/.bashrc'
            }
        }
        stage("build") {
            steps {
                sh "python -m build"
            }
        }
        stage("test") {
            steps {
                sh "pip install dist/*.whl --force-reinstall"
                sh "renamebycsv -h"
            }
        }
        stage("archive") {
            steps {
                archiveArtifacts artifacts: 'dist/*.tar.gz, dist/*.whl'
            }
        }
        stage("publish package") {
            when {
                branch '**/master'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'rs-git-package-registry-ydeng', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh 'python -m twine upload --repository-url https://git.reslate.systems/api/packages/${USER}/pypi -u ${USER} -p ${PASS} --non-interactive --disable-progress-bar --verbose dist/*'
                }
            }
        }
    }
}