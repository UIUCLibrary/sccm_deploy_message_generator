
pipeline {
    agent any
    parameters {
        booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run Automated Unit Tests")
    }
    stages {
        stage("Cloning Source") {
            agent any

            steps {
                deleteDir()
                checkout scm
                stash includes: '**', name: "Source", useDefaultExcludes: false

            }

        }

        stage("Unit tests") {
            when{
                expression{params.UNIT_TESTS == true}
            }
            steps {
                parallel(
                        "Windows": {
                            node(label: 'Windows') {
                                deleteDir()
                                unstash "Source"
                                bat "${env.TOX}  -e jenkins"
                                junit 'reports/junit-*.xml'

                            }
                        },
                        "Linux": {
                            node(label: "!Windows") {
                                deleteDir()
                                unstash "Source"
                                withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                                    sh "${env.TOX}  -e jenkins"
                                }
                                junit 'reports/junit-*.xml'
                            }
                        }
                )
            }
        }

    }
}