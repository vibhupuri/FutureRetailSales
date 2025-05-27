pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'vibhupuri/future-retail-sales:latest'
        MLFLOW_TRACKING_URI = 'http://mlflow-server:5000' // replace with your MLflow server
        EXPERIMENT_NAME = 'FutureRetailSales'
    }

    parameters {
        string(name: 'N_ESTIMATORS', defaultValue: '300', description: 'Number of estimators')
        string(name: 'MAX_DEPTH', defaultValue: '8', description: 'Max depth of trees')
        string(name: 'LEARNING_RATE', defaultValue: '0.05', description: 'Learning rate')
        string(name: 'RMSE', defaultValue: '1.8668', description: 'Root Mean Squared Error')
        string(name: 'MAE', defaultValue: '1.0123', description: 'Mean Absolute Error')
        string(name: 'MODEL_VERSION', defaultValue: 'xgb-v1', description: 'Model run name/version')
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/vibhupuri/FutureRetailSales.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d'
            }
        }

        stage('Log to MLflow') {
            steps {
                sh """
                python3 -c "
import mlflow

mlflow.set_tracking_uri('$MLFLOW_TRACKING_URI')
mlflow.set_experiment('$EXPERIMENT_NAME')

with mlflow.start_run(run_name='${params.MODEL_VERSION}'):
    mlflow.log_param('n_estimators', ${params.N_ESTIMATORS})
    mlflow.log_param('max_depth', ${params.MAX_DEPTH})
    mlflow.log_param('learning_rate', ${params.LEARNING_RATE})
    mlflow.log_metric('RMSE', ${params.RMSE})
    mlflow.log_metric('MAE', ${params.MAE})
"
                """
            }
        }
    }
}
