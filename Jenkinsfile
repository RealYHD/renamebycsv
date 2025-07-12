pipeline {
    agent {
        kubernetes {
            cloud 'rsys-devel'
            defaultContainer 'pip'
            inheritFrom 'pip'
        }
    }
    stages {
        stage("install") {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage("build") {
            steps {
                sh 'rm -rf ./dist/*'
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
                archiveArtifacts artifacts: 'dist/*.tar.gz, dist/*.whl', fingerprint: true, followSymlinks: false, onlyIfSuccessful: true
            }
        }
        stage("publish package") {
            environment {
                CREDS = credentials('rs-git-package-registry-ydeng')
            }
            when {
                branch '**/master'
            }
            steps {
                sh returnStatus: true, script: 'python -m twine upload --repository-url https://git.reslate.systems/api/packages/${CREDS_USR}/pypi -u ${CREDS_USR} -p ${CREDS_PSW} --non-interactive --disable-progress-bar --verbose dist/*'
            }
        }
    }
}