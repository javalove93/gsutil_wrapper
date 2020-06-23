# gsutil_wrapper

AWS S3 Bucket의 파일을 대량으로 GCS로 복사하는 유틸리티

## 사용방법

<pre>
usage: gsutil_wrapper [-h] path_list
</pre>

## 필요 옵션

* 파일 FD 개수(권장): ulimit -n 4096
* aws cli 설치 및 aws configure 구성
* gsutil 설치 및 Service Account 지정

## path_list 포맷

<pre>
# Options
#
# 최대로 병렬 실행할 gsutil 개수
# MAX_PROCESSES 100
#
# 로컬 저장 공간(임시 파일 저장소로 사용할)의 크기 GB
# MAX_TEMP_STORAGE 100
#
# 최대 병렬 실행 gsutil의 개수나 로컬 저장소가 꽉 찰 경우 대기 상태에 들어감
#
# Samples
# s3://gcs-jerry/ gs://s3-to-gcs-jerry/ -r
# s3://gcs-jerry/xa* gs://s3-to-gcs-jerry/
# s3://gcs-jerry/xb* gs://s3-to-gcs-jerry/
# s3://gcs-jerry/testfolder/ gs://s3-to-gcs-jerry/testfolder/ -r

# 소스 타겟 [-r 옵션]
# Wildcard 사용 가능 (크기가 큰 파일은 이 옵션이 빠름)
# -r 옵션을 사용하면 서브 디렉토리까지 복사. 단, Wildcard를 사용할 수 없음
s3://gcs-jerry/smallfiles/ gs://s3-to-gcs-jerry/smallfiles/ -r
s3://gcs-jerry/* gs://s3-to-gcs-jerry/
s3://gcs-jerry/smallfiles2/ gs://s3-to-gcs-jerry/smallfiles2/ -r

</pre>
