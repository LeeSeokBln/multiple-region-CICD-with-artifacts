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
