![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/62669117-cab3-426c-aaa3-f88376866e5d)
### 보안 팀 파이프라인
1. 보안팀 직원이 보안 관련된 파일을 ap-northeast-2에 있는 Code Commit의 Main브런치에 Push한다.
2. 개발 팀에서 IaC 코드를 개발하고 us-east-1에 있는 Code Commit의 dev 브런치에 Push하면 Code Build에서 Build진행 후 보안 팀의 Code Commit에 request라는 브런치에 Push한다.
3. 개발 팀에서 요청한 파일을 Code Build에서 보안 검사 후 개발 팀의 Code Commit의 complate브런치에 Push한다.
   - 만약 보안 상의 문제가 있는 코드일 경우 인프라를 구축하지 않고 알림을 발생시킨다.
### 개발 팀 파이프라인
1. 개발 팀 직원이 Code Commit의 인프라 구축에 필요한 파일을 dev브런치에 Push한다.
2. 개발 팀 Code Build에 해당 파일을 보안 팀의 Code Commit에 request브런치에 Push한다.
3. 또한 패키지의 업/다운로드가 필요한 파일들은 CodeArtifacts에 해당 패키지를 Push 또는 Pull 해준다.
4. Push된 request브런치는 보안 팀 Code Build에서 보안 검사를 진행하고 CloudForation을 통해서 Push된다.
 - 보안 검사 과정
     -  우선 보안 팀의 Code Commit의 main 브런치에서 보안 검사 소프트웨어를 다운 받아 보안 검사를 실시한다.
     -  검사가 정상 적으로 끝난 소스코드는 CloudFormation을 통해서 인프라를 배포한다.
          - 만약 비정상 적인 코드일 경우 인프라 배포를 하지 않으며, 알림이 전송된다.
### Create Code Commit
```
$ aws codecommit create-repository --repository-name project-secure-codecommit-repo --region ap-northeast-2
$ aws codecommit create-repository --repository-name project-infra-codecommit-repo --region us-east-1
```
```
$ mkdir project-sources ; cd project-sources
$ git init
$ git remote add infra https://git-codecommit.us-east-1.amazonaws.com/v1/repos/project-infra-codecommit-repo
$ git remote add secure https://git-codecommit.ap-northeast-2.amazonaws.com/v1/repos/project-secure-codecommit-repo
```
파일을 압축 해제 후 infra Remote에 Push 
```
$ git branch -m main dev
$ git add -A
$ git commit -m 'init'
$ git push --set-upstream infra dev
```
정상 적으로 Code Commit에 올라왔는지 확인
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/50f4aaa5-336a-4d24-ae97-0096650033b5)

### Create CodeArtifacts Project
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/117cdf09-35c3-49f5-967c-f0eb4a87db98)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/f1ff4fc2-1ce3-4fab-aa3d-5e5251cd5b60)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/f59f4453-1b74-46d0-9457-06d7364fbedc)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/2bf9ef24-6ddc-4584-bf48-7cd0be74b711)
Buildspec작성 후 업로드
```
version: 0.2

phases:
  install:
    run-as: root
    commands:
      - pip3 install twine
      - pip3 install wheel
      
  pre_build:
    commands:
      - git init
      - cd modules/
      - aws sts get-caller-identity
      - python3 setup.py install
      - python3 setup.py build
      - python3 setup.py test
      - aws codeartifact login --tool twine --domain project-infra --domain-owner <계정 ID> --repository project-infra-repository --region us-east-1

  build:
    commands:
      - python3 setup.py sdist bdist_wheel
      - pip3 install -U pip
      - cd ..
      - rm -rf modules

  post_build:
    commands:
      - twine upload --repository codeartifact ./modules/dist/*
      - git remote add secure https://git-codecommit.ap-northeast-2.amazonaws.com/v1/repos/project-secure-codecommit-repo
      - git branch -m master request
      - git add -A
      - git commit -m 'init'
      - git push --set-upstream secure request
```
```
$ git add -A
$ git commit -m 'Add Buildspec'
$ git push infra dev
```
### Create Code Pipeline
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/7f635303-d0b6-47ce-87a9-5305341c14c0)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/1d9da1f1-b654-409f-9bbd-c6155b8db97d)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/20a4e29f-c36e-4bc7-a379-f1a42f4f28d6)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/227c1967-93e4-421c-8558-abc2b7e64715)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/e8ecbea7-34cd-4ec9-b7e2-8f24300bc5c5)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/debf7e2f-9b56-480d-80ca-98203ea867eb)
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/58756b9c-e119-42bf-b484-14b4e34dd9cc)
나머지는 모두 기본 값으로 생성
![Untitled](https://github.com/LeeSeokBln/multiple-rigion-code-pipelines-security-checks-and-code-artifacts/assets/101256150/40a34f1b-ae7c-4104-ab16-9a25ec5e1a07)
CodePipeline을 생성, 해당 CodeBuild IAM Role에 아래와 같은 권한을 부여하면 완성됩니다
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "codeartifact:PutRepositoryPermissionsPolicy",
                "codeartifact:GetAuthorizationToken",
                "codeartifact:PutPackageOriginConfiguration",
                "codeartifact:GetRepositoryEndpoint",
                "sts:GetServiceBearerToken"
            ],
            "Resource": "*"
        }
    ]
}
```

### 보안팀 파이프라인 생성

