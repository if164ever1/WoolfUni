pipelineJob('django-cicd') {
  description('Build Django with Kaniko, push to ECR, update the GitOps Helm values, and let Argo CD deploy it.')
  keepDependencies(false)
  logRotator {
    numToKeep(20)
    artifactNumToKeep(5)
  }
  properties {
    disableConcurrentBuilds()
  }
  triggers {
    scm('H/5 * * * *')
  }
  definition {
    cpsScm {
      lightweight(true)
      scm {
        git {
          remote {
            url('${source_repository_url}')
            credentials('github-pat')
          }
          branch('*/${source_repository_branch}')
          extensions {
            cloneOptions {
              shallow(true)
              depth(20)
              timeout(10)
            }
          }
        }
      }
      scriptPath('${jenkinsfile_path}')
    }
  }
}

queue('django-cicd')
