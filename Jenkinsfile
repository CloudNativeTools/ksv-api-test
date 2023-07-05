pipeline {
    agent {
        label 'master'
    }
    environment {
        image_name = 'ksv_api_test'
    }
    stages {
        stage('check out') {
            steps {
                // Get some code from a GitHub repository
                git credentialsId: 'ksv-ssh', url:'https://github.com/CloudNativeTools/ksv-api-test', branch: '${branch}'

            }
        }
        // 提前准备好镜像，不用每次都重新打镜像
        stage('build image') {
            steps {
                sh "docker build -t $image_name:1.0 . "
            }
        }

        stage('run test') {
            steps {
                wrap([$class: 'BuildUser']) {
                  script {
                      BUILD_USER = "${env.BUILD_USER}"
                  }
				}

                dir("report") {
				    deleteDir()
				}

                sh "echo run testcase in docker..."
                sh "docker rm -f $image_name && docker run -itd --name=$image_name --net=host -v ${WORKSPACE}:/data/autotest $image_name:1.0 /bin/bash"
                sh "docker exec  $image_name arun -e $testenv --mp --dist-file testcases/test_api"
                // sh "docker exec  hpc_api_test arun -e $testenv -m debug"
                // docker生成挂载目录有权限问题，使用docker cp
                sh "docker cp $image_name:/data/autotest/reports report"


            }

            post {
                always {
                    // archiveArtifacts 'report/*.html'
					script {
						allure jdk: '', report: "report/html", results: [[path: "report/json"]]
						sh "docker exec $image_name bash -c 'cp -r report/html/ reports/ && python send_msg.py --simple --webhook ${webhook} --build_user=${BUILD_USER} --test_env=${testenv} --report_url=${env.BUILD_URL}allure'"
					}
                }


            }
        }
    }


    post {
        always {
            script{
                html_file = "${WORKSPACE}/reports/aomaker.html"
                html_content = readFile html_file
            }
            echo "${env.JOB_NAME}"
            mail bcc: '',to: 'qiaoshilu@yunify.com',
            from:'noreply@qingcloud.com',
            mimeType: 'text/html',
            subject: "【KSV自动化巡检】${env.JOB_NAME} - Build # ${env.BUILD_NUMBER}: $currentBuild.result",
            body: """
             <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <title>${JOB_NAME}-第${BUILD_NUMBER}次构建日志</title>
            </head>


            <body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4"
    offset="0">
    <table width="95%" cellpadding="0" cellspacing="0"  style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
        <tr>
            本邮件由系统自动发出，无需回复！<br/>
            各位同事，大家好，以下为${JOB_NAME }项目构建信息</br>
            <td><font color="#CC0000">构建结果 - ${currentBuild.result}</font></td>
        </tr>
        <tr>
            <td><br />
            <b><font color="#0B610B">构建信息</font></b>
            <hr size="2" width="100%" align="center" /></td>
        </tr>
        <tr>
            <td>
                <ul>
                    <li>项目名称 ： ${JOB_NAME}</li>
                    <li>构建编号 ： 第${BUILD_NUMBER}次构建</li>
                    <li>构建状态： ${currentBuild.result}</li>
                    <li>构建日志： <a href="${BUILD_URL}console">${BUILD_URL}console</a></li>
                    <li>构建  Url ： <a href="${BUILD_URL}">${BUILD_URL}</a></li>
                    <li>项目  Url ： <a href="${JOB_URL}">${JOB_URL}</a></li>
                     <li>测试报告： <a href="${BUILD_URL}allure">${BUILD_URL}allure</a></li>
                </ul>
                <div>${html_content}</div>
            </td>
                    </tr>
                </table>
            </body>
            </html>
            """
        }
    }
}